# Architecture Documentation

## System Architecture

### High-Level Overview

The Illustration Personalizer is a three-tier application:

1. **Presentation Layer**: Next.js frontend for user interaction
2. **Application Layer**: FastAPI backend for business logic and API orchestration
3. **AI Service Layer**: Replicate API for AI model execution

## Detailed Component Architecture

### Frontend (Next.js)

```
┌─────────────────────────────────────┐
│         Next.js Application         │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │      Upload Component          │ │
│  │  - File selection              │ │
│  │  - Drag & drop                 │ │
│  │  - Preview                     │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │      API Client (Axios)        │ │
│  │  - POST /api/personalize       │ │
│  │  - FormData upload             │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │      Result Display            │ │
│  │  - Image preview               │ │
│  │  - Download button             │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Technologies:**
- Next.js 14 (App Router)
- React 18
- TypeScript
- Axios for HTTP requests

### Backend (FastAPI)

```
┌─────────────────────────────────────┐
│         FastAPI Server               │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │   Upload Endpoint              │ │
│  │   POST /api/personalize        │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │   Image Processor              │ │
│  │   - Validation                 │ │
│  │   - Format conversion          │ │
│  │   - Resizing                   │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │   AI Service Client            │ │
│  │   - Replicate API              │ │
│  │   - Instant-ID/IP-Adapter      │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │   Template Compositor          │ │
│  │   - Face extraction            │ │
│  │   - Template integration       │ │
│  └──────────────┬────────────────┘ │
│                 │                   │
│  ┌──────────────▼────────────────┐ │
│  │   Response Handler             │ │
│  │   - Image encoding             │ │
│  │   - Error handling             │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Technologies:**
- FastAPI
- Python 3.9+
- Pillow (PIL) for image processing
- Replicate Python SDK
- Uvicorn ASGI server

### AI Processing Pipeline

```
User Photo
    │
    ▼
┌─────────────────┐
│  Image Preprocess│
│  - RGB conversion│
│  - Resize        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Replicate API   │
│  Instant-ID      │
│  - Face encoding │
│  - Style transfer│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Stylized Face   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Template        │
│  Integration     │
│  - Compositing   │
│  - Blending      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Final Image     │
└─────────────────┘
```

## Data Flow

1. **Upload Phase**:
   - User selects/drops image in frontend
   - Frontend creates FormData with image file
   - POST request to `/api/personalize`

2. **Processing Phase**:
   - Backend receives and validates image
   - Image is preprocessed (format, size)
   - Image sent to Replicate API with prompt
   - AI model processes image (10-30 seconds)
   - Stylized face is received

3. **Compositing Phase**:
   - Template image is loaded (if available)
   - Stylized face is composited into template
   - Final image is generated

4. **Response Phase**:
   - Final image encoded as PNG
   - Binary response sent to frontend
   - Frontend displays result
   - User can download image

## Security Considerations

1. **CORS**: Currently open (`*`) - should be restricted in production
2. **File Validation**: Checks file type before processing
3. **Size Limits**: Images resized to prevent memory issues
4. **API Keys**: Stored in environment variables

## Scalability Considerations

### Current Limitations:
- Synchronous processing (blocks request)
- No queue system
- Single instance

### Future Improvements:
- Async processing with Celery/Redis
- Queue system for batch processing
- Horizontal scaling with load balancer
- CDN for template storage
- Caching layer for repeated requests

## Deployment Architecture

### Development
```
Local Machine
├── Frontend (localhost:3000)
└── Backend (localhost:8000)
```

### Production (Recommended)
```
┌─────────────────┐
│   Vercel/Netlify │  ← Frontend (CDN)
└────────┬─────────┘
         │
         │ HTTPS
         ▼
┌─────────────────┐
│   FastAPI        │  ← Backend (AWS/Railway)
│   (API Server)   │
└────────┬─────────┘
         │
         │ API Calls
         ▼
┌─────────────────┐
│   Replicate API  │  ← AI Service (Cloud)
└─────────────────┘
```

## Error Handling Flow

```
Request
  │
  ▼
┌─────────────────┐
│  Validation      │ → Invalid: 400 Error
└────────┬────────┘
         │ Valid
         ▼
┌─────────────────┐
│  API Call        │ → Failure: Fallback stylization
└────────┬────────┘
         │ Success
         ▼
┌─────────────────┐
│  Processing      │ → Error: 500 Error
└────────┬────────┘
         │ Success
         ▼
┌─────────────────┐
│  Response        │
└─────────────────┘
```

## Performance Metrics

- **Upload Time**: < 1 second (depends on image size)
- **Processing Time**: 10-30 seconds (Replicate API)
- **Total Response Time**: 10-35 seconds
- **Image Size Limit**: 1024px (auto-resized)
- **Output Format**: PNG

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Next.js 14 | UI Framework |
| Frontend | React 18 | Component Library |
| Frontend | TypeScript | Type Safety |
| Frontend | Axios | HTTP Client |
| Backend | FastAPI | API Framework |
| Backend | Python 3.9+ | Programming Language |
| Backend | Pillow | Image Processing |
| Backend | Replicate SDK | AI Service Client |
| AI Service | Replicate | Cloud AI Platform |
| AI Model | Instant-ID/IP-Adapter | Face Personalization |
| Server | Uvicorn | ASGI Server |

