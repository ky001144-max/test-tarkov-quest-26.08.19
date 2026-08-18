with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-quests.mjs", "r", encoding="utf-8") as f:
    code = f.read()

import re
matches = [m.start() for m in re.finditer(r'objective\.map|objective\.position|objective\.zone|task\.map|location', code)]
print(f"Found {len(matches)} matches.")

lines = code.split("\n")
for i, line in enumerate(lines):
    if any(k in line for k in ["zone", "zones", "positions", "leftPercent", "topPercent", "objective.maps", "objective.map", "task.map", "locationMap"]):
        print(f"L{i+1}: {line.strip()}")
