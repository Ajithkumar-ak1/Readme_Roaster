import json


def _sanitize_json_control_chars(text: str) -> str:
    """Escape raw control characters that occasionally appear inside JSON strings."""
    result: list[str] = []
    in_string = False
    escaped = False

    for char in text:
        if escaped:
            result.append(char)
            escaped = False
            continue

        if char == "\\":
            result.append(char)
            escaped = True
            continue

        if char == '"':
            result.append(char)
            in_string = not in_string
            continue

        if in_string and char == "\n":
            result.append("\\n")
            continue
        if in_string and char == "\r":
            result.append("\\r")
            continue
        if in_string and char == "\t":
            result.append("\\t")
            continue

        result.append(char)

    return "".join(result)


def extract_json_block(text: str) -> dict:
    """Extract the first valid JSON object from a model response."""
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model response does not contain a valid JSON object")

    candidate = text[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        sanitized = _sanitize_json_control_chars(candidate)
        return json.loads(sanitized)


def ensure_string_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []