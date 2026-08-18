import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Checking newly added files in map_data/tarkov dev ===")
folder = "map_data/tarkov dev"
for f in os.listdir(folder):
    full_p = os.path.join(folder, f)
    size = os.path.getsize(full_p)
    print(f"  * {f} ({size:,} bytes)")
