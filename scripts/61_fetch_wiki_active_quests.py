import requests
import json
import re
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Query Tarkov Wiki Quests page or API for official active quests
wiki_url = "https://escapefromtarkov.fandom.com/api.php?action=parse&page=Quests&format=json"

try:
    r = requests.get(wiki_url, headers=headers, timeout=10)
    data = r.json()
    html_content = data.get("parse", {}).get("text", {}).get("*", "")
    print(f"Fetched Wiki Quests HTML: {len(html_content)} bytes")
    
    # Extract all quest names from table
    soup = BeautifulSoup(html_content, "html.parser")
    tables = soup.find_all("table", class_="wikitable")
    print(f"Found {len(tables)} quest tables on Wiki.")
    
    wiki_quests = set()
    for table in tables:
        for row in table.find_all("tr"):
            cols = row.find_all(["td", "th"])
            if cols:
                title_link = cols[0].find("a")
                if title_link and title_link.get("title"):
                    qname = title_link.get("title").strip()
                    if not any(k in qname for k in ["Quests", "File:", "Category:", "Trader"]):
                        wiki_quests.add(qname)
                        
    print(f"Total active quests extracted from Wiki: {len(wiki_quests)}")
    sample_list = list(wiki_quests)[:20]
    print("Sample Wiki Quests:", sample_list)
    
    # Check if BP depot exists on Wiki
    print("Is 'BP depot' in Wiki?:", "BP depot" in wiki_quests or "BP Depot" in wiki_quests)
    print("Is 'The Blood of War - Part 1' in Wiki?:", "The Blood of War - Part 1" in wiki_quests)
    
    with open("secondary_data/wiki_active_quests.json", "w", encoding="utf-8") as f:
        json.dump(sorted(list(wiki_quests)), f, indent=2, ensure_ascii=False)
except Exception as e:
    print("Error querying Wiki API:", e)
