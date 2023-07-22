import unicodedata


def remove_accents(word: str) -> str:
    """
    Removes accents from a word.
    "петру́шка" -> "петрушка"

    word: The word to remove accents from.
    Returns: The word without accents.
    """

    # Get the unicode decomposition of the word.
    decomposition = unicodedata.normalize("NFKD", word)

    # Remove all characters that are not letters.
    letters = "".join(c for c in decomposition if unicodedata.combining(c) == 0)

    # Return the word with accents removed.
    return letters

