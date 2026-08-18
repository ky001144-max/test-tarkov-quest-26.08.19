import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

js_url = "https://tarkov-market.com/_nuxt3/B6f_aNvN.js"
print(f"Fetching {js_url} to analyze decryption algorithm...")

try:
    req = urllib.request.Request(js_url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        js_content = resp.read().decode('utf-8')
        print(f"Fetched JS ({len(js_content):,} chars)!")
        with open("primary_data/market_main_bundle.js", "w", encoding="utf-8") as f:
            f.write(js_content)
            
        # Search for decryption keys, crypto-js, xor, aes, or decrypt function
        matches = re.findall(r'(\b[a-zA-Z0-9_$]+\.decrypt\b|\bAES\b|\bdecode\b|\bdecompress\b)', js_content)
        print(f"Crypto matches: {set(matches)}")
except Exception as e:
    print(f"Error fetching JS: {e}")
