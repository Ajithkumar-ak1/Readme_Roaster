from typing import Literal
from pydantic import BaseModel, Field, field_validator


RoastMode = Literal["funny", "professional", "savage"]


class RoastRequest(BaseModel):
	repo_url: str = Field(..., examples=["https://github.com/torvalds/linux"])
	mode: RoastMode = "funny"

	@field_validator("repo_url")
	@classmethod
	def validate_github_url(cls, value: str) -> str:
		if "github.com" not in value.lower():
			raise ValueError("repo_url must be a valid GitHub repository URL")
		return value.strip()


class RoastResponse(BaseModel):
	roast: str
	issues: list[str]
	suggestions: list[str]
	improved_readme: str
