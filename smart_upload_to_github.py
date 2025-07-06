import os
from dotenv import load_dotenv
import subprocess

# تحميل متغيرات البيئة من .env
load_dotenv()

# قراءة القيم من .env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")
REPO_URL = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

def run(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and "warning" not in result.stderr.lower():
        print("❌ Error:\n", result.stderr)

# Initialize git
print("📁 Initializing Git...")
run("git init")
run("git add .")
run("git commit -m \"🚀 Smart upload from JeanTrail AI Agent\"")

# Add or update remote
print("🔄 Checking remote...")
remotes = subprocess.run("git remote", shell=True, capture_output=True, text=True).stdout.strip()
if "origin" not in remotes:
    run(f"git remote add origin {REPO_URL}")
else:
    run(f"git remote set-url origin {REPO_URL}")

# Pull latest changes first
print("🔽 Pulling latest changes (if any)...")
run("git pull origin main --allow-unrelated-histories")

# Push to GitHub
print("🚀 Pushing to GitHub...")
run("git push origin main")
