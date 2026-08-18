import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Use Fandom MediaWiki API which is open and returns structured JSON
api_url = "https://escapefromtarkov.fandom.com/api.php?action=parse&page=Quests&prop=text&format=json"
headers = {
    'User-Agent': 'TarkovQuestResearcher/1.0 (Mozilla/5.0)'
}

try:
    req = urllib.request.Request(api_url, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
        html_content = data['parse']['text']['*']
        print(f"Successfully fetched Wiki Quests HTML from MediaWiki API! Length: {len(html_content):,} chars")
        
        with open("primary_data/wiki_quests_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Saved raw wiki HTML to primary_data/wiki_quests_page.html")
except Exception as e:
    print(f"Error fetching from MediaWiki API: {e}")
