import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Inspect Tigr Safari in both versions
with open("app_v10/data/quests.json", "r", encoding="utf-8") as f:
    v10 = json.load(f)

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    v11 = json.load(f)

print(f"=== Verification of v1.10 and v1.11 ===")
print(f"v1.10 Total Quests: {len(v10)}")
print(f"v1.11 Total Quests: {len(v11)}")

v10_tigr = [q for q in v10 if "Tigr" in q["title_ko"] or "사파리" in q["title_ko"]]
v11_tigr = [q for q in v11 if "Tigr" in q["title_ko"] or "사파리" in q["title_ko"]]

print(f"\nv1.10 Tigr Safari: {len(v10_tigr)} found")
if v10_tigr:
    t = v10_tigr[0]
    print(f"  Title: {t['title_ko']} | Trader: {t['trader']['name_ko']} (id: {t['trader']['id']})")
    print(f"  Objectives ({len(t['objectives'])}):")
    for o in t['objectives']:
        print(f"    * {o['description_ko']} -> pos: {o.get('position')} ({o.get('hint')})")

print(f"\nv1.11 Tigr Safari: {len(v11_tigr)} found")
if v11_tigr:
    t = v11_tigr[0]
    print(f"  Title: {t['title_ko']} | Trader: {t['trader']['name_ko']}")
    print(f"  Objectives ({len(t['objectives'])}):")
    for o in t['objectives']:
        print(f"    * {o['description_ko']} -> pos: {o.get('position')} ({o.get('hint')})")
