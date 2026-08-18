import requests
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://api.github.com/repos/TarkovTracker/tarkovtracker/git/trees/master?recursive=1"
r = requests.get(url, headers=headers)
if r.status_code == 200:
    tree = r.json().get("tree", [])
    print("Files in TarkovTracker:")
    for f in tree:
        if any(k in f["path"].lower() for k in ["map", "quest", "marker", "svg"]):
            print("  -", f["path"])
else:
    print("Tree status:", r.status_code)
