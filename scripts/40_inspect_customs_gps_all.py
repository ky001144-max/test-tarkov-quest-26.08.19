import json

with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Let's inspect all customs quests with GPS and their exact targets
customs_quests = [q for q in quests if any(o.get("map_id") == "customs" and o.get("gps") for o in q.get("objectives", []))]

print(f"Customs Quests with GPS ({len(customs_quests)}):")
for q in customs_quests:
    print(f"\n[{q['trader']['name_ko']}] {q['title_ko']} ({q['title_en']})")
    for o in q['objectives']:
        if o.get("map_id") == "customs" and o.get("gps"):
            gps = o['gps']
            print(f"   * Obj #{o['id']}: [{o['type']}] {o['target']} -> left: {gps.get('leftPercent')}%, top: {gps.get('topPercent')}%, floor: {gps.get('floor')}")
