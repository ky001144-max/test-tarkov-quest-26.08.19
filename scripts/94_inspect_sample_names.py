import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("intermediate_results/customs_quests_cross_analysis.json", "r", encoding="utf-8") as f:
    data = json.load(f)

td_list = data["tarkov_dev_customs_list"]
wiki_list = data["wiki_customs_list"]

print("Tarkov.dev sample customs quests:", td_list[:10])
print("\nWiki sample customs quests:", wiki_list[:10])
