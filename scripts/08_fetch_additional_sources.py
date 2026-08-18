import requests
import json

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://raw.githubusercontent.com/Zeliper/Tarkov-Item-Helper/main/TarkovDBEditor/Additional/tarkov_data.db"
# Let's check what other json files Zeliper has
urls = [
    ("zeliper_tasks_json", "https://raw.githubusercontent.com/Zeliper/Tarkov-Item-Helper/main/src/data/tasks.json"),
    ("tarkov_changes_quests", "https://raw.githubusercontent.com/tarkov-changes/data/master/quests.json"),
    ("tarkov_tools_quests", "https://raw.githubusercontent.com/kokarn/tarkov-tools/master/src/data/quests.json"),
]

for name, u in urls:
    r = requests.get(u, headers=headers)
    print(f"{name}: status {r.status_code}")
    if r.status_code == 200:
        with open(f"primary_data/{name}.json", "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"  Saved {len(r.text)} bytes")
