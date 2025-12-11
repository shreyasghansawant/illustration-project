# Complete Hosting Guide

## Quick Overview

This application has two parts:
1. **Backend (FastAPI)** - Python server
2. **Frontend (Next.js)** - React application

You can host them separately or together. Here are the best options:

## Option 1: Vercel (Recommended - Easiest)

### Frontend on Vercel (Free)

1. **Push your code to GitHub** (see GITHUB_SETUP.md)

2. **Go to [Vercel](https://vercel.com)** and sign in with GitHub

3. **Import your repository:**
   - Click "Add New..." → "Project"
   - Select your GitHub repository
   - Vercel auto-detects Next.js

4. **Configure environment variables:**
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.com`
   - Click "Deploy"

5. **Your frontend is live!** (e.g., `https://your-app.vercel.app`)

### Backend on Railway/Render (Recommended)

**Railway:**
1. Go to [Railway](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Set root directory to `backend`
6. Add environment variable: `REPLICATE_API_TOKEN`
7. Railway auto-detects Python and deploys
8. Get your backend URL (e.g., `https://your-app.railway.app`)

**Render:**
1. Go to [Render](https://render.com)
2. Sign in with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - **Name**: illustration-personalizer-backend
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variable: `REPLICATE_API_TOKEN`
7. Click "Create Web Service"

## Option 2: All-in-One on Railway

1. **Frontend:**
   - Create new service
   - Root directory: `frontend`
   - Build command: `npm install && npm run build`
   - Start command: `npm start`
   - Add env: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`

2. **Backend:**
   - Create new service
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add env: `REPLICATE_API_TOKEN`

## Option 3: AWS (More Complex)

### Using AWS Elastic Beanstalk

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   cd backend
   eb init -p python-3.9 illustration-personalizer
   ```

3. **Create environment:**
   ```bash
   eb create illustration-env
   ```

4. **Set environment variables:**
   ```bash
   eb setenv REPLICATE_API_TOKEN=your_token
   ```

5. **Deploy:**
   ```bash
   eb deploy
   ```

### Frontend on AWS Amplify

1. Go to [AWS Amplify](https://aws.amazon.com/amplify/)
2. Connect GitHub repository
3. Select `frontend` as root directory
4. Add build settings:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - cd frontend && npm install
       build:
         commands:
           - cd frontend && npm run build
     artifacts:
       baseDirectory: frontend/.next
       files:
         - '**/*'
   ```
5. Add environment variable: `NEXT_PUBLIC_API_URL`

## Option 4: Docker Deployment

### Create Dockerfile for Backend

Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Create Dockerfile for Frontend

Create `frontend/Dockerfile`:
```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

EXPOSE 3000
CMD ["npm", "start"]
```

### Deploy with Docker Compose

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - REPLICATE_API_TOKEN=${REPLICATE_API_TOKEN}
    volumes:
      - ./backend/templates:/app/templates

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend
```

Deploy:
```bash
docker-compose up -d
```

## Environment Variables Checklist

### Backend
- ✅ `REPLICATE_API_TOKEN` - Your Replicate API token

### Frontend
- ✅ `NEXT_PUBLIC_API_URL` - Your backend URL (e.g., `https://your-backend.railway.app`)

## Post-Deployment Steps

1. **Update CORS in backend:**
   ```python
   # In backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://your-frontend.vercel.app"],  # Your frontend URL
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Test your endpoints:**
   - Backend health: `https://your-backend.railway.app/health`
   - Frontend: `https://your-frontend.vercel.app`

3. **Update frontend environment variable:**
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Redeploy frontend

## Cost Estimates

### Free Tier Options:
- **Vercel**: Free for personal projects
- **Railway**: $5/month free credit
- **Render**: Free tier available (with limitations)

### Paid Options:
- **AWS**: Pay-as-you-go (~$10-50/month for small traffic)
- **Railway Pro**: $20/month
- **Render**: $7/month per service

## Recommended Setup for Production

1. **Frontend**: Vercel (free, excellent Next.js support)
2. **Backend**: Railway or Render (easy Python deployment)
3. **Database** (if needed later): Railway Postgres or Supabase (free tier)

## Monitoring Your Deployment

### Health Checks

Set up uptime monitoring:
- [UptimeRobot](https://uptimerobot.com) - Free
- Monitor: `https://your-backend.railway.app/health`

### Logs

- **Railway**: View logs in dashboard
- **Render**: View logs in dashboard
- **Vercel**: View logs in dashboard

## Troubleshooting

### Backend Not Starting

- Check logs in hosting platform
- Verify `REPLICATE_API_TOKEN` is set
- Check Python version (should be 3.9+)

### Frontend Can't Connect to Backend

- Verify `NEXT_PUBLIC_API_URL` is correct
- Check CORS settings in backend
- Verify backend is running and accessible

### Build Failures

- Check build logs for specific errors
- Verify all dependencies in `requirements.txt` and `package.json`
- Check Node.js and Python versions

## Quick Deploy Commands

### Railway CLI
```bash
npm i -g @railway/cli
railway login
railway init
railway up
```

### Vercel CLI
```bash
npm i -g vercel
vercel login
vercel
```

