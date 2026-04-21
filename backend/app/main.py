from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ai import generate_roast
from app.config import settings
from app.github import get_readme_from_repo_url
from app.schemas import RoastRequest, RoastResponse

app = FastAPI(title="README Roaster", version="1.0.0")

app.add_middleware(
	CORSMiddleware,
	allow_origins=[settings.cors_origin] if settings.cors_origin != "*" else ["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
	return {"status": "ok"}


@app.post("/roast", response_model=RoastResponse)
async def roast_readme(payload: RoastRequest) -> RoastResponse:
	try:
		readme_text = await get_readme_from_repo_url(payload.repo_url)
		roasted = await generate_roast(readme_text, payload.mode)
		return RoastResponse(**roasted)
	except ValueError as exc:
		raise HTTPException(status_code=400, detail=str(exc)) from exc
	except RuntimeError as exc:
		raise HTTPException(status_code=502, detail=str(exc)) from exc
	except Exception as exc:
		raise HTTPException(status_code=500, detail="Unexpected server error") from exc
