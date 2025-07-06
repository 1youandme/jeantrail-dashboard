import os
from github import Github
from git import Repo

# بياناتك هنا
GITHUB_USERNAME = "YourUsername"
GITHUB_TOKEN = "ghp_YourGitHubTokenHere"
REPO_NAME = "jeantrail_ai"
PROJECT_PATH = "C:/Users/dell/JeanTrail_AI"

def create_and_push_repo():
    # الاتصال بـ GitHub
    g = Github(GITHUB_TOKEN)
    user = g.get_user()

    # إنشاء الريبو لو مش موجود
    repo = None
    try:
        repo = user.create_repo(REPO_NAME)
        print(f"✅ تم إنشاء الريبو: https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
    except Exception as e:
        print(f"⚠️ الريبو موجود بالفعل أو فشل الإنشاء: {e}")
        repo = user.get_repo(REPO_NAME)

    # تهيئة Git محليًا
    if not os.path.exists(os.path.join(PROJECT_PATH, ".git")):
        Repo.init(PROJECT_PATH)
    repo_local = Repo(PROJECT_PATH)
    origin = None

    # إضافة الملفات ورفعها
    repo_local.git.add(all=True)
    repo_local.index.commit("initial commit")
    origin = repo_local.create_remote("origin", repo.clone_url.replace("https://", f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@"))
    origin.push(refspec="master:main")
    print("🚀 تم رفع المشروع بنجاح على GitHub!")

if __name__ == "__main__":
    create_and_push_repo()
