import os

target_folder = "tarkov-dev-svg-maps-main"
if os.path.exists(target_folder):
    print(f"Found folder: {target_folder}")
    for root, dirs, files in os.walk(target_folder):
        for f in files:
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, target_folder)
            print(f"  - {rel_p} ({os.path.getsize(full_p)} bytes)")
else:
    print(f"Folder {target_folder} does not exist in root directory. Searching elsewhere...")
    for item in os.listdir("."):
        if "svg" in item.lower() or "map" in item.lower():
            print("  *", item)
