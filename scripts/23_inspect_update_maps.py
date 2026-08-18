with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-maps.mjs", "r", encoding="utf-8") as f:
    code = f.read()

print(f"update-maps.mjs length: {len(code)}")
lines = code.split("\n")
for i, l in enumerate(lines[:120]):
    print(f"L{i+1}: {l}")
