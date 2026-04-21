import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
	groq_api_key: str = os.getenv("GROQ_API_KEY", "")
	groq_model: str = os.getenv("GROQ_MODEL", "")
	groq_api_base: str = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1")
	github_api_base: str = os.getenv("GITHUB_API_BASE", "https://api.github.com")
	cors_origin: str = os.getenv("CORS_ORIGIN", "*")


settings = Settings()
