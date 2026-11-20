"""Validate data/trivia.json for schema issues, duplicates, and Discord button limits."""
import json
import sys
from pathlib import Path

TRIVIA_PATH = Path(__file__).resolve().parent / "data" / "trivia.json"
MAX_BUTTON_LABEL = 80


def validate_trivia(path: Path = TRIVIA_PATH) -> list[str]:
    errors: list[str] = []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"Failed to read/parse JSON: {exc}"]

    if not isinstance(data, list) or not data:
        return ["Top-level JSON value must be a non-empty list."]

    seen_questions: dict[str, int] = {}

    for idx, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f"Item #{idx}: must be a JSON object.")
            continue

        question = item.get("question")
        correct = item.get("correct")
        wrong = item.get("wrong")

        # 1. Check required fields and types
        if not isinstance(question, str) or not question.strip():
            errors.append(f"Item #{idx}: 'question' must be a non-empty string.")
            continue
        if not isinstance(correct, str) or not correct.strip():
            errors.append(f"Item #{idx}: 'correct' must be a non-empty string.")
            continue
        if not isinstance(wrong, list) or not wrong or not all(isinstance(w, str) and w.strip() for w in wrong):
            errors.append(f"Item #{idx}: 'wrong' must be a non-empty list of strings.")
            continue

        # 2. Check for duplicate questions (case-insensitive)
        norm_q = " ".join(question.lower().split())
        if norm_q in seen_questions:
            errors.append(
                f"Item #{idx}: duplicate question (matches item #{seen_questions[norm_q]}): {question!r}"
            )
        else:
            seen_questions[norm_q] = idx

        # 3. Check for duplicate answer options within the same question
        all_options = [correct, *wrong]
        seen_opts: set[str] = set()
        for opt in all_options:
            norm_opt = opt.strip().lower()
            if norm_opt in seen_opts:
                errors.append(f"Item #{idx}: duplicate answer option {opt!r} in {question!r}")
            seen_opts.add(norm_opt)

        # 4. Check Discord's 80-character button label limit
        for opt in all_options:
            if len(opt) > MAX_BUTTON_LABEL:
                errors.append(
                    f"Item #{idx}: option exceeds {MAX_BUTTON_LABEL} chars ({len(opt)} chars): {opt!r}"
                )

    return errors


if __name__ == "__main__":
    issues = validate_trivia()
    if issues:
        print(f"❌ Found {len(issues)} issue(s) in data/trivia.json:\n")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)

    total = len(json.loads(TRIVIA_PATH.read_text(encoding="utf-8")))
    print(f"✅ data/trivia.json is valid! ({total} questions checked, 0 issues)")