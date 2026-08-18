import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Checking map_data folder contents ===")
for root, dirs, files in os.walk("map_data"):
    print(f"\nFolder: {root}")
    for f in files:
        full_p = os.path.join(root, f)
        size = os.path.getsize(full_p)
        print(f"  - {f} ({size:,} bytes)")
