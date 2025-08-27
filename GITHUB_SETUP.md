# GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in to your account
2. Click the "+" icon in the top right corner and select "New repository"
3. Repository settings:
   - **Repository name**: `travel-lykk` (or your preferred name)
   - **Description**: `Travel booking web application built with Django`
   - **Visibility**: Public (recommended for showcase)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

## Step 2: Push Code to GitHub

After creating the repository, run these commands in your terminal:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/travel-lykk.git

# Push the code to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed automatically

## Step 4: Update README with Your Links

1. Edit the README.md file on GitHub (or locally)
2. Replace these placeholders:
   - `[Your GitHub URL will go here]` with your actual repository URL
   - `[Coming Soon - Will be deployed to PythonAnywhere]` with your deployment URL once deployed

## Your Repository URL Format

Your GitHub repository URL will be:
```
https://github.com/YOUR_USERNAME/travel-lykk
```

## Next Steps

After pushing to GitHub:
1. ✅ GitHub repository created and code uploaded
2. 🚀 Deploy to PythonAnywhere (see PYTHONANYWHERE_DEPLOYMENT.md)
3. 📝 Update README with deployment URL
4. 🎉 Share both GitHub and deployment URLs for submission

---

**Important**: Make sure to replace `YOUR_USERNAME` with your actual GitHub username in all commands and URLs!
