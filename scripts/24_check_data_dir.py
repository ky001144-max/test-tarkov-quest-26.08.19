import os

data_dir = "tarkov-data-manager-main/src/tarkov-data-manager/data"
if os.path.exists(data_dir):
    files = os.listdir(data_dir)
    print(f"Files in data_dir ({len(files)}):")
    for f in sorted(files):
        print(f"  - {f} ({os.path.getsize(os.path.join(data_dir, f))} bytes)")
else:
    print("data_dir does not exist")
