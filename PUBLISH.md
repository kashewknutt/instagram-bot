# Publish this platform to GitHub

This cloud token cannot create new repositories. Create an empty repo once, then push:

## Option A — GitHub website

1. Open https://github.com/new
2. Owner: `kashewknutt`
3. Name: `social-agent-platform`
4. Public, **no** README / gitignore / license
5. Create repository
6. From this folder:

```powershell
cd D:\GitHub\social-agent-platform
git remote add origin https://github.com/kashewknutt/social-agent-platform.git
git push -u origin main
```

## Option B — gh CLI (your account)

```powershell
gh repo create kashewknutt/social-agent-platform --public --source=. --remote=origin --push
```
