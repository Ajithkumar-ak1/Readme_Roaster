import asyncio
import requests
from app.config import settings
from app.schemas import RoastMode
from app.utils import ensure_string_list, extract_json_block


def _tone_instruction(mode: RoastMode) -> str:
	if mode == "funny":
		return (
			"Use high-energy humor with playful punchlines. Keep it constructive, non-offensive, "
			"and trend-aware with modern internet and developer culture references."
		)
	if mode == "savage":
		return "Use a brutal roast style and trend-aware with modern internet and developer culture references, but do not use hate, slurs, threats, or harassment."
	return "Use a professional and direct tone."


def _roast_length_rule(mode: RoastMode) -> str:
	if mode == "funny":
		return (
			"roast must be 6-10 short lines with line breaks, at least 90 words total, "
			"include specific jokes about the README content, and end with a playful mic-drop line."
		)
	if mode == "savage":
		return "roast must be 4-7 sentences and sharply critical, but still constructive."
	return "roast must be 3-5 sentences in a clear, professional tone."


def _build_prompt(readme_text: str, mode: RoastMode) -> str:
	return f"""
You are an expert README reviewer.

Style requirement:
{_tone_instruction(mode)}

Analyze the README below and return ONLY a valid JSON object with this exact schema:
{{
  "roast": "string",
  "issues": ["string"],
  "suggestions": ["string"],
  "improved_readme": "string"
}}

Rules:
- roast: based on mode, with personality and concrete references to README weaknesses
- {_roast_length_rule(mode)}
- for funny mode: include 2-4 references to current internet/dev culture language naturally (for example: POV, vibe check, main-character energy, this is giving, low-key/high-key)
- avoid generic one-liners; each roast line should reference an actual README issue
- humor must stay clean, non-hateful, and non-explicit
- if roast quality feels bland, internally revise once before final JSON output
- issues: concrete problems found in the README
- suggestions: actionable improvements
- improved_readme: a rewritten, production-ready README markdown
- No extra keys
- No markdown code fences
- Output must be valid JSON

README to analyze:
{readme_text}
""".strip()


def _call_groq(prompt: str, mode: RoastMode) -> dict:
	if not settings.groq_api_key:
		raise RuntimeError("Missing GROQ_API_KEY in backend/.env")

	url = f"{settings.groq_api_base}/chat/completions"
	headers = {
		"Authorization": f"Bearer {settings.groq_api_key}",
		"Content-Type": "application/json",
	}
	temperature = 0.7
	if mode == "funny":
		temperature = 1.0
	elif mode == "professional":
		temperature = 0.4

	payload = {
		"model": settings.groq_model,
		"messages": [
			{"role": "system", "content": "You are a strict JSON-only assistant."},
			{"role": "user", "content": prompt},
		],
		"temperature": temperature,
	}

	response = requests.post(url, headers=headers, json=payload, timeout=60)
	if response.status_code >= 400:
		raise RuntimeError(f"Groq API error: {response.status_code} {response.text}")

	data = response.json()
	content = data["choices"][0]["message"]["content"]
	parsed = extract_json_block(content)

	return {
		"roast": str(parsed.get("roast", "")).strip(),
		"issues": ensure_string_list(parsed.get("issues", [])),
		"suggestions": ensure_string_list(parsed.get("suggestions", [])),
		"improved_readme": str(parsed.get("improved_readme", "")).strip(),
	}


async def generate_roast(readme_text: str, mode: RoastMode) -> dict:
	prompt = _build_prompt(readme_text, mode)
	result = await asyncio.to_thread(_call_groq, prompt, mode)

	if not result["roast"]:
		result["roast"] = "No roast generated."

	return result
