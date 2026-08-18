import json
import re
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Normalize strings for robust matching (lowercase, strip special chars)
def normalize_name(name):
    if not name:
        return ""
    # remove parenthesis, hyphens, extra whitespace, roman numerals/parts standardizing
    s = name.lower().strip()
    s = re.sub(r'[\(\)\-\–\—\:\,\.\'\"]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# ----------------------------------------------------
# 1. PARSE WIKI QUESTS (Fandom Wiki)
# ----------------------------------------------------
with open("primary_data/wiki_quests_page.html", "r", encoding="utf-8") as f:
    wiki_html = f.read()

wiki_soup = BeautifulSoup(wiki_html, 'html.parser')

wiki_quests_all = {}
wiki_customs_quests = {}

# Find trader tables
trader_sections = wiki_soup.find_all(['h2', 'h3'])
tables = wiki_soup.find_all('table', class_='wikitable')

print(f"Parsing {len(tables)} Wiki Tables...")

for t in tables:
    rows = t.find_all('tr')
    headers = [th.get_text().strip().lower() for th in rows[0].find_all(['th', 'td'])] if rows else []
    
    # Locate Quest Name and Location columns
    name_col = 0
    loc_col = -1
    for idx, h in enumerate(headers):
        if "quest" in h or "task" in h or "name" in h:
            name_col = idx
        if "location" in h or "map" in h:
            loc_col = idx
            
    for r in rows[1:]:
        cols = r.find_all(['td', 'th'])
        if len(cols) > name_col:
            q_link = cols[name_col].find('a')
            q_name = q_link.get_text().strip() if q_link else cols[name_col].get_text().strip()
            
            # Location text
            loc_text = cols[loc_col].get_text().strip() if loc_col >= 0 and len(cols) > loc_col else r.get_text()
            
            if q_name and not q_name.startswith("File:") and len(q_name) > 1:
                norm = normalize_name(q_name)
                wiki_quests_all[norm] = q_name
                
                # Check if customs is listed in location
                if "customs" in loc_text.lower() or "any" in loc_text.lower() or loc_col == -1:
                    # Specific customs check
                    if "customs" in loc_text.lower():
                        wiki_customs_quests[norm] = {
                            "original_name": q_name,
                            "location": loc_text
                        }

print(f"-> Wiki Total Quests Parsed: {len(wiki_quests_all)}")
print(f"-> Wiki Customs-Specific Quests Parsed: {len(wiki_customs_quests)}")

# ----------------------------------------------------
# 2. PARSE TARKOV.DEV QUESTS
# ----------------------------------------------------
with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    tarkov_dev_raw = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tarkov_dev_tasks = tarkov_dev_raw["data"]["tasks"]
CUSTOMS_HASH = "56f40101d2720b2a4d8b45d6"

tarkov_dev_customs = {}
tarkov_dev_all = {}

for q_id, q in tarkov_dev_tasks.items():
    name_en = q.get("name", "")
    norm = normalize_name(name_en)
    name_ko = i18n.get(f"{q_id} name") or i18n.get(f"{q_id} Name") or name_en
    
    tarkov_dev_all[norm] = {"id": q_id, "name_en": name_en, "name_ko": name_ko}
    
    is_customs = False
    if q.get("map") == CUSTOMS_HASH:
        is_customs = True
    else:
        for o in q.get("objectives", []):
            if any(z.get("map") == CUSTOMS_HASH for z in o.get("zones", [])):
                is_customs = True
                break
            if any(m == CUSTOMS_HASH for m in o.get("maps", [])):
                is_customs = True
                break
                
    if is_customs:
        tarkov_dev_customs[norm] = {"id": q_id, "name_en": name_en, "name_ko": name_ko}

print(f"-> Tarkov.dev Total Quests: {len(tarkov_dev_all)}")
print(f"-> Tarkov.dev Customs Quests: {len(tarkov_dev_customs)}")

# ----------------------------------------------------
# 3. PARSE TARKOV-MARKET QUESTS
# ----------------------------------------------------
with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

market_soup = BeautifulSoup(market_html, 'html.parser')
market_customs = {}

# Check for JSON objects or marker lists inside scripts / DOM
script_matches = re.findall(r'(\{[^{}]*"name"[^{}]*"quest"[^{}]*\})', market_html, re.IGNORECASE)
quest_names_found = set()

# Search for quest mentions in HTML text
for text in market_soup.stripped_strings:
    # Common Tarkov quests
    norm = normalize_name(text)
    if norm in wiki_quests_all or norm in tarkov_dev_all:
        quest_names_found.add(norm)

# Also regex search for task patterns in embedded JS
embedded_json_match = re.findall(r'\"task\"\:\"([^\"]+)\"', market_html)
for m in embedded_json_match:
    quest_names_found.add(normalize_name(m))
    
embedded_quest_match = re.findall(r'\"quest\"\:\"([^\"]+)\"', market_html)
for m in embedded_quest_match:
    quest_names_found.add(normalize_name(m))

for norm in quest_names_found:
    market_customs[norm] = norm

print(f"-> Tarkov-Market Customs Quests Identified: {len(market_customs)}")

# ----------------------------------------------------
# 4. CROSS MATCHING & STATISTICAL OVERLAP ANALYSIS
# ----------------------------------------------------
# A. Tarkov.dev Customs vs Wiki Customs
tarkov_dev_in_wiki = {k: v for k, v in tarkov_dev_customs.items() if k in wiki_customs_quests or k in wiki_quests_all}
wiki_in_tarkov_dev = {k: v for k, v in wiki_customs_quests.items() if k in tarkov_dev_customs or k in tarkov_dev_all}

# B. Tarkov-Market Customs vs Wiki Customs
market_in_wiki = {k: v for k, v in market_customs.items() if k in wiki_customs_quests or k in wiki_quests_all}

print("\n=======================================================")
print("          SCIENTIFIC CROSS-MATCHING REPORT             ")
print("=======================================================")

print(f"\n1. [Tarkov.dev vs Wiki] 세관(Customs) 퀘스트 일치 분석:")
print(f"   - Tarkov.dev 세관 퀘스트 총 개수: {len(tarkov_dev_customs)}개")
print(f"   - Wiki 세관 퀘스트 총 개수: {len(wiki_customs_quests)}개")
print(f"   - Tarkov.dev 퀘스트 중 Wiki와 100% 일치하는 퀘스트 수: {len(tarkov_dev_in_wiki)}개 ({len(tarkov_dev_in_wiki)/len(tarkov_dev_customs)*100:.1f}%)")
print(f"   - Wiki 세관 퀘스트 중 Tarkov.dev에 존재하는 퀘스트 수: {len(wiki_in_tarkov_dev)}개 ({len(wiki_in_tarkov_dev)/len(wiki_customs_quests)*100:.1f}%)")

print(f"\n2. [Tarkov-Market vs Wiki] 세관(Customs) 퀘스트 일치 분석:")
print(f"   - Tarkov-Market 지도에 표기된 세관 퀘스트 수: {len(market_customs)}개")
print(f"   - Tarkov-Market 퀘스트 중 Wiki와 일치하는 퀘스트 수: {len(market_in_wiki)}개 ({len(market_in_wiki)/max(len(market_customs), 1)*100:.1f}%)")

# Save complete JSON comparison report
report = {
    "summary": {
        "wiki_customs_total": len(wiki_customs_quests),
        "tarkov_dev_customs_total": len(tarkov_dev_customs),
        "tarkov_dev_wiki_overlap": len(tarkov_dev_in_wiki),
        "market_customs_total": len(market_customs),
        "market_wiki_overlap": len(market_in_wiki)
    },
    "tarkov_dev_customs_list": list(tarkov_dev_customs.values()),
    "wiki_customs_list": list(wiki_customs_quests.values())
}

with open("intermediate_results/customs_quests_cross_analysis.json", "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)

print("\nSaved detailed comparison to intermediate_results/customs_quests_cross_analysis.json")
