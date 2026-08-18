import urllib.request
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Check market HTML for __NUXT__ or api endpoints
with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

nuxt_match = re.search(r'window\.__NUXT__\s*=\s*(.*?);<\/script>', market_html, re.DOTALL)
if nuxt_match:
    nuxt_data = nuxt_match.group(1)
    print(f"Found __NUXT__ state in Tarkov-Market! Length: {len(nuxt_data):,} chars")
    with open("primary_data/market_nuxt_state.js", "w", encoding="utf-8") as f:
        f.write(nuxt_data)
else:
    print("No __NUXT__ found. Searching for marker endpoints in JS scripts...")
    script_srcs = re.findall(r'src=\"([^\"]+\.js)\"', market_html)
    print(f"Found {len(script_srcs)} JS scripts:")
    for s in script_srcs[:5]:
        print("  *", s)
