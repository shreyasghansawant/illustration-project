# Deployment Guide

## Deployment Options

### Option 1: Vercel (Recommended for Frontend)

#### Frontend Deployment

1. **Connect Repository**
   - Push code to GitHub
   - Go to [Vercel](https://vercel.com)
   - Import your repository

2. **Configure Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` with your backend URL
   - Example: `https://your-backend.railway.app`

3. **Deploy**
   - Vercel will auto-detect Next.js
   - Click Deploy
   - Your frontend will be live!

#### Backend Deployment (Vercel Serverless)

Vercel also supports Python/FastAPI via serverless functions:

1. Create `vercel.json` in backend:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

2. Add environment variables in Vercel dashboard
3. Deploy

### Option 2: Railway (Recommended for Backend)

#### Backend Deployment

1. **Sign up** at [Railway](https://railway.app)

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"

3. **Configure**
   - Select your repository
   - Railway auto-detects Python
   - Add environment variables:
     - `REPLICATE_API_TOKEN`

4. **Deploy**
   - Railway will build and deploy
   - Get your backend URL (e.g., `https://your-app.railway.app`)

5. **Update Frontend**
   - Update `NEXT_PUBLIC_API_URL` to Railway URL

### Option 3: Render

#### Backend Deployment

1. **Create Web Service** on [Render](https://render.com)

2. **Connect Repository**
   - Link GitHub repo
   - Select branch

3. **Configure**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
   - Add environment variables:
     - `REPLICATE_API_TOKEN`

4. **Deploy**
   - Render will build and deploy
   - Get your backend URL

#### Frontend Deployment

1. **Create Static Site** on Render
2. **Build Command**: `npm run build`
3. **Publish Directory**: `.next`
4. Add environment variables

### Option 4: AWS (EC2/ECS)

#### Using EC2

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro or larger
   - Configure security group (port 8000)

2. **SSH into Instance**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

4. **Clone and Setup**
```bash
git clone your-repo
cd your-repo/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. **Create Systemd Service**
```bash
sudo nano /etc/systemd/system/illustration-api.service
```

Add:
```ini
[Unit]
Description=Illustration Personalizer API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/your-repo/backend
Environment="PATH=/home/ubuntu/your-repo/backend/venv/bin"
ExecStart=/home/ubuntu/your-repo/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

6. **Start Service**
```bash
sudo systemctl start illustration-api
sudo systemctl enable illustration-api
```

7. **Configure Nginx** (optional, for reverse proxy)
```bash
sudo nano /etc/nginx/sites-available/illustration-api
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/illustration-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Using ECS (Docker)

1. **Create Dockerfile** in backend:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Build and Push to ECR**
```bash
aws ecr create-repository --repository-name illustration-personalizer
docker build -t illustration-personalizer .
docker tag illustration-personalizer:latest your-account.dkr.ecr.region.amazonaws.com/illustration-personalizer:latest
docker push your-account.dkr.ecr.region.amazonaws.com/illustration-personalizer:latest
```

3. **Create ECS Task Definition and Service**
   - Use AWS Console or CLI
   - Configure environment variables
   - Set up load balancer

### Option 5: Docker Compose (Local/Server)

1. **Create Dockerfile** (see above)

2. **Create docker-compose.yml**:
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

3. **Deploy**
```bash
docker-compose up -d
```

## Environment Variables

### Backend
- `REPLICATE_API_TOKEN`: Your Replicate API token (required)

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL (required)

## Post-Deployment Checklist

- [ ] Backend is accessible (test `/health` endpoint)
- [ ] Frontend can connect to backend
- [ ] CORS is configured correctly
- [ ] Environment variables are set
- [ ] API token is valid
- [ ] Templates directory exists (if using templates)
- [ ] Error handling works
- [ ] Logs are accessible

## Monitoring

### Recommended Tools

1. **Uptime Monitoring**: UptimeRobot, Pingdom
2. **Error Tracking**: Sentry
3. **Analytics**: Google Analytics, Plausible
4. **Logs**: CloudWatch (AWS), Railway logs, Render logs

### Health Check Endpoint

Your backend has a `/health` endpoint:
```bash
curl https://your-backend-url/health
```

Use this for uptime monitoring.

## Scaling Considerations

### Backend Scaling

1. **Horizontal Scaling**
   - Use load balancer (Nginx, AWS ALB)
   - Deploy multiple instances
   - Use container orchestration (Kubernetes, ECS)

2. **Database** (if adding in v2)
   - Use managed database (RDS, Railway Postgres)
   - Connection pooling

3. **Caching**
   - Redis for request caching
   - CDN for static assets

### Cost Optimization

1. **API Costs**
   - Cache frequent requests
   - Use local models for high volume
   - Batch processing

2. **Infrastructure**
   - Use serverless for variable traffic
   - Auto-scaling
   - Reserved instances for steady traffic

## Troubleshooting Deployment

### Backend Not Starting

- Check logs: `docker logs <container>` or service logs
- Verify environment variables
- Check port binding
- Verify Python version

### Frontend Build Fails

- Check Node.js version (18+)
- Clear `.next` folder
- Verify environment variables
- Check for TypeScript errors

### API Connection Issues

- Verify CORS settings
- Check backend URL in frontend
- Verify network/firewall rules
- Test backend directly with curl

### Replicate API Errors

- Verify API token
- Check Replicate account credits
- Verify model availability
- Check API rate limits

## Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **CORS**: Restrict origins in production
3. **Rate Limiting**: Add rate limiting middleware
4. **HTTPS**: Always use HTTPS in production
5. **API Keys**: Rotate keys regularly
6. **Input Validation**: Validate all inputs
7. **File Upload**: Limit file size and types

## Example Production Configuration

### Backend (FastAPI)

```python
# In main.py, update CORS for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],  # Specific origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Frontend (Next.js)

```javascript
// In next.config.js
module.exports = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
  // Add security headers
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
        ],
      },
    ]
  },
}
```

