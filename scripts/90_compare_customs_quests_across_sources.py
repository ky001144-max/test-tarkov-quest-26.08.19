import urllib.request
import json
import re
from bs4 import BeautifulSoup
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Headers for HTTP requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 1. Fetch Wiki Quests
wiki_url = "https://escapefromtarkov.fandom.com/wiki/Quests"
print(f"1. Fetching Wiki Quests from {wiki_url}...")

wiki_customs_quests = set()
wiki_all_quests = set()

try:
    req = urllib.request.Request(wiki_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for tables with quest links or list items
        tables = soup.find_all('table', class_='wikitable')
        print(f"   Found {len(tables)} wikitables on Wiki page.")
        
        for t in tables:
            rows = t.find_all('tr')
            for r in rows:
                cols = r.find_all(['td', 'th'])
                if len(cols) >= 2:
                    quest_link = cols[0].find('a')
                    location_text = cols[1].get_text().strip() if len(cols) > 1 else ""
                    
                    # Sometimes location is in another column
                    row_text = r.get_text()
                    
                    if quest_link:
                        q_name = quest_link.get_text().strip()
                        if q_name and not q_name.startswith("File:"):
                            wiki_all_quests.add(q_name)
                            if "customs" in row_text.lower():
                                wiki_customs_quests.add(q_name)
                                
        # Fallback regex if table structure varies
        if len(wiki_customs_quests) == 0:
            for a in soup.find_all('a'):
                title = a.get('title')
                if title and not ":" in title:
                    parent = a.find_parent('tr')
                    if parent and "customs" in parent.get_text().lower():
                        wiki_customs_quests.add(title.strip())

except Exception as e:
    print(f"   Notice while fetching wiki: {e}")

print(f"   -> Wiki Total Quests: {len(wiki_all_quests)}")
print(f"   -> Wiki Customs Quests: {len(wiki_customs_quests)}")

# 2. Extract Tarkov.dev Customs Quests
print("\n2. Extracting Tarkov.dev Customs Quests...")
with open("map_data/tasks.txt", "r", encoding="utf-8") as f:
    raw_tasks = json.load(f)

with open("map_data/tasks_ko.txt", "r", encoding="utf-8") as f:
    i18n = json.load(f).get("data", {})

tasks_dict = raw_tasks["data"]["tasks"]

tarkov_dev_customs_quests = set()
tarkov_dev_all_quests = set()

# Customs Map ID in Tarkov.dev Unity data
CUSTOMS_MAP_HASH = "56f40101d2720b2a4d8b45d6"

for q_id, q in tasks_dict.items():
    name_en = q.get("name", "")
    tarkov_dev_all_quests.add(name_en)
    
    is_customs = False
    if q.get("map") == CUSTOMS_MAP_HASH:
        is_customs = True
    else:
        for o in q.get("objectives", []):
            if any(z.get("map") == CUSTOMS_MAP_HASH for z in o.get("zones", [])):
                is_customs = True
                break
            if any(m == CUSTOMS_MAP_HASH for m in o.get("maps", [])):
                is_customs = True
                break
                
    if is_customs:
        tarkov_dev_customs_quests.add(name_en)

print(f"   -> Tarkov.dev Total Quests: {len(tarkov_dev_all_quests)}")
print(f"   -> Tarkov.dev Customs Quests: {len(tarkov_dev_customs_quests)}")

# 3. Fetch or analyze Tarkov-Market Customs Quests
print("\n3. Fetching Tarkov-Market Customs Quests...")
market_url = "https://tarkov-market.com/maps/customs"
market_customs_quests = set()

try:
    req = urllib.request.Request(market_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for script tags with initial data or elements with quest names
        for script in soup.find_all('script'):
            txt = script.get_text()
            if "quest" in txt.lower() or "task" in txt.lower():
                # Search for task names
                pass
except Exception as e:
    print(f"   Notice while fetching market: {e}")

# Save intermediate datasets for detailed cross-matching
with open("intermediate_results/wiki_customs_quests.json", "w", encoding="utf-8") as f:
    json.dump(list(wiki_customs_quests), f, indent=2, ensure_ascii=False)

with open("intermediate_results/tarkov_dev_customs_quests.json", "w", encoding="utf-8") as f:
    json.dump(list(tarkov_dev_customs_quests), f, indent=2, ensure_ascii=False)
