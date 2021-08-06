from __future__ import annotations

from pathlib import Path
from string import Template
from typing import AnyStr, Dict, Union

import yaml

from Skyfixer.config import logger


class Language:
    __slots__ = ("language_name", "phrases")

    def __init__(self, language_name: AnyStr, phrases: Dict[AnyStr, AnyStr]):
        if len(language_name) > 20:
            raise ValueError(f"Too long language name: {language_name}")

        self.language_name = language_name
        self.phrases = {
            k: Template(v) for k, v in phrases.items()
            if isinstance(v, str) and (0 < len(v) <= 2000)
        }

    def keys(self) -> set:
        return set(self.phrases.keys())

    def validate_translation(self, reference_translation: Language):
        reference_keys = reference_translation.keys()
        current_translation_keys = self.keys()
        total_keys_count = len(reference_keys)
        valid_keys_count = total_keys_count

        for key in reference_keys:
            if key not in current_translation_keys:
                valid_keys_count -= 1

        if total_keys_count != valid_keys_count:
            logger.warn(
                f"Translator: Language {self.language_name} has {round(valid_keys_count / total_keys_count, 2)}% "
                "of valid keys, compared to reference language"
            )

    def translate(self, key: AnyStr):
        return self.phrases[key]

    @classmethod
    def load_from_file(cls, language_name: str, file_path: Union[str, Path]):
        with open(file_path) as f:
            localisation = yaml.safe_load(f)

        return cls(language_name, localisation)

    def __hash__(self):
        return hash(self.language_name)
