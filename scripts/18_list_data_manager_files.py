import os

base_dir = "tarkov-data-manager-main"
all_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, base_dir)
        size = os.path.getsize(full_path)
        all_files.append((rel_path, size))

print(f"Total files in tarkov-data-manager-main: {len(all_files)}")
print("\nFiles related to tasks, quests, maps, coordinates:")
for path, size in all_files:
    if any(k in path.lower() for k in ["quest", "task", "map", "coord", "pos", "data", "dump", "schema", "job"]):
        print(f"  - {path} ({size} bytes)")
