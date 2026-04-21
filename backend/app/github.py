import asyncio
import base64
from urllib.parse import urlparse
import requests
from app.config import settings


def parse_repo_url(repo_url: str) -> tuple[str, str]:
	parsed = urlparse(repo_url.strip())
	if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
		raise ValueError("Only github.com repository URLs are supported")

	path_parts = [part for part in parsed.path.split("/") if part]
	if len(path_parts) < 2:
		raise ValueError("Repository URL must look like https://github.com/owner/repo")

	owner = path_parts[0]
	repo = path_parts[1]

	if repo.endswith(".git"):
		repo = repo[:-4]

	return owner, repo


def _fetch_readme(owner: str, repo: str) -> str:
	url = f"{settings.github_api_base}/repos/{owner}/{repo}/readme"
	headers = {
		"Accept": "application/vnd.github+json",
		"X-GitHub-Api-Version": "2022-11-28",
		"User-Agent": "README-Roaster",
	}

	response = requests.get(url, headers=headers, timeout=20)

	if response.status_code == 404:
		raise ValueError("Repository or README not found")
	if response.status_code >= 400:
		raise RuntimeError(f"GitHub API error: {response.status_code} {response.text}")

	payload = response.json()
	encoded = payload.get("content")
	if not encoded:
		raise ValueError("README content is empty or missing")

	decoded = base64.b64decode(encoded).decode("utf-8", errors="replace")
	if not decoded.strip():
		raise ValueError("README is empty")

	return decoded


async def get_readme_from_repo_url(repo_url: str) -> str:
	owner, repo = parse_repo_url(repo_url)
	return await asyncio.to_thread(_fetch_readme, owner, repo)
