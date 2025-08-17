import json
import os
from typing import Dict


class I18N:
    def __init__(self, default_locale: str = "tr"):
        self.default_locale = default_locale
        self.translations: Dict[str, Dict[str, str]] = {}
        self.current_locale = default_locale
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.load_locale("tr", os.path.join(base_dir, "i18n", "tr.json"))
        self.load_locale("en", os.path.join(base_dir, "i18n", "en.json"))

    def load_locale(self, locale: str, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                self.translations[locale] = json.load(f)
        except Exception:
            self.translations[locale] = {}

    def set_locale(self, locale: str):
        if locale in self.translations:
            self.current_locale = locale

    def t(self, key: str) -> str:
        return self.translations.get(self.current_locale, {}).get(
            key,
            self.translations.get(self.default_locale, {}).get(key, key),
        )
