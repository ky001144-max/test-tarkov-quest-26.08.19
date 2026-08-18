import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Searching for market_quests.json and dev_quests.json ===")

target_files = ["market_quests.json", "dev_quests.json"]

for root, dirs, files in os.walk("."):
    for f in files:
        if f in target_files or "quest" in f.lower():
            full_p = os.path.join(root, f)
            size = os.path.getsize(full_p)
            print(f"  * Found: {full_p} ({size:,} bytes)")
