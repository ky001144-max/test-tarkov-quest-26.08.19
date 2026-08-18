import shutil

# Sync app_v11 to main app/
shutil.copyfile("app_v11/data/quests.json", "app/data/quests.json")
print("Synced enriched quests.json to main app/ directory successfully!")
