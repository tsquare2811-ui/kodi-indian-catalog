import hashlib
import os
import re
import shutil
import zipfile

HOME = os.path.expanduser("~")
REPO = os.path.join(HOME, "kodi-repo")
ADDONS = [
    os.path.join(HOME, "kodi-addon", "plugin.video.indiancatalog"),
    os.path.join(REPO, "repository.indiancatalog"),
]


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def version_of(addon_dir):
    text = read(os.path.join(addon_dir, "addon.xml"))
    return re.search(r'<addon[^>]*\sversion="([^"]+)"', text).group(1)


def make_zip(addon_dir):
    aid = os.path.basename(addon_dir)
    out_dir = os.path.join(REPO, "zips", aid)
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "%s-%s.zip" % (aid, version_of(addon_dir)))
    base = os.path.dirname(addon_dir)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(addon_dir):
            dirs[:] = [d for d in dirs if d != "__pycache__"]
            for name in files:
                if name.endswith(".pyc") or name.endswith(".bak"):
                    continue
                full = os.path.join(root, name)
                z.write(full, os.path.relpath(full, base))
    for art in ("icon.png", "fanart.png"):
        src = os.path.join(addon_dir, art)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(out_dir, art))
    print("zip: " + out)


parts = []
for d in ADDONS:
    make_zip(d)
    text = read(os.path.join(d, "addon.xml")).strip()
    parts.append(re.sub(r"^<\?xml[^>]*\?>\s*", "", text))

xml = '<?xml version="1.0" encoding="UTF-8"?>\n<addons>\n' + "\n".join(parts) + "\n</addons>\n"
with open(os.path.join(REPO, "addons.xml"), "w", encoding="utf-8") as f:
    f.write(xml)
md5 = hashlib.md5(xml.encode("utf-8")).hexdigest()
with open(os.path.join(REPO, "addons.xml.md5"), "w") as f:
    f.write(md5)
print("addons.xml md5: " + md5)
