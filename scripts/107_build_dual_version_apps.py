import shutil
import os
import json
import re

print("=== Building v1.10 (Tarkov.dev) and v1.11 (Tarkov-Market) Applications ===")

# Base source is app/
app_v10_dir = "app_v10"
app_v11_dir = "app_v11"

# 1. Clean and recreate app_v10
if os.path.exists(app_v10_dir):
    shutil.rmtree(app_v10_dir)
shutil.copytree("app", app_v10_dir)
print(f"Created {app_v10_dir} base structure.")

# 2. Clean and recreate app_v11
if os.path.exists(app_v11_dir):
    shutil.rmtree(app_v11_dir)
shutil.copytree("app", app_v11_dir)
print(f"Created {app_v11_dir} base structure.")

# ----------------------------------------------------
# CONFIGURE APP V1.10 (Tarkov.dev Edition)
# ----------------------------------------------------
# Customize index.html for v1.10
v10_html_path = os.path.join(app_v10_dir, "index.html")
with open(v10_html_path, "r", encoding="utf-8") as f:
    v10_html = f.read()

v10_html = v10_html.replace("<title>타르코프 퀘스트 가이드 & 맵</title>", "<title>[v1.10] 타르코프 퀘스트 가이드 - Tarkov.dev Edition</title>")
v10_html = v10_html.replace('<h1>타르코프 퀘스트 가이드</h1>', '<h1>타르코프 퀘스트 가이드 <span class="version-tag" style="background: rgba(229,197,138,0.2); color: #e5c58a; border: 1px solid #e5c58a; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-left: 8px;">v1.10 Tarkov.dev</span></h1>')

with open(v10_html_path, "w", encoding="utf-8") as f:
    f.write(v10_html)

# ----------------------------------------------------
# CONFIGURE APP V1.11 (Tarkov-Market Edition)
# ----------------------------------------------------
# Customize index.html for v1.11
v11_html_path = os.path.join(app_v11_dir, "index.html")
with open(v11_html_path, "r", encoding="utf-8") as f:
    v11_html = f.read()

v11_html = v11_html.replace("<title>타르코프 퀘스트 가이드 & 맵</title>", "<title>[v1.11] 타르코프 퀘스트 가이드 - Tarkov-Market Edition</title>")
v11_html = v11_html.replace('<h1>타르코프 퀘스트 가이드</h1>', '<h1>타르코프 퀘스트 가이드 <span class="version-tag" style="background: rgba(0,210,255,0.2); color: #00d2ff; border: 1px solid #00d2ff; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin-left: 8px;">v1.11 Tarkov-Market</span></h1>')

with open(v11_html_path, "w", encoding="utf-8") as f:
    f.write(v11_html)

print("Successfully configured HTML templates for both versions!")
