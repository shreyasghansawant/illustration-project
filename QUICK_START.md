# Quick Start Guide - GitHub & Hosting

## 🚀 Complete Setup in 5 Steps

### Step 1: Push to GitHub

```bash
# In your project root directory
cd "C:\Users\Shreyas Ghansawant\Desktop\New folder"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Illustration Personalizer"

# Add your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**First time?** You'll need to:
- Create repository on GitHub.com first
- Authenticate (use Personal Access Token or SSH)

### Step 2: Deploy Backend (Railway - Easiest)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Click **"Add Service"** → **"GitHub Repo"**
6. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variable:
   - **Name**: `REPLICATE_API_TOKEN`
   - **Value**: Your Replicate API token
8. Railway auto-deploys! Get your URL (e.g., `https://your-app.railway.app`)

### Step 3: Deploy Frontend (Vercel - Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click **"Add New..."** → **"Project"**
4. Select your repository
5. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js (auto-detected)
6. Add environment variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Railway backend URL (from Step 2)
7. Click **"Deploy"**
8. Your frontend is live! (e.g., `https://your-app.vercel.app`)

### Step 4: Update Backend CORS

Edit `backend/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://your-app.vercel.app"  # Your Vercel frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit and push:
```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push
```

Railway will auto-redeploy!

### Step 5: Test Your Deployment

1. Visit your Vercel frontend URL
2. Upload a photo
3. Wait for processing
4. Download the result!

## 📋 Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Railway
- [ ] Frontend deployed on Vercel
- [ ] Environment variables set
- [ ] CORS updated
- [ ] Tested end-to-end

## 🔧 Alternative: All on Railway

If you prefer one platform:

1. **Backend Service:**
   - Root: `backend`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Env: `REPLICATE_API_TOKEN`

2. **Frontend Service:**
   - Root: `frontend`
   - Build: `npm install && npm run build`
   - Start: `npm start`
   - Env: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`

## 💰 Cost

- **Vercel**: Free for personal projects
- **Railway**: $5/month free credit (usually enough for small projects)
- **Total**: ~$0-5/month

## 🆘 Need Help?

- **GitHub Issues**: Check GITHUB_SETUP.md
- **Hosting Issues**: Check HOSTING_GUIDE.md
- **Local Setup**: Check SETUP.md

## 🔄 Updating Your Deployment

After making changes:

```bash
# Make your changes
# ...

# Commit and push
git add .
git commit -m "Your update description"
git push
```

Both Railway and Vercel auto-deploy on push!

