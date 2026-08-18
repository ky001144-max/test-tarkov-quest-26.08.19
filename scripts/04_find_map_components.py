import requests

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://api.github.com/repos/the-hideout/tarkov-dev/git/trees/main?recursive=1"
r = requests.get(url, headers=headers)
if r.status_code == 200:
    tree = r.json().get("tree", [])
    map_files = [f["path"] for f in tree if "map" in f["path"].lower() or "leaflet" in f["path"].lower() or "canvas" in f["path"].lower()]
    print("Map related files in tarkov-dev:")
    for mf in map_files:
        print("  -", mf)
