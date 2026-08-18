import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Committing and Pushing to GitHub ===")

def run_cmd(cmd):
    print(f"\n$ {cmd}")
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', shell=True)
    if res.stdout:
        print("STDOUT:", res.stdout.strip())
    if res.stderr:
        print("STDERR:", res.stderr.strip())
    return res.returncode

run_cmd("git add .")
run_cmd('git commit -m "test-tarkov quest(26.08.19)"')
run_cmd("git push -u origin main")
