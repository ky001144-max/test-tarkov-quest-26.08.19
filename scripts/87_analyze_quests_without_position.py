import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

print(f"=== Analysis of Quests without Position Data ===")
print(f"Total Quests in tasks.txt: {len(tasks_dict)}")

# Group objectives by type and check if they have zones or not
obj_type_stats = {}
no_pos_reasons = {
    "kill_quests": [], # e.g., Kill 15 Scavs on Woods, Kill PMCs
    "find_or_handover_items": [], # e.g., Hand over 3 Salewa kits, find 60-round mags
    "skill_or_level": [], # e.g., Reach Level 15, raise Sniper skill to level 3
    "general_extract": [], # e.g., Survive and extract from Customs
    "quest_item_without_zone": [], # Quest items where position is in questItems or wiki only
    "other": []
}

for q_id, q in tasks_dict.items():
    raw_name_key = f"{q_id} name"
    name_ko = i18n.get(raw_name_key) or i18n.get(f"{q_id} Name") or q.get("name") or "이름 없음"
    
    has_pos = False
    for o in q.get("objectives", []):
        otype = o.get("type", "unknown")
        has_zone = bool(o.get("zones"))
        
        if otype not in obj_type_stats:
            obj_type_stats[otype] = {"total": 0, "with_zones": 0, "without_zones": 0}
        obj_type_stats[otype]["total"] += 1
        if has_zone:
            obj_type_stats[otype]["with_zones"] += 1
            has_pos = True
        else:
            obj_type_stats[otype]["without_zones"] += 1
            
    if not has_pos:
        # Categorize why this quest has no position
        types_in_q = [o.get("type") for o in q.get("objectives", [])]
        if any(t in ["shoot", "kill"] for t in types_in_q):
            no_pos_reasons["kill_quests"].append((name_ko, types_in_q))
        elif any(t in ["giveItem", "findItem", "handover"] for t in types_in_q):
            no_pos_reasons["find_or_handover_items"].append((name_ko, types_in_q))
        elif any(t in ["skill", "level"] for t in types_in_q):
            no_pos_reasons["skill_or_level"].append((name_ko, types_in_q))
        elif any(t in ["extract"] for t in types_in_q):
            no_pos_reasons["general_extract"].append((name_ko, types_in_q))
        else:
            no_pos_reasons["other"].append((name_ko, types_in_q))

print("\n--- Objective Types in tarkov.dev raw tasks.txt ---")
for otype, stats in sorted(obj_type_stats.items(), key=lambda x: x[1]["total"], reverse=True):
    print(f"  * Type [{otype:15s}]: Total {stats['total']:4d} | With 3D Position: {stats['with_zones']:3d} | Without Position: {stats['without_zones']:4d}")

print(f"\n--- Quests without Position Breakdown (Total {sum(len(v) for v in no_pos_reasons.values())} quests) ---")
print(f"1. 단순 아이템 수집/전달 퀘스트 (Salewa 3개, 가스마스크 등 - 고정 위치 없음): {len(no_pos_reasons['find_or_handover_items'])}개")
print(f"   예시: {[x[0] for x in no_pos_reasons['find_or_handover_items'][:5]]}")

print(f"\n2. 적/스캐브/보스 처치 퀘스트 (스캐브 15명 처치, 야간 처치 등 - 고정 점이 아닌 맵 전역): {len(no_pos_reasons['kill_quests'])}개")
print(f"   예시: {[x[0] for x in no_pos_reasons['kill_quests'][:5]]}")

print(f"\n3. 단순 생존 탈출 퀘스트: {len(no_pos_reasons['general_extract'])}개")
print(f"   예시: {[x[0] for x in no_pos_reasons['general_extract'][:5]]}")

print(f"\n4. 스킬/레벨 달성 퀘스트: {len(no_pos_reasons['skill_or_level'])}개")
print(f"   예시: {[x[0] for x in no_pos_reasons['skill_or_level'][:5]]}")

print(f"\n5. 기타 특정 목표 퀘스트: {len(no_pos_reasons['other'])}개")
print(f"   예시: {[x[0] for x in no_pos_reasons['other'][:5]]}")
