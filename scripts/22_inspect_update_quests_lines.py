with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-quests.mjs", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("update-quests.mjs lines 490 to 550:")
for i in range(490, min(550, len(lines))):
    print(f"L{i+1}: {lines[i].rstrip()}")
