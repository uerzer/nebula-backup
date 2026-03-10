#!/usr/bin/env python3
"""Push SaunaFinder v2 static site to GitHub using the Git Data API.

Atomic push of ALL files in a single commit.

Usage:
  GITHUB_TOKEN=ghp_xxx python3 push_sauna_v2.py
  python3 push_sauna_v2.py --token ghp_xxx
  python3 push_sauna_v2.py --token ghp_xxx --dry-run
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

REPO = "uerzer/sauna-finder"
BRANCH = "main"
SITE_DIR = "/home/user/files/code/sauna-site-v2"
COMMIT_MSG = "feat: SaunaFinder v2 - complete static site with 4,040 venues"
API_BASE = "https://api.github.com"
PRESERVE = {"README.md", "DEPLOYMENT_GUIDE.md", "PROJECT_SUMMARY.md", ".nojekyll", ".github", "CNAME"}
MAX_WORKERS = 10


class GitHubPusher:
    def __init__(self, token, repo=REPO, branch=BRANCH):
        self.token = token
        self.repo = repo
        self.branch = branch
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github.v3+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })

    def _api(self, method, path, **kwargs):
        url = API_BASE + path if path.startswith("/") else path
        for attempt in range(3):
            resp = self.session.request(method, url, **kwargs)
            if resp.status_code == 403 and "rate limit" in resp.text.lower():
                reset = int(resp.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset - int(time.time()), 10)
                print("  Rate limited. Waiting " + str(wait) + "s...")
                time.sleep(wait + 1)
                continue
            if resp.status_code == 502 and attempt < 2:
                time.sleep(5)
                continue
            break
        return resp

    def get_ref(self):
        r = self._api("GET", "/repos/" + self.repo + "/git/ref/heads/" + self.branch)
        r.raise_for_status()
        return r.json()["object"]["sha"]

    def get_commit(self, sha):
        r = self._api("GET", "/repos/" + self.repo + "/git/commits/" + sha)
        r.raise_for_status()
        return r.json()

    def get_tree(self, sha, recursive=True):
        params = {"recursive": "1"} if recursive else {}
        r = self._api("GET", "/repos/" + self.repo + "/git/trees/" + sha, params=params)
        r.raise_for_status()
        return r.json()

    def create_blob(self, content_b64):
        r = self._api("POST", "/repos/" + self.repo + "/git/blobs", json={
            "content": content_b64, "encoding": "base64"
        })
        r.raise_for_status()
        return r.json()["sha"]

    def create_tree(self, tree_entries, base_tree=None):
        payload = {"tree": tree_entries}
        if base_tree:
            payload["base_tree"] = base_tree
        r = self._api("POST", "/repos/" + self.repo + "/git/trees", json=payload)
        r.raise_for_status()
        return r.json()["sha"]

    def create_commit(self, message, tree_sha, parent_sha):
        r = self._api("POST", "/repos/" + self.repo + "/git/commits", json={
            "message": message, "tree": tree_sha, "parents": [parent_sha]
        })
        r.raise_for_status()
        return r.json()["sha"]

    def update_ref(self, commit_sha):
        r = self._api("PATCH", "/repos/" + self.repo + "/git/refs/heads/" + self.branch, json={
            "sha": commit_sha, "force": True
        })
        r.raise_for_status()
        return r.json()

    def collect_files(self, site_dir):
        site_path = Path(site_dir)
        files = []
        for fpath in sorted(site_path.rglob("*")):
            if fpath.is_file():
                rel = str(fpath.relative_to(site_path))
                files.append((rel, str(fpath)))
        return files

    def create_blobs_parallel(self, files, max_workers=MAX_WORKERS):
        results = []
        total = len(files)
        completed = 0
        errors = []

        def upload_one(item):
            rel_path, abs_path = item
            with open(abs_path, "rb") as f:
                content = f.read()
            b64 = base64.b64encode(content).decode("ascii")
            sha = self.create_blob(b64)
            return (rel_path, sha)

        print("  Creating " + str(total) + " blobs with " + str(max_workers) + " workers...")
        start = time.time()
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(upload_one, f): f for f in files}
            for future in as_completed(futures):
                completed += 1
                try:
                    rel_path, sha = future.result()
                    results.append((rel_path, sha))
                except Exception as e:
                    errors.append(str(e))
                if completed % 500 == 0 or completed == total:
                    elapsed = time.time() - start
                    rate = completed / elapsed if elapsed > 0 else 0
                    print("    [" + str(completed) + "/" + str(total) + "] " + "{:.1f}".format(rate) + "/s")
        elapsed = time.time() - start
        print("  Done: " + str(len(results)) + " blobs in " + "{:.1f}".format(elapsed) + "s")
        if errors:
            print("  Errors: " + str(len(errors)))
            for e in errors[:5]:
                print("    " + e)
        return results

    def push(self, site_dir=SITE_DIR, commit_msg=COMMIT_MSG, dry_run=False):
        t0 = time.time()
        print("[1/6] Collecting files...")
        files = self.collect_files(site_dir)
        total_size = sum(os.path.getsize(f[1]) for f in files)
        print("  " + str(len(files)) + " files (" + "{:.1f}".format(total_size / 1024 / 1024) + " MB)")

        if dry_run:
            by_dir = {}
            for rel, _ in files:
                d = str(Path(rel).parent)
                by_dir[d] = by_dir.get(d, 0) + 1
            print("[DRY RUN] Would push:")
            for d in sorted(by_dir):
                print("  " + d + ": " + str(by_dir[d]) + " files")
            return

        print("[2/6] Getting branch state...")
        commit_sha = self.get_ref()
        commit = self.get_commit(commit_sha)
        base_tree_sha = commit["tree"]["sha"]
        print("  Commit: " + commit_sha[:8])

        print("[3/6] Reading existing tree...")
        existing_tree = self.get_tree(base_tree_sha, recursive=True)
        preserved = []
        for item in existing_tree.get("tree", []):
            top = item["path"].split("/")[0]
            if top in PRESERVE and item["type"] == "blob":
                preserved.append({"path": item["path"], "mode": item["mode"], "type": "blob", "sha": item["sha"]})
        print("  Preserving " + str(len(preserved)) + " entries")

        print("[4/6] Uploading blobs...")
        blob_results = self.create_blobs_parallel(files)
        if len(blob_results) < len(files) * 0.9:
            print("  ABORTING: >10% failures")
            return

        print("[5/6] Creating tree...")
        tree_entries = list(preserved)
        for rel_path, sha in blob_results:
            tree_entries.append({"path": rel_path, "mode": "100644", "type": "blob", "sha": sha})
        print("  " + str(len(tree_entries)) + " entries")
        new_tree_sha = self.create_tree(tree_entries)
        print("  Tree: " + new_tree_sha[:8])

        print("[6/6] Creating commit...")
        new_commit_sha = self.create_commit(commit_msg, new_tree_sha, commit_sha)
        self.update_ref(new_commit_sha)
        elapsed = time.time() - t0
        print("  Push complete in " + "{:.1f}".format(elapsed) + "s")
        print("  Commit: " + new_commit_sha)
        print("  URL: https://github.com/" + self.repo + "/commit/" + new_commit_sha)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--site-dir", default=SITE_DIR)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--workers", type=int, default=MAX_WORKERS)
    args = parser.parse_args()
    if not args.token:
        print("ERROR: Set GITHUB_TOKEN or use --token")
        print("  Create at: https://github.com/settings/tokens")
        print("  Scope needed: repo")
        sys.exit(1)
    if not os.path.isdir(args.site_dir):
        print("ERROR: Site dir not found: " + args.site_dir)
        sys.exit(1)
    pusher = GitHubPusher(args.token)
    pusher.push(args.site_dir, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
