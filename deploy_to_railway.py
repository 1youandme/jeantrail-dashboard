import subprocess

print("🚀 بدء عملية النشر إلى Railway...")

# تنفيذ أمر git commit
subprocess.run(["git", "add", "."], check=True)
subprocess.run(["git", "commit", "-m", "🚀 نشر إلى Railway"], check=True)

# تنفيذ push
subprocess.run(["git", "push", "origin", "main"], check=True)

print("✅ تم الدفع إلى GitHub بنجاح. يمكنك الآن فتح Railway لاستكمال الربط.")
