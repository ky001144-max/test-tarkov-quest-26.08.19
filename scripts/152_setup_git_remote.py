import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Setting up Git Remote and Pushing ===")

repo_url = "https://github.com/ky001144-max/test-tarkov-quest-26.08.19.git"

def run_cmd(cmd):
    print(f"\n$ {cmd}")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
    if res.stdout:
        print("STDOUT:", res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return res.returncode

# 1. Check if git initialized
run_cmd("git init")

# 2. Set remote origin
run_cmd(f"git remote set-url origin {repo_url} || git remote add origin {repo_url}")

# 3. Verify remote
run_cmd("git remote -v")

# 4. Check status
run_cmd("git status")
