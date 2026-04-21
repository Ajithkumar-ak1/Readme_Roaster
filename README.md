# README Roaster

README Roaster is an AI-powered full-stack app that fetches a GitHub repository README, roasts it, identifies issues, suggests improvements, and generates an improved rewritten README.

## Project Structure

- backend: FastAPI API + GitHub fetch + Groq integration
- frontend: React + Vite + Tailwind single-page app

## End-to-End Flow

1. User enters a GitHub repository URL.
2. Backend fetches README using GitHub API.
3. Backend sends README to Groq model.
4. API returns:
   - roast
   - issues
   - suggestions
   - improved_readme
5. Frontend renders output with copy button.

## Run Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and calls backend at `http://localhost:8000/roast`.

## Example cURL

```bash
curl -X POST http://localhost:8000/roast \
-H "Content-Type: application/json" \
-d '{"repo_url":"https://github.com/torvalds/linux","mode":"funny"}'
```
