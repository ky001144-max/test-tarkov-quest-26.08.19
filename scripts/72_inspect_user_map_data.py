import os
import json

map_data_dir = "map_data"

if os.path.exists(map_data_dir):
    print(f"Found folder: {map_data_dir}")
    for root, dirs, files in os.walk(map_data_dir):
        for f in files:
            full_p = os.path.join(root, f)
            size = os.path.getsize(full_p)
            print(f"  - File: {f} ({size:,} bytes)")
            
            # Check JSON content sample
            if f.endswith(".json") or not "." in f:
                try:
                    with open(full_p, "r", encoding="utf-8") as jf:
                        content = jf.read()
                        print(f"     * Preview (first 200 chars): {content[:200]}")
                        # Try parsing json
                        data = json.loads(content)
                        if isinstance(data, list):
                            print(f"     * Type: Array of {len(data)} items")
                            if len(data) > 0 and isinstance(data[0], dict):
                                print(f"     * Keys in item[0]: {list(data[0].keys())}")
                        elif isinstance(data, dict):
                            print(f"     * Type: Object with keys: {list(data.keys())[:10]}")
                except Exception as e:
                    print(f"     * Read/Parse notice: {e}")
else:
    print("map_data folder not found at root. Checking subdirectories...")
    for item in os.listdir("."):
        if "map" in item.lower() or "data" in item.lower():
            print("  *", item)
