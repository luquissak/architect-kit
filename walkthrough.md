# Application Startup Walkthrough

The Architect Kit application consists of a FastAPI backend and a Vite/React frontend.

## 1. Backend Startup

The backend is located in the `backend` directory. It uses a Python virtual environment.

- **Command**: `.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000`
- **Location**: `backend`
- **Status**: Currently running at [http://localhost:8000](http://localhost:8000)

## 2. Frontend Startup

The frontend is located in the root directory.

- **Command**: `npm run dev`
- **Location**: Root directory
- **Status**: Currently running at [http://localhost:5173/](http://localhost:5173/)

## Verification

- Backend API: [http://localhost:8000/api/history](http://localhost:8000/api/history) (Should return a JSON list of history items)
- Frontend UI: [http://localhost:5173/](http://localhost:5173/) (Main application interface)
