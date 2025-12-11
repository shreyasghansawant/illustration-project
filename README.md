# 🎨 Illustration Personalizer

An end-to-end prototype that personalizes illustrations with a child's photo using AI. Upload a photo, and the system will transform it into a stylized illustrated version and insert it into a template.

## 🏗️ Architecture

```
┌─────────────────┐
│   Next.js UI    │
│  (Frontend)     │
│  - Upload UI    │
│  - Preview      │
│  - Download     │
└────────┬────────┘
         │ HTTP POST
         │ /api/personalize
         ▼
┌─────────────────┐
│  FastAPI        │
│  (Backend)      │
│  - Image Upload │
│  - Processing   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Replicate API  │
│  - Instant-ID   │
│  - IP-Adapter   │
│  FaceID         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Personalized   │
│  Illustration   │
└─────────────────┘
```

### Components

1. **Frontend (Next.js)**: React-based UI for uploading photos and displaying results
2. **Backend (FastAPI)**: Python API server handling image processing
3. **AI Model (Replicate)**: Cloud-based AI service using Instant-ID/IP-Adapter for face personalization

## 📦 GitHub & Deployment

**Quick Setup:**
1. See [QUICK_START.md](QUICK_START.md) for GitHub push and hosting
2. See [GITHUB_SETUP.md](GITHUB_SETUP.md) for detailed GitHub instructions
3. See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for deployment options

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Replicate API token ([Get one here](https://replicate.com/account/api-tokens))

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file:
```bash
cp .env.example .env
# Edit .env and add your REPLICATE_API_TOKEN
```

Run the backend:
```bash
python main.py
# Or: uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the frontend:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example         # Environment variables template
│   └── templates/           # Template illustrations
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main upload UI
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Styles
│   ├── package.json
│   └── next.config.js
└── README.md
```

## 🎯 Features

- ✅ Drag-and-drop photo upload
- ✅ Real-time preview
- ✅ AI-powered face personalization
- ✅ Template integration
- ✅ Download personalized illustrations
- ✅ Responsive UI

## 🤖 Model Choice: Instant-ID / IP-Adapter FaceID

### Why Instant-ID?

**Instant-ID** is chosen for this prototype because:

1. **High Quality Face Preservation**: Maintains facial identity while applying artistic styles
2. **Fast Processing**: Optimized for real-time or near-real-time generation
3. **Style Flexibility**: Can adapt to various illustration styles (cartoon, children's book, etc.)
4. **Cloud-Based**: No need for local GPU setup via Replicate API
5. **Easy Integration**: Simple API interface

**IP-Adapter FaceID** is used as a fallback because:
- Similar capabilities to Instant-ID
- Better availability on Replicate
- Good balance between quality and speed

### Alternative Models Considered

- **ControlNet**: More control but requires more setup and is slower
- **SDXL**: General purpose, less specialized for face preservation
- **Stable Diffusion**: Base model, would need additional face preservation layers

## ⚠️ Limitations

1. **API Dependency**: Requires Replicate API token and internet connection
2. **Processing Time**: Can take 10-30 seconds depending on API load
3. **Face Detection**: Current implementation uses simplified face positioning (center placement)
4. **Template Integration**: Basic compositing - doesn't use advanced face detection for template positioning
5. **Cost**: Replicate API usage incurs costs per request
6. **Image Size**: Large images are resized to 1024px for faster processing
7. **Single Face**: Optimized for single face photos

## 🔮 Version 2 Improvements

1. **Advanced Face Detection**: 
   - Use OpenCV/MTCNN for precise face detection in templates
   - Automatic face alignment and positioning

2. **Multiple Templates**:
   - Template selection UI
   - Pre-defined template library
   - Custom template upload

3. **Local Model Option**:
   - Support for local Instant-ID deployment
   - Reduce API costs and latency

4. **Batch Processing**:
   - Process multiple photos at once
   - Queue system for multiple requests

5. **Style Customization**:
   - User-selectable illustration styles
   - Adjustable parameters (color intensity, cartoon level, etc.)

6. **Better Error Handling**:
   - Retry logic for API failures
   - Progress indicators for long-running operations
   - Better fallback mechanisms

7. **Performance Optimization**:
   - Image caching
   - CDN for template storage
   - Async processing with webhooks

8. **User Features**:
   - User accounts and history
   - Save favorite templates
   - Share personalized illustrations

9. **Quality Improvements**:
   - Higher resolution output
   - Better face blending with templates
   - Support for multiple faces

10. **Deployment**:
    - Docker containerization
    - Kubernetes deployment
    - Auto-scaling for high traffic

## 🛠️ Deployment

### Backend (FastAPI)

**Option 1: Vercel (Serverless)**
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd backend
vercel
```

**Option 2: AWS (EC2/ECS)**
- Use Docker container
- Deploy to ECS or EC2 instance
- Set up load balancer

**Option 3: Railway/Render**
- Connect GitHub repo
- Set environment variables
- Auto-deploy on push

### Frontend (Next.js)

**Vercel (Recommended)**
```bash
cd frontend
vercel
```

Or connect GitHub repo to Vercel for automatic deployments.

## 📝 API Documentation

### POST `/api/personalize`

Upload a photo to personalize an illustration.

**Request:**
- `file`: Image file (multipart/form-data)
- `template` (optional): Template name

**Response:**
- PNG image (binary)

**Example:**
```bash
curl -X POST http://localhost:8000/api/personalize \
  -F "file=@photo.jpg"
```

## 🔒 Environment Variables

### Backend
- `REPLICATE_API_TOKEN`: Your Replicate API token

### Frontend
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)

## 📄 License

This is a prototype project for demonstration purposes.

## 🤝 Contributing

This is a prototype assignment. For production use, consider:
- Adding proper error handling
- Implementing authentication
- Adding rate limiting
- Setting up monitoring and logging

## 📧 Support

For issues or questions, please check:
- Replicate API documentation: https://replicate.com/docs
- FastAPI documentation: https://fastapi.tiangolo.com
- Next.js documentation: https://nextjs.org/docs

