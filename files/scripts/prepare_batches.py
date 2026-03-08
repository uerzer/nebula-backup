#!/usr/bin/env python3
"""Walk sauna-site-v2, base64-encode all files, split into batch JSONs."""

import os
import json
import base64
from collections import Counter

SITE_DIR = "/home/user/files/code/sauna-site-v2"
OUT_DIR = "/home/user/files/data"
BATCH_SIZE = 100

os.makedirs(OUT_DIR, exist_ok=True)

# Walk the directory and collect all files
all_files = []
total_size = 0

for root, dirs, files in os.walk(SITE_DIR):
    dirs.sort()
    for fname in sorted(files):
        full_path = os.path.join(root, fname)
        rel_path = os.path.relpath(full_path, SITE_DIR)

        with open(full_path, "rb") as f:
            content = f.read()

        b64 = base64.b64encode(content).decode("ascii")
        file_size = len(content)
        total_size += file_size

        all_files.append({
            "path": rel_path,
            "content_base64": b64
        })

all_files.sort(key=lambda x: x["path"])

total_files = len(all_files)
print(f"Total files collected: {total_files}")
print(f"Total raw size: {total_size:,} bytes ({total_size / 1024 / 1024:.1f} MB)")

# Split into batches
num_batches = (total_files + BATCH_SIZE - 1) // BATCH_SIZE
batch_filenames = []

for i in range(num_batches):
    start = i * BATCH_SIZE
    end = min(start + BATCH_SIZE, total_files)
    batch = all_files[start:end]

    batch_filename = f"push_batch_{i+1:03d}.json"
    batch_path = os.path.join(OUT_DIR, batch_filename)

    with open(batch_path, "w") as f:
        json.dump(batch, f)

    batch_size = os.path.getsize(batch_path)
    batch_filenames.append(batch_filename)
    print(f"  Batch {i+1:3d}: {len(batch):3d} files, {batch_size:>12,} bytes ({batch_size/1024/1024:.1f} MB)")

# Create manifest
manifest = {
    "total_files": total_files,
    "total_batches": num_batches,
    "total_raw_size_bytes": total_size,
    "total_raw_size_mb": round(total_size / 1024 / 1024, 1),
    "batch_size": BATCH_SIZE,
    "batch_files": batch_filenames
}

manifest_path = os.path.join(OUT_DIR, "push_manifest.json")
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest saved to: {manifest_path}")
print(f"\n{'='*60}")
print(f"  SUMMARY")
print(f"{'='*60}")
print(f"  Total files:   {total_files:,}")
print(f"  Total size:    {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
print(f"  Total batches: {num_batches}")
print(f"  Batch size:    {BATCH_SIZE} files per batch")
print(f"{'='*60}")

# File type breakdown
ext_counter = Counter()
ext_size = Counter()
for item in all_files:
    ext = os.path.splitext(item["path"])[1] or "(no ext)"
    ext_counter[ext] += 1
    ext_size[ext] += len(base64.b64decode(item["content_base64"]))

print(f"\n  File type breakdown:")
for ext in sorted(ext_counter.keys()):
    cnt = ext_counter[ext]
    sz = ext_size[ext]
    print(f"    {ext:10s}: {cnt:5,} files  ({sz/1024/1024:.1f} MB)")
