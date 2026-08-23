import json
from pathlib import Path
from typing import Any

from src.localization.locales import DEFAULT_LOCALE, SUPPORTED_LOCALES


TRANSLATIONS_DIRECTORY = Path(__file__).parent / "translations"


def load_translations(locale: str) -> dict[str, Any]:
    if locale not in SUPPORTED_LOCALES:
        locale = DEFAULT_LOCALE

    translation_file = TRANSLATIONS_DIRECTORY / f"{locale}.json"

    with translation_file.open(encoding="utf-8") as file:
        return json.load(file)


def tr(key: str, locale: str, fallback: str | None = None) -> str:
    translations = load_translations(locale)
    default_translations = load_translations(DEFAULT_LOCALE)

    return translations.get(
        key,
        default_translations.get(key, fallback if fallback is not None else key),
    )
