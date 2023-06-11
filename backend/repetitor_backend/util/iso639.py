import iso639
from enum import Enum


class Iso639(str, Enum):
    PART3 = "part3"
    PART2B = "part2b"
    PART2T = "part2t"
    PART1 = "part1"
    NAME = "name"


def iso639_match(lng: str, target: Iso639 = Iso639.PART1) -> str:
    """Translate language name (in the terminology of iso639) to Iso639.
    
    input string are matching in next order:
        ISO 639-3 codes (among the active codes)
        ISO 639-2 (bibliographic) codes
        ISO 639-2 (terminological) codes
        ISO 639-1 codes
        ISO 639-3 codes (among the retired codes)
        ISO 639-3 reference language names
        ISO 639-3 alternative language names (the "print" ones)
        ISO 639-3 alternative language names (the "inverted" ones) 

    if lng no matches any language, return "no match"
    WARNING: returning value may be None
    """
    try:
        lang = iso639.Language.match(lng)
    except iso639.LanguageNotFoundError:
        return "no match"
    if target == Iso639.PART1:
        return lang.part1
    elif target == Iso639.NAME:
        return lang.name
    elif target == Iso639.PART2B:
        return lang.part2b
    elif target == Iso639.PART2T:
        return lang.part2t
    elif target == Iso639.PART3:
        return lang.part3
