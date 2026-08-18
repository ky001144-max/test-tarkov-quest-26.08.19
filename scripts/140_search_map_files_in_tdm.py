import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for root, dirs, files in os.walk("tarkov-data-manager-main"):
    for f in files:
        if "map" in f.lower():
            full_p = os.path.join(root, f)
            print(f"Found map file: {full_p} ({os.path.getsize(full_p):,} bytes)")
