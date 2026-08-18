import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

map_data_dir = "map_data"
print(f"=== Scanning {map_data_dir} directory structure ===")

for root, dirs, files in os.walk(map_data_dir):
    rel_path = os.path.relpath(root, map_data_dir)
    print(f"\n[Directory] map_data / {rel_path if rel_path != '.' else ''}")
    for d in dirs:
        print(f"  + Subfolder: {d}")
    for f in files:
        full_f = os.path.join(root, f)
        size = os.path.getsize(full_f)
        print(f"  - File: {f} ({size:,} bytes)")
