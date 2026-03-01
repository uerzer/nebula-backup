
# Read all files and output their full content for pushing to GitHub
import os

channels = ["hf", "crypto", "internal-self-improvement", "memory", "gsd"]
results = {}

for ch in channels:
    results[ch] = {}
    for fname in ["conversation.md", "manifest.json"]:
        path = f"/tmp/nebula-backup/{ch}/{fname}"
        if os.path.exists(path):
            with open(path, "r") as f:
                results[ch][fname] = f.read()
        else:
            results[ch][fname] = None

# Output sizes
for ch in channels:
    for fname in ["conversation.md", "manifest.json"]:
        content = results[ch][fname]
        if content:
            print(f"{ch}/{fname}: {len(content)} chars - OK")
        else:
            print(f"{ch}/{fname}: MISSING")
