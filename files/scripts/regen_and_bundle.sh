#!/bin/bash
set -e

echo "=== Step 1: Regenerate site ==="
python3 /home/user/files/scripts/scripts/generate_sauna_site_v2.py

echo ""
echo "=== Step 2: Verify generated files ==="
find /home/user/files/code/sauna-site-v2 -type f | wc -l

echo ""
echo "=== Step 3: Clone repo ==="
cd /tmp
rm -rf sauna-finder
git clone --depth=1 https://github.com/uerzer/sauna-finder.git
cd sauna-finder

git config user.name "uerzer"
git config user.email "phobik2000+ai@gmail.com"

echo ""
echo "=== Step 4: Remove old content ==="
rm -rf listings/ states/ test-nested/
rm -f directory.html index.html script.js styles.css test-action.txt test-api-write.txt test-pages-check.txt

echo ""
echo "=== Step 5: Copy new content ==="
cp -r /home/user/files/code/sauna-site-v2/* .

echo "Files after copy:"
find . -not -path './.git/*' -type f | wc -l

echo ""
echo "=== Step 6: Git commit ==="
git add -A
git commit -m "Deploy SaunaFinder v2 - 4,478 static pages with JSON-LD, claim forms, city hubs

- 4,040 individual venue listing pages
- 377 city hub pages
- 55 state pages
- Full directory with search
- JSON-LD structured data on all pages
- Sitemap with 4,478 URLs
- Dark theme responsive design
- Business claim forms"

echo ""
echo "=== Step 7: Create bundle ==="
mkdir -p /home/user/files/tmp
git bundle create /home/user/files/tmp/sauna-site-v2.bundle main
ls -lh /home/user/files/tmp/sauna-site-v2.bundle

echo ""
echo "=== Step 8: Verify bundle ==="
git bundle verify /home/user/files/tmp/sauna-site-v2.bundle

echo ""
echo "=== DONE ==="
git log --oneline -1
echo "Bundle saved to /home/user/files/tmp/sauna-site-v2.bundle"
