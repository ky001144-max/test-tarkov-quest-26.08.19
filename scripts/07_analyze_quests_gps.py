import json

with open("primary_data/tracker_quests_json.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

with open("primary_data/tracker_maps_json.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

with open("primary_data/traders.json", "r", encoding="utf-8") as f:
    traders = json.load(f)

print(f"Total Quests: {len(quests)}")
print(f"Total Maps in tracker_maps_json: {len(maps_data)}")
print(f"Traders type: {type(traders)}")
if isinstance(traders, dict):
    print("Trader keys:", list(traders.keys()))
    trader_id_to_name = {v.get("id", k): v.get("name", k) if isinstance(v, dict) else v for k, v in traders.items()}
elif isinstance(traders, list):
    trader_id_to_name = {t["id"]: t["name"] if isinstance(t, dict) else t for t in traders}
else:
    trader_id_to_name = {}

map_id_to_name = {v["id"]: k for k, v in maps_data.items() if "id" in v}
print("\nMap ID mapping:", map_id_to_name)
print("\nTrader ID mapping:", trader_id_to_name)

quests_with_gps = 0
total_objectives = 0
objectives_with_gps = 0
gps_samples = []

for q in quests:
    has_gps = False
    for obj in q.get("objectives", []):
        total_objectives += 1
        if "gps" in obj and obj["gps"]:
            has_gps = True
            objectives_with_gps += 1
            if len(gps_samples) < 8:
                gps_samples.append({
                    "quest": q.get("title"),
                    "trader": trader_id_to_name.get(q.get("giver"), q.get("giver")),
                    "objective_type": obj.get("type"),
                    "target": obj.get("target"),
                    "location_id": obj.get("location"),
                    "map_name": map_id_to_name.get(obj.get("location")),
                    "gps": obj["gps"]
                })
    if has_gps:
        quests_with_gps += 1

print(f"\nQuests with GPS: {quests_with_gps} / {len(quests)}")
print(f"Objectives with GPS: {objectives_with_gps} / {total_objectives}")

print("\nGPS Samples:")
for s in gps_samples:
    print(json.dumps(s, indent=2, ensure_ascii=False))
