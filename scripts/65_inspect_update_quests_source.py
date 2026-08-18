with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-quests.mjs", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines[:100]):
    if "http" in l or "import" in l or "api" in l or "task" in l:
        print(f"L{i+1}: {l.strip()}")
