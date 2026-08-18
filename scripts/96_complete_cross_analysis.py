import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def normalize_name(name):
    if not name:
        return ""
    s = name.lower().strip()
    s = re.sub(r'[\(\)\-\–\—\:\,\.\'\"]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# 1. PARSE WIKI QUESTS
with open("primary_data/wiki_quests_page.html", "r", encoding="utf-8") as f:
    wiki_html = f.read()

wiki_soup = BeautifulSoup(wiki_html, 'html.parser')

wiki_all_quests = {}
wiki_customs_quests = {}

tables = wiki_soup.find_all('table', class_='wikitable')
print(f"Found {len(tables)} Wikitables.")

for t in tables:
    rows = t.find_all('tr')
    for r in rows:
        cols = r.find_all(['td', 'th'])
        if len(cols) >= 3:
            # Check col 1 for quest link
            q_link = cols[1].find('a') if len(cols) > 1 else None
            if q_link:
                q_name = q_link.get_text().strip()
                if q_name and not q_name.startswith("File:"):
                    norm = normalize_name(q_name)
                    wiki_all_quests[norm] = q_name
                    
                    # Check objectives in col 2 or whole row for "Customs"
                    obj_text = cols[2].get_text() if len(cols) > 2 else ""
                    if "customs" in obj_text.lower() or "customs" in r.get_text().lower():
                        wiki_customs_quests[norm] = {
                            "name": q_name,
                            "objectives_snippet": obj_text.strip()[:100]
                        }

print(f"Wiki Total Quests: {len(wiki_all_quests)}")
print(f"Wiki Customs Quests: {len(wiki_customs_quests)}")

# 2. PARSE TARKOV.DEV QUESTS
with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    td_raw = json.load(f)

td_tasks = td_raw["data"]["tasks"]
CUSTOMS_HASH = "56f40101d2720b2a4d8b45d6"

td_all_quests = {}
td_customs_quests = {}

for q_id, q in td_tasks.items():
    name_en = q.get("name", "")
    norm = normalize_name(name_en)
    if norm:
        td_all_quests[norm] = name_en
        
        is_customs = q.get("map") == CUSTOMS_HASH
        if not is_customs:
            for o in q.get("objectives", []):
                if any(z.get("map") == CUSTOMS_HASH for z in o.get("zones", [])):
                    is_customs = True
                    break
                if any(m == CUSTOMS_HASH for m in o.get("maps", [])):
                    is_customs = True
                    break
        if is_customs:
            td_customs_quests[norm] = name_en

print(f"Tarkov.dev Total Quests: {len(td_all_quests)}")
print(f"Tarkov.dev Customs Quests: {len(td_customs_quests)}")

# 3. PARSE TARKOV-MARKET CUSTOMS QUESTS
# Tarkov-market customs map pins
with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

market_customs_quests = {}

# Check all wiki customs quests against market page content
for norm, info in wiki_customs_quests.items():
    qname = info["name"]
    # Look for exact or normalized occurrence
    if qname.lower() in market_html.lower() or norm in normalize_name(market_html):
        market_customs_quests[norm] = qname

print(f"Tarkov-Market Customs Quests found on map: {len(market_customs_quests)}")

# 4. STATISTICAL MATCHING & OVERLAP
td_in_wiki = set(td_customs_quests.keys()).intersection(set(wiki_customs_quests.keys()))
market_in_wiki = set(market_customs_quests.keys()).intersection(set(wiki_customs_quests.keys()))

print("\n=======================================================")
print("          FINAL SCIENTIFIC OVERLAP ANALYSIS            ")
print("=======================================================")
print(f"1. [Tarkov.dev vs Wiki 세관 퀘스트]")
print(f"   - Wiki 세관 퀘스트 총 개수: {len(wiki_customs_quests)}개")
print(f"   - Tarkov.dev 세관 퀘스트 총 개수: {len(td_customs_quests)}개")
print(f"   - 일치(Overlap)하는 퀘스트 개수: {len(td_in_wiki)}개")
print(f"   - 일치율: {len(td_in_wiki) / len(wiki_customs_quests) * 100:.1f}%")

print(f"\n2. [Tarkov-Market vs Wiki 세관 퀘스트]")
print(f"   - Wiki 세관 퀘스트 총 개수: {len(wiki_customs_quests)}개")
print(f"   - Tarkov-Market 세관 퀘스트 총 개수: {len(market_customs_quests)}개")
print(f"   - 일치(Overlap)하는 퀘스트 개수: {len(market_in_wiki)}개")
print(f"   - 일치율: {len(market_in_wiki) / len(wiki_customs_quests) * 100:.1f}%")

print(f"\n--- Tarkov.dev & Wiki 겹치는 세관 퀘스트 목록 ({len(td_in_wiki)}개) ---")
for idx, k in enumerate(sorted(td_in_wiki)):
    print(f"  {idx+1:2d}. {wiki_customs_quests[k]['name']}")

print(f"\n--- Tarkov-Market & Wiki 겹치는 세관 퀘스트 목록 ({len(market_in_wiki)}개) ---")
for idx, k in enumerate(sorted(market_in_wiki)):
    print(f"  {idx+1:2d}. {wiki_customs_quests[k]['name']}")

# Save detailed artifact
analysis_result = {
    "wiki_total": len(wiki_all_quests),
    "wiki_customs_total": len(wiki_customs_quests),
    "tarkov_dev_customs_total": len(td_customs_quests),
    "tarkov_dev_wiki_overlap_count": len(td_in_wiki),
    "tarkov_dev_wiki_overlap_percentage": round(len(td_in_wiki) / len(wiki_customs_quests) * 100, 1),
    "market_customs_total": len(market_customs_quests),
    "market_wiki_overlap_count": len(market_in_wiki),
    "market_wiki_overlap_percentage": round(len(market_in_wiki) / len(wiki_customs_quests) * 100, 1),
    "tarkov_dev_overlapping_quests": [wiki_customs_quests[k]["name"] for k in sorted(td_in_wiki)],
    "market_overlapping_quests": [wiki_customs_quests[k]["name"] for k in sorted(market_in_wiki)]
}

with open("intermediate_results/customs_quests_cross_analysis.json", "w", encoding="utf-8") as f:
    json.dump(analysis_result, f, indent=2, ensure_ascii=False)
