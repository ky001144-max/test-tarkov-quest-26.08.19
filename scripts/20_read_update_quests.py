with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-quests.mjs", "r", encoding="utf-8") as f:
    code = f.read()

print(f"update-quests.mjs length: {len(code)}")

# Look for location, map, gps, objective, bounds
lines = code.split("\n")
for i, l in enumerate(lines[:120]):
    print(f"L{i+1}: {l}")
