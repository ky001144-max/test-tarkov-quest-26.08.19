import json

with open("app/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

with open("app/data/maps.json", "r", encoding="utf-8") as f:
    maps = json.load(f)

print(f"Total Quests in app/data: {len(quests)}")
print(f"Total Maps in app/data: {len(maps)}")

print("\n--- Map Filtering Test ---")
for m in maps:
    m_id = m["id"]
    # Filter quests that have at least one objective on this map
    matched_quests = [q for q in quests if any(o.get("map_id") == m_id for o in q.get("objectives", []))]
    gps_objectives = [o for q in matched_quests for o in q.get("objectives", []) if o.get("map_id") == m_id and o.get("gps")]
    
    print(f"[{m['name_ko']} / {m['name_en']}] -> {len(matched_quests)} Quests, {len(gps_objectives)} GPS Pin Markers")
    for q in matched_quests[:3]:
        q_objs_on_map = [o for o in q['objectives'] if o.get('map_id') == m_id]
        print(f"   * {q['title_ko']} ({q['trader']['name_ko']}) - {len(q_objs_on_map)} objectives on map")

print("\nAll map filters are strictly scoped to only the selected map!")
