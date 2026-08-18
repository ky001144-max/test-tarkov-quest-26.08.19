import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ----------------------------------------------------------------------
# 1. WIKI QUESTS EXHAUSTIVE BREAKDOWN (From primary_data/wiki_quests_page.html)
# ----------------------------------------------------------------------
with open("primary_data/wiki_quests_page.html", "r", encoding="utf-8") as f:
    wiki_html = f.read()

wiki_soup = BeautifulSoup(wiki_html, 'html.parser')

# Map of Trader Name -> List of Quests
wiki_trader_quests = {}
wiki_customs_exclusive = []  # Only mentions Customs
wiki_customs_multi = []      # Mentions Customs along with other maps or 'Any'
wiki_customs_all = []

tables = wiki_soup.find_all('table', class_='wikitable')

# Also find trader tabs
trader_names = ["Prapor", "Therapist", "Fence", "Skier", "Peacekeeper", "Mechanic", "Ragman", "Jaeger", "Ref", "Lightkeeper", "BTR Driver"]

for t_idx, t in enumerate(tables):
    rows = t.find_all('tr')
    # Try to identify trader
    trader_name = trader_names[t_idx] if t_idx < len(trader_names) else f"Trader_{t_idx}"
    wiki_trader_quests[trader_name] = []
    
    for r in rows[1:]:
        cols = r.find_all(['td', 'th'])
        if len(cols) >= 3:
            q_link = cols[1].find('a')
            if q_link:
                q_name = q_link.get_text().strip()
                if q_name and not q_name.startswith("File:"):
                    obj_text = cols[2].get_text()
                    full_text = r.get_text()
                    
                    is_customs_exclusive = False
                    is_customs_multi = False
                    
                    if "customs" in obj_text.lower() or "customs" in full_text.lower():
                        # Check if other maps are also mentioned
                        other_maps = [m for m in ["woods", "factory", "shoreline", "interchange", "reserve", "lighthouse", "streets", "ground zero", "labs"] if m in obj_text.lower()]
                        if len(other_maps) == 0 and "any" not in obj_text.lower():
                            is_customs_exclusive = True
                            wiki_customs_exclusive.append((trader_name, q_name, obj_text.strip()[:60]))
                        else:
                            is_customs_multi = True
                            wiki_customs_multi.append((trader_name, q_name, obj_text.strip()[:60]))
                        wiki_customs_all.append((trader_name, q_name))
                        
                    wiki_trader_quests[trader_name].append(q_name)

print("=== 1. WIKI QUESTS EXHAUSTIVE STATS ===")
total_wiki = sum(len(v) for v in wiki_trader_quests.values())
print(f"Total Quests on Wiki across all traders: {total_wiki} quests")
for tname, qlist in wiki_trader_quests.items():
    c_count = sum(1 for q in qlist if any(q == item[1] for item in wiki_customs_all))
    print(f"  * {tname:15s}: {len(qlist):3d} total | {c_count:2d} related to Customs")

print(f"\nWiki Customs Breakdown:")
print(f"  - 세관 전용 (Customs Only): {len(wiki_customs_exclusive)}개")
print(f"  - 세관 포함 다중 맵/선택 (Customs + Other Maps): {len(wiki_customs_multi)}개")
print(f"  - 세관 관련 전체 (Total Customs Related): {len(wiki_customs_all)}개")


# ----------------------------------------------------------------------
# 2. TARKOV.DEV QUESTS EXHAUSTIVE BREAKDOWN (From map_data/tasks.txt)
# ----------------------------------------------------------------------
with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    td_raw = json.load(f)

td_tasks = td_raw["data"]["tasks"]
CUSTOMS_HASH = "56f40101d2720b2a4d8b45d6"

td_customs_only = []
td_customs_with_zones = []
td_customs_all_related = []

for q_id, q in td_tasks.items():
    name = q.get("wikiLink", "").split("/wiki/")[-1] if q.get("wikiLink") else q.get("name", "")
    name = re.sub(r'[\_]', ' ', name)
    
    is_main_customs = q.get("map") == CUSTOMS_HASH
    has_customs_zone = any(any(z.get("map") == CUSTOMS_HASH for z in o.get("zones", [])) for o in q.get("objectives", []))
    has_customs_map_obj = any(any(m == CUSTOMS_HASH for m in o.get("maps", [])) for o in q.get("objectives", []))
    
    if is_main_customs and not any(o.get("maps") and any(m != CUSTOMS_HASH for m in o.get("maps")) for o in q.get("objectives", [])):
        td_customs_only.append((q_id, name))
    
    if has_customs_zone:
        td_customs_with_zones.append((q_id, name))
        
    if is_main_customs or has_customs_zone or has_customs_map_obj:
        td_customs_all_related.append((q_id, name))

print("\n=== 2. TARKOV.DEV QUESTS EXHAUSTIVE STATS ===")
print(f"Total Quests in Tarkov.dev: {len(td_tasks)} quests")
print(f"  - 세관이 주 맵(Main Map)인 퀘스트: {len(td_customs_only)}개")
print(f"  - 실제 지도에 3D 핀(Zone/Marker)이 찍히는 퀘스트: {len(td_customs_with_zones)}개")
print(f"  - 세관 관련 전체(주맵 + 목표맵 + 존 포함): {len(td_customs_all_related)}개")

# ----------------------------------------------------------------------
# 3. SAVE COMPLETE LISTINGS FOR COMPARISON
# ----------------------------------------------------------------------
save_data = {
    "wiki_customs_exclusive": [f"[{t}] {q}" for t, q, _ in wiki_customs_exclusive],
    "wiki_customs_multi": [f"[{t}] {q}" for t, q, _ in wiki_customs_multi],
    "td_customs_with_markers": [name for _, name in td_customs_with_zones],
    "td_customs_all": [name for _, name in td_customs_all_related]
}

with open("intermediate_results/exhaustive_customs_breakdown.json", "w", encoding="utf-8") as f:
    json.dump(save_data, f, indent=2, ensure_ascii=False)

print("\nSaved breakdown to intermediate_results/exhaustive_customs_breakdown.json")
