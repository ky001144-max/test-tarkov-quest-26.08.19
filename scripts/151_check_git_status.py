import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Checking Git Status & Remotes ===")

def run_git(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
        print(f"\n$ {cmd}")
        if res.stdout:
            print(res.stdout[:1000])
        if res.stderr:
            print("STDERR:", res.stderr[:500])
        return res.returncode
    except Exception as e:
        print("Error:", e)
        return 1

run_git("git status")
run_git("git remote -v")
run_git("git branch")
