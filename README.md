# 🎨 Illustration Personalizer

An end-to-end prototype that personalizes illustrations with a child's photo using AI. Upload a photo, and the system transforms it into a stylized illustrated version.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Replicate API token ([Get one here](https://replicate.com/account/api-tokens))

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Create `.env` file:
```bash
REPLICATE_API_TOKEN=your_token_here
```

Run the backend:
```bash
python main.py
```

Backend runs on `http://localhost:8001`

### Frontend Setup

```bash
cd frontend
npm install
```

Create `.env.local` file:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8001
```

Run the frontend:
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   ├── env.example          # Environment template
│   └── templates/           # Template illustrations
├── frontend/
│   ├── app/
│   │   ├── page.tsx         # Main UI
│   │   ├── layout.tsx
│   │   └── globals.css
│   └── package.json
└── README.md
```

## 🎯 Features

- Drag-and-drop photo upload
- AI-powered face personalization
- Template integration
- Download personalized illustrations

## 🤖 AI Model

Uses **Instant-ID / IP-Adapter FaceID** via Replicate API for face personalization with illustration styling.

## 🛠️ Deployment

**See [DEPLOY.md](DEPLOY.md) for complete step-by-step instructions**

Quick steps:
1. Push code to GitHub
2. Deploy backend and frontend on Railway (or Render)
3. Set environment variables
4. Update CORS settings
5. Done!

## 📝 API

**POST** `/api/personalize`

Upload a photo to personalize an illustration.

**Request:**
- `file`: Image file (multipart/form-data)

**Response:**
- PNG image (binary)

## 🔒 Environment Variables

**Backend:**
- `REPLICATE_API_TOKEN`: Your Replicate API token

**Frontend:**
- `NEXT_PUBLIC_API_URL`: Backend API URL

## 📄 License

Prototype project for demonstration purposes.
