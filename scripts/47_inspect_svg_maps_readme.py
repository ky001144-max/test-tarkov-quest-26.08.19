import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("tarkov-dev-svg-maps-main/README.md", "r", encoding="utf-8") as f:
    print("README.md:")
    print(f.read()[:1000])

with open("tarkov-dev-svg-maps-main/replace_style_common.py", "r", encoding="utf-8") as f:
    print("\nreplace_style_common.py:")
    print(f.read())
