# GitHub Setup Guide

## Initial GitHub Repository Setup

### Step 1: Create a New Repository on GitHub

1. Go to [GitHub](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `illustration-personalizer` (or your preferred name)
   - **Description**: "AI-powered illustration personalizer using Instant-ID"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 2: Initialize Git in Your Project

Open terminal/PowerShell in your project root directory and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Illustration Personalizer with FastAPI and Next.js"

# Add your GitHub repository as remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/illustration-personalizer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify Push

1. Go to your GitHub repository page
2. You should see all your files there
3. Verify that `.env` files are NOT included (they should be in .gitignore)

## Complete Git Commands (Copy-Paste Ready)

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual values:

```bash
# Navigate to project root
cd "C:\Users\Shreyas Ghansawant\Desktop\New folder"

# Initialize git
git init

# Configure git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Illustration Personalizer

- FastAPI backend with Replicate API integration
- Next.js frontend with upload UI
- AI-powered face personalization
- Template compositing support
- Complete documentation"

# Add remote repository (replace URL with yours)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

## Future Updates

After making changes:

```bash
# Check status
git status

# Add changed files
git add .

# Commit changes
git commit -m "Description of your changes"

# Push to GitHub
git push
```

## Important: Environment Variables

**NEVER commit `.env` files!** They contain sensitive API keys.

The `.gitignore` file already excludes:
- `.env`
- `.env.local`
- `venv/`
- `node_modules/`
- Other sensitive files

## GitHub Repository Structure

Your repository should have:

```
illustration-personalizer/
├── .gitignore
├── README.md
├── ARCHITECTURE.md
├── MODEL_CHOICE.md
├── SETUP.md
├── DEPLOYMENT.md
├── GITHUB_SETUP.md
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── env.example
│   └── templates/
└── frontend/
    ├── app/
    ├── package.json
    └── ...
```

## Troubleshooting

### Authentication Issues

If you get authentication errors:

**Option 1: Use Personal Access Token**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use token as password when pushing

**Option 2: Use SSH**
```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@example.com"

# Add to GitHub: Settings → SSH and GPG keys → New SSH key
# Then use SSH URL:
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git
```

### Large Files

If you have large files (templates, etc.):
- Use Git LFS: `git lfs install`
- Or add to `.gitignore` if not needed in repo

### Port Conflicts

If you need to change the port back to 8000:
1. Update `backend/main.py` (change port 8001 → 8000)
2. Update `frontend/app/page.tsx` (change port 8001 → 8000)
3. Commit and push changes

