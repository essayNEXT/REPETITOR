import unicodedata


def remove_accents(word: str) -> str:
    """
    Removes accents from a word.
    "петру́шка" -> "петрушка"

    word: The word to remove accents from.
    Returns: The word without accents.
    """

    # Get the unicode decomposition of the word.
    decomposition = unicodedata.normalize("NFKC", word)
    # print([c for c in decomposition])
    # Remove all characters that are not letters. and c not in ["і","ї","й","ё"]
    letters = "".join(c for c in decomposition if unicodedata.combining(c) == 0)

    # Return the word with accents removed.
    return letters


if __name__ == "__main__":
    word = "петру́шка п'ять іёїй"
    print(remove_accents(word))
