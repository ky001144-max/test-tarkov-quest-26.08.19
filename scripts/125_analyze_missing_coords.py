import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Analyzing Quest Datasets for Missing Objective Coordinates ===")

# 1. Check quest-data.json in tarkov-data-manager
qdm_path = "tarkov-data-manager-main/src/tarkov-data-manager/public/data/quest-data.json"
if os.path.exists(qdm_path):
    with open(qdm_path, "r", encoding="utf-8") as f:
        qdm = json.load(f)
    print(f"Loaded quest-data.json: {len(qdm)} quests")
    # Inspect sample
    if isinstance(qdm, list) and len(qdm) > 0:
        sample = qdm[0]
        print("Sample keys in quest-data.json:", list(sample.keys()))
        for o in sample.get("objectives", []):
            print("  -", o)
    elif isinstance(qdm, dict):
        print("Keys:", list(qdm.keys())[:10])

# 2. Check tracker_quests_json.json in primary_data
tr_path = "primary_data/tracker_quests_json.json"
if os.path.exists(tr_path):
    with open(tr_path, "r", encoding="utf-8") as f:
        tr = json.load(f)
    print(f"Loaded tracker_quests_json.json: {len(tr)} quests")
    if isinstance(tr, list) and len(tr) > 0:
        print("Sample keys in tracker_quests_json.json:", list(tr[0].keys()))
        for o in tr[0].get("objectives", []):
            print("  -", o)

# 3. Check current app_v11/data/quests.json
v11_path = "app_v11/data/quests.json"
with open(v11_path, "r", encoding="utf-8") as f:
    v11_quests = json.load(f)

total_objectives = sum(len(q.get("objectives", [])) for q in v11_quests)
objectives_with_pos = sum(sum(1 for o in q.get("objectives", []) if o.get("position")) for q in v11_quests)
quests_with_pos = sum(1 for q in v11_quests if q.get("has_position"))

print(f"\nCurrent app_v11 Stats:")
print(f"  * Total Quests: {len(v11_quests)}")
print(f"  * Quests with Position: {quests_with_pos} / {len(v11_quests)} ({quests_with_pos/len(v11_quests)*100:.1f}%)")
print(f"  * Total Objectives: {total_objectives}")
print(f"  * Objectives with Position: {objectives_with_pos} / {total_objectives} ({objectives_with_pos/total_objectives*100:.1f}%)")
