import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("map_data/tarkov market/market_all.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Parse pseudo JSON keys in market_all.txt
print(f"Total length of market_all.txt: {len(content):,} chars")

# Find keys: word followed by encrypted base64 payload
keys_found = re.findall(r'([a-zA-Z0-9_\-]+)\s+([A-Za-z0-9\+\/\=]{30,})', content)
print(f"Found {len(keys_found)} key-payload pairs in market_all.txt:")
for k, payload in keys_found:
    print(f"  * Key: '{k}' -> Payload size: {len(payload):,} bytes")
