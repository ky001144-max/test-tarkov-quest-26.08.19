import re

with open("primary_data/market_customs_page.html", "r", encoding="utf-8") as f:
    market_html = f.read()

scripts = re.findall(r'<script[^>]*src=\"([^\"]+)\"', market_html)
print("All script src tags in tarkov-market HTML:")
for s in scripts:
    print("  *", s)
