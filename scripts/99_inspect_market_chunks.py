import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

# Find all script src
scripts = re.findall(r'src=\"(\/_nuxt\/[^\"]+\.js)\"', market_html)
print(f"Found {len(scripts)} Nuxt chunk scripts in Tarkov-Market:")

base_market_url = "https://tarkov-market.com"
market_quests_from_chunks = set()

for s in scripts:
    s_url = base_market_url + s
    print(f"  Fetching chunk: {s}...")
    try:
        req = urllib.request.Request(s_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode('utf-8')
            if "quest" in content.lower() or "customs" in content.lower() or "pocket watch" in content.lower():
                print(f"    -> MATCH in {s}! Size: {len(content):,} chars")
                # Look for quest titles
                titles = re.findall(r'\"([A-Z][a-zA-Z0-9\s\-\'\:]{3,40})\"', content)
                for t in titles:
                    if any(k in t.lower() for k in ["check", "delivery", "customs", "chemical", "dorm", "watch", "bad rep", "golden swag", "water", "extortionist"]):
                        market_quests_from_chunks.add(t)
    except Exception as e:
        print(f"    Error: {e}")

print(f"\nExtracted {len(market_quests_from_chunks)} potential quest markers from Tarkov-Market JS chunks:")
for q in list(market_quests_from_chunks)[:15]:
    print("  *", q)
