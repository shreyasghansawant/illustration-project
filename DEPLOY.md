# Step-by-Step Deployment Guide

## Part 1: Push to GitHub

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `illustration-personalizer` (or your choice)
   - **Description**: "AI illustration personalizer"
   - **Visibility**: Public or Private
   - **DO NOT** check "Initialize with README" (we already have files)
4. Click **"Create repository"**
5. **Copy the repository URL** (you'll need it in Step 3)

### Step 2: Open Terminal in Project Folder

1. Open PowerShell or Command Prompt
2. Navigate to your project:
   ```bash
   cd "C:\Users\Shreyas Ghansawant\Desktop\New folder"
   ```

### Step 3: Initialize Git and Push

Run these commands one by one:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Illustration Personalizer"

# Add your GitHub repository (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**If you get authentication error:**
- GitHub will ask for username and password
- For password, use a **Personal Access Token** (not your GitHub password)
- Create token: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token
- Give it `repo` scope
- Use the token as your password

### Step 4: Verify

1. Go to your GitHub repository page
2. You should see all your files
3. ✅ Done! Your code is on GitHub

---

## Part 2: Deploy to Railway (All-in-One)

Railway can host both backend and frontend in one place.

### Step 1: Sign Up for Railway

1. Go to [railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Sign in with **GitHub** (connect your GitHub account)
4. Authorize Railway to access your repositories

### Step 2: Create Backend Service

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Find and select your `illustration-personalizer` repository
4. Railway will create a service automatically

5. **Configure Backend:**
   - Click on the service
   - Go to **"Settings"** tab
   - Set **Root Directory**: `backend`
   - Scroll down to **"Deploy"** section
   - Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Click **"Save"**

6. **Add Environment Variable:**
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - **Name**: `REPLICATE_API_TOKEN`
   - **Value**: Your Replicate API token (get from [replicate.com/account/api-tokens](https://replicate.com/account/api-tokens))
   - Click **"Add"**

7. **Get Backend URL:**
   - Go to **"Settings"** tab
   - Scroll to **"Domains"** section
   - Click **"Generate Domain"**
   - Copy the URL (e.g., `https://your-backend.railway.app`)
   - ✅ Backend is deploying!

### Step 3: Create Frontend Service

1. In your Railway project, click **"New"** → **"GitHub Repo"**
2. Select the same repository (`illustration-personalizer`)
3. **Configure Frontend:**
   - Click on the new service
   - Go to **"Settings"** tab
   - Set **Root Directory**: `frontend`
   - Set **Build Command**: `npm install && npm run build`
   - Set **Start Command**: `npm start`
   - Click **"Save"**

4. **Add Environment Variable:**
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your backend URL from Step 2 (e.g., `https://your-backend.railway.app`)
   - Click **"Add"**

5. **Get Frontend URL:**
   - Go to **"Settings"** tab
   - Scroll to **"Domains"** section
   - Click **"Generate Domain"**
   - Copy the URL (e.g., `https://your-frontend.railway.app`)
   - ✅ Frontend is deploying!

### Step 4: Update Backend CORS

Your backend needs to allow requests from your frontend:

1. Go to your local project
2. Open `backend/main.py`
3. Find this section (around line 19):
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["*"],  # In production, specify your frontend URL
   ```
4. Replace it with:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:3000",
           "https://your-frontend.railway.app"  # Replace with your actual frontend URL
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```
5. Save the file

6. **Commit and push:**
   ```bash
   git add backend/main.py
   git commit -m "Update CORS for production"
   git push
   ```
7. Railway will automatically redeploy your backend!

### Step 5: Test Your Deployment

1. Wait for both services to finish deploying (check Railway dashboard)
2. Visit your frontend URL (e.g., `https://your-frontend.railway.app`)
3. Upload a photo
4. Wait for processing
5. Download the result!

---

## Alternative: Deploy to Render (Free Option)

If you prefer Render:

### Step 1: Sign Up

1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Deploy Backend

1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `illustration-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `REPLICATE_API_TOKEN`
5. Click **"Create Web Service"**
6. Copy your backend URL

### Step 3: Deploy Frontend

1. Click **"New"** → **"Static Site"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `illustration-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `.next`
4. Add environment variable: `NEXT_PUBLIC_API_URL` (your backend URL)
5. Click **"Create Static Site"**

---

## Troubleshooting

### GitHub Push Issues

**"Authentication failed"**
- Use Personal Access Token instead of password
- Create token: GitHub → Settings → Developer settings → Personal access tokens

**"Repository not found"**
- Make sure you created the repository on GitHub first
- Check the repository URL is correct

### Railway Deployment Issues

**Backend not starting**
- Check logs in Railway dashboard
- Verify `REPLICATE_API_TOKEN` is set
- Check Start Command is correct

**Frontend can't connect to backend**
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Make sure backend URL doesn't have trailing slash

**Build fails**
- Check build logs in Railway
- Verify all files are committed to GitHub
- Check Node.js version (should be 18+)

---

## Quick Command Reference

```bash
# Git commands
git init
git add .
git commit -m "Your message"
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

# Update after changes
git add .
git commit -m "Update description"
git push
```

---

## Cost

- **Railway**: $5/month free credit (usually enough for small projects)
- **Render**: Free tier available (with limitations)
- **Total**: ~$0-5/month

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed on Railway/Render
- [ ] Frontend deployed on Railway/Render
- [ ] Environment variables set
- [ ] CORS updated
- [ ] Both services running
- [ ] Tested end-to-end

Your app is now live! 🎉

