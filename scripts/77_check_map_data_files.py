import os
import json

map_data_dir = "map_data"
print(f"Listing files in {map_data_dir}:")
for f in os.listdir(map_data_dir):
    full_p = os.path.join(map_data_dir, f)
    print(f"  - {f} ({os.path.getsize(full_p):,} bytes)")
