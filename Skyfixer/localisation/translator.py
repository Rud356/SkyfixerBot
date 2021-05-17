from functools import lru_cache
from string import Template
from typing import AnyStr, Dict, List, Set

from Skyfixer.config import skyfixer_localisation
from .language import Language


class Translator:
    def __init__(self, reference_language: str, loaded_languages: List[Language]):
        self.languages: Dict[AnyStr, Language] = {lang.language_name: lang for lang in loaded_languages}

        try:
            self.reference_language = self.languages.pop(reference_language)

        except KeyError:
            print(f"No reference language with name {reference_language} found")
            print("Check configuration files")
            exit(-1)

        for language in self.languages.values():
            language.validate_translation(self.reference_language)

    def get_language(self, language_name: AnyStr) -> Language:
        """
        Gives some language and if not found specified one - gives default language.

        :param language_name: language name string.
        :return: Language instance.
        """
        return self.languages.get(language_name, self.reference_language)

    def translate(self, key: AnyStr, to_language: AnyStr) -> Template:
        language = self.get_language(to_language)

        try:
            return language.translate(key)

        except KeyError:
            if language is not self.reference_language:
                return self.translate(key, self.reference_language)

            else:
                raise self.exc.TranslationError()

    @property
    @lru_cache(None)
    def languages_set(self) -> Set[AnyStr]:
        return set(self.languages.keys())

    @classmethod
    def load_languages(cls):
        languages = set()

        for language_file in skyfixer_localisation.supported_languages_files:
            language = Language.load_from_file(language_file.stem, language_file)
            languages.add(language)

        return cls(skyfixer_localisation.reference_language.value, list(languages))

    class exc:
        class TranslationError(ValueError):
            pass
