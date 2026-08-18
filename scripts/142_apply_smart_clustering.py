import json
import math
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Implementing Tarkov.dev Smart Multi-Spawn Clustering Engine ===")

# Load current raw tasks to inspect all zone and quest item multi-positions
with open("map_data/tarkov dev/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)["data"]["tasks"]

with open("app_v11/data/quests.json", "r", encoding="utf-8") as f:
    quests = json.load(f)

# Distance calculation in 3D world space (XZ plane)
def calc_distance(p1, p2):
    return math.sqrt((p1['x'] - p2['x'])**2 + (p1['z'] - p2['z'])**2)

# Cluster threshold: 25.0 meters (same room/building = cluster, distant spots = separate markers)
CLUSTER_THRESHOLD = 25.0

clustered_count = 0
separated_count = 0

# Check each quest in quests.json and enrich with raw multi-zone positions
for q in quests:
    q_id = q["id"]
    raw_q = raw_tasks.get(q_id)
    
    new_objectives = []
    
    for obj in q.get("objectives", []):
        # Check if this objective in raw_tasks has multiple zones
        raw_obj_zones = []
        if raw_q:
            for ro in raw_q.get("objectives", []):
                if ro.get("type") == obj.get("type"):
                    for z in ro.get("zones", []):
                        if z.get("position"):
                            raw_obj_zones.append({
                                "x": round(z["position"]["x"], 2),
                                "z": round(z["position"]["z"], 2),
                                "id": z.get("id", "")
                            })
                            
        # If we have multiple raw zone positions for this objective
        if len(raw_obj_zones) > 1:
            # Group positions into clusters within CLUSTER_THRESHOLD
            clusters = []
            for pos in raw_obj_zones:
                assigned = False
                for c in clusters:
                    # If within threshold of any point in cluster
                    if any(calc_distance(pos, member) <= CLUSTER_THRESHOLD for member in c["points"]):
                        c["points"].append(pos)
                        assigned = True
                        break
                if not assigned:
                    clusters.append({"points": [pos]})
                    
            # Process each cluster
            for c_idx, cluster in enumerate(clusters):
                pts = cluster["points"]
                if len(pts) == 1:
                    # Single distinct spawn
                    p = pts[0]
                    new_objectives.append({
                        **obj,
                        "id": f"{obj['id']}_{c_idx+1}",
                        "position": {"x": p["x"], "z": p["z"]},
                        "is_cluster": False,
                        "spawn_count": 1,
                        "hint": obj.get("hint") or f"스폰 위치 #{c_idx+1}"
                    })
                    separated_count += 1
                else:
                    # Multiple close spawns -> compute centroid (Center point)
                    avg_x = round(sum(p["x"] for p in pts) / len(pts), 2)
                    avg_z = round(sum(p["z"] for p in pts) / len(pts), 2)
                    
                    sub_hints = [f"후보 {i+1}: ({p['x']}, {p['z']})" for i, p in enumerate(pts)]
                    hint_text = f"📍 다중 스폰 반경 ({len(pts)}곳 집중 구역: {', '.join(sub_hints[:3])})"
                    
                    new_objectives.append({
                        **obj,
                        "id": f"{obj['id']}_cluster_{c_idx+1}",
                        "position": {"x": avg_x, "z": avg_z},
                        "is_cluster": True,
                        "spawn_count": len(pts),
                        "spawn_points": pts,
                        "hint": hint_text
                    })
                    clustered_count += 1
        else:
            new_objectives.append(obj)
            
    q["objectives"] = new_objectives
    q["has_position"] = any(bool(o.get("position")) for o in new_objectives)

# Save updated dataset to app_v11 and app
with open("app_v11/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

with open("app/data/quests.json", "w", encoding="utf-8") as f:
    json.dump(quests, f, indent=2, ensure_ascii=False)

print(f"=== Multi-Spawn Clustering Results ===")
print(f"  * Clustered Centroid Groups (within {CLUSTER_THRESHOLD}m): {clustered_count} groups")
print(f"  * Separated Distant Spawn Markers (> {CLUSTER_THRESHOLD}m): {separated_count} distinct markers")
print(f"  * Total Active Quests with Valid Positions: {sum(1 for q in quests if q.get('has_position'))}")
