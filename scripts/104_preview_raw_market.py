with open("map_data/tarkov market/market_all.txt", "r", encoding="utf-8") as f:
    text_sample = f.read(1000)

print("=== market_all.txt raw preview ===")
print(text_sample)

with open("map_data/tarkov market/market_list.txt", "r", encoding="utf-8") as f:
    list_sample = f.read(1000)

print("\n=== market_list.txt raw preview ===")
print(list_sample)
