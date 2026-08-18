import json

with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Inspect Customs Checking, Delivery from the past, BP depot
print("Customs Key Quests GPS Check:")
for q in quests:
    for obj in q['objectives']:
        if obj.get("map_id") == "customs" and obj.get("gps"):
            gps = obj['gps']
            print(f"  * [{q['trader']['name_ko']}] {q['title_ko']} -> left: {gps['leftPercent']}%, top: {gps['topPercent']}%, svg: ({gps.get('svgX')}, {gps.get('svgY')}) | {obj.get('hint')}")
