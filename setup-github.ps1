# GitHub Setup Script for Windows PowerShell
# Run this script in your project root directory

Write-Host "🚀 GitHub Setup Script" -ForegroundColor Green
Write-Host ""

# Check if git is installed
try {
    $gitVersion = git --version
    Write-Host "✅ Git found: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if we're in a git repository
if (Test-Path .git) {
    Write-Host "✅ Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "📦 Initializing git repository..." -ForegroundColor Yellow
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
}

# Check if .gitignore exists
if (Test-Path .gitignore) {
    Write-Host "✅ .gitignore found" -ForegroundColor Green
} else {
    Write-Host "⚠️  .gitignore not found" -ForegroundColor Yellow
}

# Get GitHub repository URL
Write-Host ""
Write-Host "📝 Enter your GitHub repository URL:" -ForegroundColor Cyan
Write-Host "   Example: https://github.com/yourusername/illustration-personalizer.git" -ForegroundColor Gray
$repoUrl = Read-Host "Repository URL"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "❌ Repository URL is required" -ForegroundColor Red
    exit 1
}

# Check if remote already exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "⚠️  Remote 'origin' already exists: $remoteExists" -ForegroundColor Yellow
    $update = Read-Host "Update it? (y/n)"
    if ($update -eq "y" -or $update -eq "Y") {
        git remote set-url origin $repoUrl
        Write-Host "✅ Remote updated" -ForegroundColor Green
    }
} else {
    git remote add origin $repoUrl
    Write-Host "✅ Remote added" -ForegroundColor Green
}

# Add all files
Write-Host ""
Write-Host "📦 Adding files to git..." -ForegroundColor Yellow
git add .

# Check if there are changes to commit
$status = git status --porcelain
if ([string]::IsNullOrWhiteSpace($status)) {
    Write-Host "ℹ️  No changes to commit" -ForegroundColor Gray
} else {
    Write-Host "💾 Creating initial commit..." -ForegroundColor Yellow
    git commit -m "Initial commit: Illustration Personalizer

- FastAPI backend with Replicate API integration
- Next.js frontend with upload UI
- AI-powered face personalization
- Template compositing support
- Complete documentation"
    Write-Host "✅ Commit created" -ForegroundColor Green
}

# Set branch to main
Write-Host ""
Write-Host "🌿 Setting branch to main..." -ForegroundColor Yellow
git branch -M main

# Push to GitHub
Write-Host ""
Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "   (You may need to authenticate)" -ForegroundColor Gray
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📚 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Go to your GitHub repository to verify" -ForegroundColor White
    Write-Host "   2. See HOSTING_GUIDE.md for deployment options" -ForegroundColor White
    Write-Host "   3. See QUICK_START.md for quick deployment" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "❌ Push failed. Common issues:" -ForegroundColor Red
    Write-Host "   - Authentication required (use Personal Access Token)" -ForegroundColor Yellow
    Write-Host "   - Repository doesn't exist (create it on GitHub first)" -ForegroundColor Yellow
    Write-Host "   - Check GITHUB_SETUP.md for detailed instructions" -ForegroundColor Yellow
}

