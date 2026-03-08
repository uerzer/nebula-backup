#!/usr/bin/env python3
"""Full pipeline: generate site -> tar -> git bundle
All in one script to avoid sandbox recycling between steps.
"""
import os
import sys
import subprocess
import shutil

# Paths
GEN_SCRIPT = "/home/user/files/scripts/scripts/generate_sauna_site_v2.py"
CSV_PATH = "/home/user/files/data/sauna_master_database.csv"
TMP_OUT = "/tmp/sauna-site-v2"
TMP_GIT = "/tmp/sauna-git"
TAR_OUT = "/home/user/files/tmp/sauna-site-v2.tar.gz"
BUNDLE_OUT = "/home/user/files/tmp/sauna-v2.bundle"

def main():
    # Verify inputs exist
    print("[1/5] Checking inputs...")
    if not os.path.exists(GEN_SCRIPT):
        print(f"ERROR: Generator script not found at {GEN_SCRIPT}")
        sys.exit(1)
    if not os.path.exists(CSV_PATH):
        print(f"ERROR: CSV database not found at {CSV_PATH}")
        sys.exit(1)
    print(f"  Generator: {GEN_SCRIPT} ({os.path.getsize(GEN_SCRIPT):,} bytes)")
    print(f"  CSV: {CSV_PATH} ({os.path.getsize(CSV_PATH):,} bytes)")

    # Clean previous outputs
    for d in [TMP_OUT, TMP_GIT]:
        if os.path.exists(d):
            shutil.rmtree(d)

    # Copy generator to /tmp and modify output path
    print("\n[2/5] Preparing generator...")
    with open(GEN_SCRIPT, 'r') as f:
        gen_code = f.read()
    # Replace the output directory to use /tmp
    gen_code = gen_code.replace(
        'OUT_DIR  = "/home/user/files/code/sauna-site-v2"',
        f'OUT_DIR  = "{TMP_OUT}"'
    )
    tmp_gen = "/tmp/generate_sauna_site_v2.py"
    with open(tmp_gen, 'w') as f:
        f.write(gen_code)
    print(f"  Modified generator saved to {tmp_gen}")

    # Run generator
    print("\n[3/5] Running site generator...")
    result = subprocess.run(
        [sys.executable, tmp_gen],
        capture_output=True, text=True,
        cwd="/tmp"
    )
    print(result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout)
    if result.returncode != 0:
        print("STDERR:", result.stderr[-1000:])
        sys.exit(1)

    # Count files
    file_count = 0
    total_size = 0
    for root, dirs, files in os.walk(TMP_OUT):
        for fn in files:
            fp = os.path.join(root, fn)
            file_count += 1
            total_size += os.path.getsize(fp)
    print(f"\n=== FILES GENERATED ===")
    print(f"  Count: {file_count}")
    print(f"  Size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")

    # Create tar.gz
    print("\n[4/5] Creating tar.gz...")
    os.makedirs(os.path.dirname(TAR_OUT), exist_ok=True)
    result = subprocess.run(
        ["tar", "czf", TAR_OUT, "-C", "/tmp", "sauna-site-v2"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: tar failed: {result.stderr}")
        sys.exit(1)
    tar_size = os.path.getsize(TAR_OUT)
    print(f"  {TAR_OUT} ({tar_size:,} bytes / {tar_size/1024/1024:.1f} MB)")

    # Create git bundle
    print("\n[5/5] Creating git bundle...")
    os.makedirs(TMP_GIT, exist_ok=True)
    cmds = [
        ["git", "init"],
        ["git", "config", "user.name", "uerzer"],
        ["git", "config", "user.email", "phobik2000+ai@gmail.com"],
    ]
    for cmd in cmds:
        subprocess.run(cmd, cwd=TMP_GIT, capture_output=True)

    # Copy files
    for item in os.listdir(TMP_OUT):
        src = os.path.join(TMP_OUT, item)
        dst = os.path.join(TMP_GIT, item)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    subprocess.run(["git", "add", "-A"], cwd=TMP_GIT, capture_output=True)
    result = subprocess.run(
        ["git", "commit", "-m", "Deploy SaunaFinder v2 - 4478 static pages"],
        cwd=TMP_GIT, capture_output=True, text=True
    )
    print(f"  Commit: {result.stdout.strip().split(chr(10))[0]}")

    os.makedirs(os.path.dirname(BUNDLE_OUT), exist_ok=True)
    result = subprocess.run(
        ["git", "bundle", "create", BUNDLE_OUT, "HEAD"],
        cwd=TMP_GIT, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERROR: bundle failed: {result.stderr}")
        sys.exit(1)
    bundle_size = os.path.getsize(BUNDLE_OUT)
    print(f"  {BUNDLE_OUT} ({bundle_size:,} bytes / {bundle_size/1024/1024:.1f} MB)")

    print("\n" + "="*60)
    print("=== ALL DONE ===")
    print(f"  Site files: {file_count} files ({total_size/1024/1024:.1f} MB)")
    print(f"  Tar:    {TAR_OUT} ({tar_size/1024/1024:.1f} MB)")
    print(f"  Bundle: {BUNDLE_OUT} ({bundle_size/1024/1024:.1f} MB)")
    print("="*60)

if __name__ == "__main__":
    main()
