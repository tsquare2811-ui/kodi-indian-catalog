#!/data/data/com.termux/files/usr/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: bash ~/kodi-repo/release.sh 0.1.0"
  exit 1
fi
cd ~/kodi-addon/plugin.video.indiancatalog
sed -i "/<addon /s/version=\"[^\"]*\"/version=\"$1\"/" addon.xml
grep -n "<addon " addon.xml
cd ~/kodi-repo
python3 build.py
git add -A
git commit -m "Release $1"
git push
echo "RELEASED $1"
