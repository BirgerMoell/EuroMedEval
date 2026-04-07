"""Helpers for parsing source records into the normalized schema."""

from __future__ import annotations

import re


_INLINE_OPTION_PATTERN = re.compile(r"(?:^|\s)([A-E])\.\s")


def parse_inline_lettered_mcq(text: str) -> tuple[str, tuple[str, ...]]:
    """Split a question with inline `A. ... B. ...` options.

    Returns the stem and option texts prefixed with their original letters.
    """
    normalized = re.sub(r"\s+", " ", text).strip()
    matches = list(_INLINE_OPTION_PATTERN.finditer(normalized))
    if len(matches) < 2:
        return normalized, tuple()

    stem = normalized[: matches[0].start()].strip()
    options: list[str] = []

    for index, match in enumerate(matches):
        letter = match.group(1)
        content_start = match.end()
        content_end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        option_text = normalized[content_start:content_end].strip()
        if option_text:
            options.append(f"{letter}. {option_text}")

    return stem, tuple(options)


def label_from_answer_letter(answer_letter: str, options: tuple[str, ...]) -> str | None:
    """Resolve an answer key like `B` against normalized option texts."""
    normalized = answer_letter.strip().upper().rstrip(".")
    if not normalized:
        return None
    for option in options:
        if option.startswith(f"{normalized}. "):
            return option
    return None


def label_from_one_based_index(answer_index: str, options: tuple[str, ...]) -> str | None:
    """Resolve a one-based index like `1` or `2` against option texts."""
    normalized = answer_index.strip()
    if not normalized:
        return None
    try:
        index = int(normalized)
    except ValueError:
        return None
    if 1 <= index <= len(options):
        return options[index - 1]
    return None
