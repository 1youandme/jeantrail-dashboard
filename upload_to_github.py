import os
from dotenv import load_dotenv
import subprocess

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = "youandme"
REPO_NAME = "jeantrail-dashboard"
PROJECT_PATH = os.path.abspath(".")

remote_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{REPO_NAME}.git"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error:\n{result.stderr}")
    else:
        print(result.stdout.strip())

# Git commands
print("📁 Initializing Git...")
run_cmd("git init")
run_cmd(f"git remote add origin {remote_url}")
run_cmd("git add .")
run_cmd('git commit -m "🚀 Initial upload from JeanTrail AI Agent"')
run_cmd("git branch -M main")
run_cmd("git push -u origin main")
