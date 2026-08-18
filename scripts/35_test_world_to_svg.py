import json
import math

# Load maps data with official transforms
with open("primary_data/tarkov_dev_maps_json.json", "r", encoding="utf-8") as f:
    maps_data = json.load(f)

customs_map = next(m for m in maps_data if m.get("normalizedName") == "customs")
submap = next(sm for sm in customs_map["maps"] if sm.get("projection") == "interactive")
transform = submap["transform"] # [0.239, 168.65, 0.239, 136.35]
rotation = submap["coordinateRotation"] # 180

scaleX = transform[0]
scaleY = transform[2] * -1
marginX = transform[1]
marginY = transform[3]

print(f"Customs Transform: scaleX={scaleX}, scaleY={scaleY}, marginX={marginX}, marginY={marginY}, rotation={rotation}")

def world_to_svg(x, z):
    rad = (rotation * math.pi) / 180.0
    cosA = math.cos(rad)
    sinA = math.sin(rad)
    rotX = x * cosA - z * sinA
    rotZ = x * sinA + z * cosA
    
    # SVG coordinates
    svgX = scaleX * rotX + marginX
    svgY = scaleY * rotZ + marginY
    return svgX, svgY

# Checking Bronze Pocket Watch in Construction Tanker Truck:
# Construction Tanker in Unity is approx around x = 120 ~ 130, z = -80 ~ -90
# Let's test
test_points = [
    ("Construction Tanker (Pocket Watch)", 125.0, -85.0),
    ("Dorms 3-Story (Golden Zibbo)", 180.0, -250.0),
    ("Big Red / Customs Office (Delivery from past)", -300.0, 50.0),
    ("Gas Station", 30.0, -50.0)
]

print("\nWorld (x, z) to SVG (pixelX, pixelY) on Customs.svg (1062.5 x 535.2):")
for name, wx, wz in test_points:
    sx, sy = world_to_svg(wx, wz)
    print(f"  {name:45s} -> World({wx:6.1f}, {wz:6.1f}) -> SVG({sx:6.1f}, {sy:6.1f}) | ({sx/1062.5*100:5.1f}%, {sy/535.2*100:5.1f}%)")
