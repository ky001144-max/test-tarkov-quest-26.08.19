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

# 1. Wiki Customs Quests
with open("primary_data/wiki_quests_page.html", "r", encoding="utf-8") as f:
    wiki_html = f.read()

wiki_soup = BeautifulSoup(wiki_html, 'html.parser')
wiki_all = {}
wiki_customs = {}

tables = wiki_soup.find_all('table', class_='wikitable')
for t in tables:
    rows = t.find_all('tr')
    for r in rows:
        cols = r.find_all(['td', 'th'])
        if cols:
            q_link = cols[0].find('a')
            if q_link:
                q_name = q_link.get_text().strip()
                row_text = r.get_text()
                if q_name and not q_name.startswith("File:") and len(q_name) > 1:
                    norm = normalize_name(q_name)
                    wiki_all[norm] = q_name
                    if "customs" in row_text.lower():
                        wiki_customs[norm] = q_name

# 2. Tarkov.dev Quests with English names
# We can load English translations from primary_data or tasks.txt
with open("app/data/quests.json", "r", encoding="utf-8") as f:
    td_quests = json.load(f)

td_customs = {}
td_all = {}

for q in td_quests:
    q_name = q.get("title_en", "")
    norm = normalize_name(q_name)
    td_all[norm] = q_name
    
    is_customs = q.get("map_id") == "customs" or any(o.get("map_id") == "customs" for o in q.get("objectives", []))
            
    if is_customs:
        td_customs[norm] = q_name

# 3. Tarkov-Market Customs Quests
# Tarkov-Market maps show specific in-map marker quest objects
# Let's extract the actual quest markers on tarkov-market.com/maps/customs
market_customs = {}
with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

# Look for quest names in the market HTML
for norm, name in wiki_all.items():
    # If the quest name appears in the market page HTML
    pattern = r'\b' + re.escape(name) + r'\b'
    if re.search(pattern, market_html, re.IGNORECASE):
        market_customs[norm] = name

print("=== EXACT COMPARISON RESULTS ===")
print(f"1. Fandom Wiki Total Quests: {len(wiki_all)} quests")
print(f"   - Fandom Wiki Customs Quests: {len(wiki_customs)} quests")

print(f"\n2. Tarkov.dev Total Quests: {len(td_all)} quests")
print(f"   - Tarkov.dev Customs Quests: {len(td_customs)} quests")

print(f"\n3. Tarkov-Market Customs Quests on Map: {len(market_customs)} quests")

# Overlaps
td_overlap_wiki = set(td_customs.keys()).intersection(set(wiki_customs.keys()))
market_overlap_wiki = set(market_customs.keys()).intersection(set(wiki_customs.keys()))

print(f"\n=======================================================")
print(f"               OVERLAP ANALYSIS REPORT                 ")
print(f"=======================================================")
print(f"A. [Tarkov.dev vs Wiki]")
print(f"   - Tarkov.dev 세관 퀘스트 총: {len(td_customs)}개")
print(f"   - Wiki 세관 퀘스트와 겹치는 퀘스트: {len(td_overlap_wiki)}개 ({len(td_overlap_wiki)/len(td_customs)*100:.1f}%)")

print(f"\nB. [Tarkov-Market vs Wiki]")
print(f"   - Tarkov-Market 세관 퀘스트 총: {len(market_customs)}개")
print(f"   - Wiki 세관 퀘스트와 겹치는 퀘스트: {len(market_overlap_wiki)}개 ({len(market_overlap_wiki)/max(len(market_customs), 1)*100:.1f}%)")

# Detailed list of matched quests
print(f"\n--- Overlapping Customs Quests (Tarkov.dev & Wiki) Sample ({len(td_overlap_wiki)} total) ---")
for idx, k in enumerate(sorted(td_overlap_wiki)[:15]):
    print(f"  {idx+1}. {wiki_customs[k]}")

# Detailed list of market matched quests
print(f"\n--- Overlapping Customs Quests (Tarkov-Market & Wiki) Sample ({len(market_overlap_wiki)} total) ---")
for idx, k in enumerate(sorted(market_overlap_wiki)[:15]):
    print(f"  {idx+1}. {wiki_customs[k]}")
