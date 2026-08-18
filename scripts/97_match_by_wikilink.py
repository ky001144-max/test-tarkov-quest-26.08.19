import json
import re
import urllib.parse
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def normalize_name(name):
    if not name:
        return ""
    s = urllib.parse.unquote(name).replace("_", " ").lower().strip()
    s = re.sub(r'[\(\)\-\–\—\:\,\.\'\"]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

# 1. PARSE WIKI QUESTS
with open("primary_data/wiki_quests_page.html", "r", encoding="utf-8") as f:
    wiki_html = f.read()

wiki_soup = BeautifulSoup(wiki_html, 'html.parser')
wiki_all = {}
wiki_customs = {}

for t in wiki_soup.find_all('table', class_='wikitable'):
    for r in t.find_all('tr'):
        cols = r.find_all(['td', 'th'])
        if len(cols) >= 3:
            q_link = cols[1].find('a') if len(cols) > 1 else None
            if q_link:
                q_name = q_link.get_text().strip()
                if q_name and not q_name.startswith("File:"):
                    norm = normalize_name(q_name)
                    wiki_all[norm] = q_name
                    obj_text = cols[2].get_text() if len(cols) > 2 else ""
                    if "customs" in obj_text.lower() or "customs" in r.get_text().lower():
                        wiki_customs[norm] = {
                            "name": q_name,
                            "objectives": obj_text.strip()
                        }

# 2. PARSE TARKOV.DEV QUESTS using wikiLink and Unity map hash
with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    td_raw = json.load(f)

td_tasks = td_raw["data"]["tasks"]
CUSTOMS_HASH = "56f40101d2720b2a4d8b45d6"

td_customs = {}
td_all = {}

for q_id, q in td_tasks.items():
    wiki_link = q.get("wikiLink", "")
    # extract title from wiki link
    name_from_link = wiki_link.split("/wiki/")[-1] if "/wiki/" in wiki_link else q.get("name", "")
    norm = normalize_name(name_from_link)
    
    if norm:
        td_all[norm] = {
            "id": q_id,
            "name": urllib.parse.unquote(name_from_link).replace("_", " "),
            "wiki_link": wiki_link
        }
        
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
            td_customs[norm] = {
                "id": q_id,
                "name": urllib.parse.unquote(name_from_link).replace("_", " "),
                "wiki_link": wiki_link
            }

# 3. PARSE TARKOV-MARKET CUSTOMS
with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

# Extract all quest title links or markers on Tarkov-Market customs
market_customs = {}
market_norm_html = normalize_name(market_html)

for norm, info in wiki_customs.items():
    qname = info["name"]
    # Check if exact quest name or url slug exists in market html
    if norm in market_norm_html or qname.lower() in market_html.lower():
        market_customs[norm] = qname

# CROSS MATCHING
td_in_wiki = set(td_customs.keys()).intersection(set(wiki_customs.keys()))
market_in_wiki = set(market_customs.keys()).intersection(set(wiki_customs.keys()))

print(f"=======================================================")
print(f"               CROSS MATCHING REPORT                   ")
print(f"=======================================================")
print(f"1. Fandom Wiki 세관 퀘스트 총 개수: {len(wiki_customs)}개")
print(f"2. Tarkov.dev 세관 퀘스트 총 개수: {len(td_customs)}개")
print(f"   -> Wiki와 겹치는 퀘스트 수: {len(td_in_wiki)}개 ({len(td_in_wiki)/len(wiki_customs)*100:.1f}%)")

print(f"\n3. Tarkov-Market 세관 퀘스트 총 개수: {len(market_customs)}개")
print(f"   -> Wiki와 겹치는 퀘스트 수: {len(market_in_wiki)}개 ({len(market_in_wiki)/len(wiki_customs)*100:.1f}%)")

print(f"\n--- [Tarkov.dev & Wiki] 겹치는 세관 퀘스트 목록 ({len(td_in_wiki)}개) ---")
for idx, k in enumerate(sorted(td_in_wiki)):
    print(f"  {idx+1:2d}. {wiki_customs[k]['name']}")

print(f"\n--- [Tarkov-Market & Wiki] 겹치는 세관 퀘스트 목록 ({len(market_in_wiki)}개) ---")
for idx, k in enumerate(sorted(market_in_wiki)):
    print(f"  {idx+1:2d}. {wiki_customs[k]['name']}")
