# Starting the Backend Server

## Quick Start

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Activate virtual environment (if using one):**
   ```bash
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD:
   venv\Scripts\activate.bat
   
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Start the server:**
   ```bash
   python main.py
   ```

4. **Server will start on:**
   - URL: `http://localhost:8001`
   - Root endpoint: `http://localhost:8001/`
   - Health check: `http://localhost:8001/health`
   - API docs: `http://localhost:8001/docs`
   - Personalize endpoint: `http://localhost:8001/api/personalize`

## Alternative: Using Uvicorn Directly

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

The `--reload` flag enables auto-reload on code changes (useful for development).

## Troubleshooting

### Port Already in Use

If port 8001 is already in use, you can change it in `main.py`:

```python
uvicorn.run(app, host="0.0.0.0", port=8002)  # Change port number
```

Then update the frontend `.env.local` file:
```
NEXT_PUBLIC_API_URL=http://localhost:8002
```

### Module Not Found Errors

Make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### API Token Not Set

Create a `.env` file in the backend directory:
```
REPLICATE_API_TOKEN=your_token_here
```

## Verifying Server is Running

Test the server with:

```bash
# PowerShell:
Invoke-RestMethod -Uri http://localhost:8001/ -Method Get

# Or using curl:
curl http://localhost:8001/
```

You should see:
```json
{
  "message": "Illustration Personalizer API",
  "status": "running"
}
```

