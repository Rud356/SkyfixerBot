import codecs
import re

_prefix_regex = re.compile(r"^([a-zA-Z!\\\-+=?|$#]){1,2}$")


def validate_prefix(string: str) -> bool:
    result = _prefix_regex.fullmatch(string)
    if result is None:
        raise ValueError(f"Prefix {string} doesn't matches regex")

    return True


def validate_encoding(value: str):
    try:
        codecs.lookup(value)

    except LookupError:
        raise ValueError("Invalid logs encoding")

    return True
