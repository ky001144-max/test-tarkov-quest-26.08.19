import os
import json

base_dir = "tarkov-data-manager-main/src/tarkov-data-manager"

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if any(k in f.lower() for k in ["zone", "loot", "location", "detail", "coord", "map"]):
            full_p = os.path.join(root, f)
            print(f"File: {full_p} ({os.path.getsize(full_p)} bytes)")
