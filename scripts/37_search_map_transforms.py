with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-maps.mjs", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ["processZones", "extracts", "spawns", "switches", "convertCoordinates", "getTransformedPosition", "transform["]):
        print(f"L{i+1}: {l.strip()}")
