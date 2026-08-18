import os
import shutil
import json

# Create app folders
os.makedirs("app/data", exist_ok=True)
os.makedirs("app/maps", exist_ok=True)
os.makedirs("app/icons", exist_ok=True)

# Copy processed datasets
shutil.copy("secondary_data/processed_quests.json", "app/data/quests.json")
shutil.copy("secondary_data/processed_maps.json", "app/data/maps.json")
shutil.copy("secondary_data/processed_traders.json", "app/data/traders.json")

# Copy SVG maps
svg_dir = "primary_data/maps_svg"
for f in os.listdir(svg_dir):
    if f.endswith(".svg"):
        shutil.copy(os.path.join(svg_dir, f), os.path.join("app/maps", f))

# Copy interactive icons
icons_dir = "primary_data/interactive_icons"
if os.path.exists(icons_dir):
    for f in os.listdir(icons_dir):
        if f.endswith(".png"):
            shutil.copy(os.path.join(icons_dir, f), os.path.join("app/icons", f))

print("Asset bundling completed successfully for app directory.")
