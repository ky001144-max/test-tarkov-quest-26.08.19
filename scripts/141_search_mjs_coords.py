import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("tarkov-data-manager-main/src/tarkov-data-manager/jobs/update-maps.mjs", "r", encoding="utf-8") as f:
    mjs = f.read()

keywords = ["coordinateRotation", "bounds", "transform"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), mjs)]
    print(f"'{kw}': {len(matches)} matches")
    for p in matches[:2]:
        print(f"\nMatch at {p}:")
        print(mjs[max(0, p-60):min(len(mjs), p+200)])
