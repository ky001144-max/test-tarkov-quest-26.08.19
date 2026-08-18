import requests
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://api.github.com/repos/the-hideout/tarkov-dev/git/trees/main?recursive=1"
r = requests.get(url, headers=headers)
if r.status_code == 200:
    tree = r.json().get("tree", [])
    loc_files = [f["path"] for f in tree if "ko" in f["path"].lower() or "locale" in f["path"].lower() or "translations" in f["path"].lower()]
    print("Locale files in tarkov-dev:")
    for lf in loc_files:
        print("  -", lf)
else:
    print(f"Failed to fetch tree: {r.status_code}")
