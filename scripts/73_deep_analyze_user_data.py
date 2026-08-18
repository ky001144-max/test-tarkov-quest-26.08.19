import json

# Let's inspect maps_ko.txt and tasks_ko.txt
with open("map_data/maps_ko.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    tasks_raw = json.load(f)

print(f"=== Analysis of User Provided Data in map_data/ ===")
print(f"1. maps_ko.txt:")
print(f"   - Total Maps: {len(maps_raw)}")
for m in maps_raw:
    print(f"     * {m.get('name')} (normalizedName: {m.get('normalizedName')}) -> submaps: {len(m.get('maps', []))}")

print(f"\n2. tasks_ko.txt:")
print(f"   - Total Tasks: {len(tasks_raw)}")

# Count tasks per map and tasks with 3D zones/positions
map_task_counts = {}
tasks_with_positions = 0

for t in tasks_raw:
    t_map = t.get("map", {})
    m_name = t_map.get("name") if t_map else "Any / Multi"
    map_task_counts[m_name] = map_task_counts.get(m_name, 0) + 1
    
    has_pos = False
    for obj in t.get("objectives", []):
        zones = obj.get("zones", [])
        for z in zones:
            if z.get("position"):
                has_pos = True
                break
    if has_pos:
        tasks_with_positions += 1

print("\nTasks distribution by Map:")
for m_name, count in sorted(map_task_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"   * {m_name}: {count} tasks")

print(f"\nTasks with 3D Zones/Positions: {tasks_with_positions} / {len(tasks_raw)}")
