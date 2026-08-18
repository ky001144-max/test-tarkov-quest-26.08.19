import json

with open("map_data/maps_ko.txt", "r", encoding="utf-8") as f:
    maps_raw = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    tasks_raw = json.load(f)

print("maps_ko type:", type(maps_raw))
if isinstance(maps_raw, dict):
    print("maps_ko keys:", list(maps_raw.keys())[:15])
    print("maps_ko sample key-value:", list(maps_raw.items())[:3])
elif isinstance(maps_raw, list):
    print("maps_ko items:", len(maps_raw), maps_raw[:3])

print("\ntasks_ko type:", type(tasks_raw))
if isinstance(tasks_raw, dict):
    print("tasks_ko keys:", list(tasks_raw.keys())[:15])
    print("tasks_ko sample key-value:", list(tasks_raw.items())[:3])
elif isinstance(tasks_raw, list):
    print("tasks_ko items:", len(tasks_raw), tasks_raw[:3])
