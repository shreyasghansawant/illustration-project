# Setup Instructions

## Prerequisites

- **Node.js**: Version 18 or higher ([Download](https://nodejs.org/))
- **Python**: Version 3.9 or higher ([Download](https://www.python.org/downloads/))
- **Replicate API Token**: Get one from [Replicate](https://replicate.com/account/api-tokens)

## Step-by-Step Setup

### 1. Clone or Download the Repository

```bash
# If using git
git clone <repository-url>
cd illustration-personalizer

# Or extract the downloaded folder
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
# Copy the example file
copy env.example .env  # Windows
# or
cp env.example .env    # macOS/Linux

# Edit .env and add your Replicate API token
# REPLICATE_API_TOKEN=your_token_here
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local file
# On Windows:
copy .env.local.example .env.local
# On macOS/Linux:
cp .env.local.example .env.local

# Edit .env.local if needed (default is http://localhost:8000)
```

### 4. Add Template (Optional)

1. Place your template illustration in `backend/templates/`
2. Name it `template.png` for default template
3. Or use custom names and reference in code

### 5. Run the Application

#### Terminal 1 - Backend

```bash
cd backend
# Make sure virtual environment is activated
python main.py
```

Backend will run on `http://localhost:8000`

#### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

### 6. Test the Application

1. Open browser to `http://localhost:3000`
2. Upload a child's photo
3. Click "Personalize Illustration"
4. Wait for processing (10-30 seconds)
5. Download the result

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

**Module not found:**
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

**Replicate API errors:**
- Check your API token in `.env`
- Verify token is valid at https://replicate.com/account/api-tokens
- Check your Replicate account has credits

### Frontend Issues

**Cannot connect to backend:**
- Verify backend is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Check CORS settings in backend

**Build errors:**
```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
```

### General Issues

**Image upload fails:**
- Check file size (should be reasonable, < 10MB)
- Verify file is an image format (JPG, PNG, etc.)
- Check browser console for errors

**Processing takes too long:**
- Normal: 10-30 seconds is expected
- Check Replicate API status
- Verify internet connection

## Development Tips

### Backend Development

- Use `uvicorn main:app --reload` for auto-reload
- Check logs in terminal for errors
- Test API directly with:
  ```bash
  curl -X POST http://localhost:8000/api/personalize -F "file=@test.jpg"
  ```

### Frontend Development

- Use browser DevTools to debug
- Check Network tab for API calls
- Use React DevTools for component debugging

## Production Deployment

See `README.md` for deployment instructions to:
- Vercel (Frontend)
- AWS/Railway/Render (Backend)
- Or your preferred hosting platform

## Getting Help

1. Check the documentation files:
   - `README.md` - Overview and features
   - `ARCHITECTURE.md` - System architecture
   - `MODEL_CHOICE.md` - AI model details

2. Check error messages in:
   - Backend terminal output
   - Browser console
   - Network tab in DevTools

3. Verify:
   - All dependencies installed
   - Environment variables set
   - Services running on correct ports

