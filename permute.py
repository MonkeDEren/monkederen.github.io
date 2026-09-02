from itertools import permutations
from my_dictionary import DICTIONARY

def fixed_permutations(word, req_word_len, fixed_data):
    """fixed_data = [(letter, index), ...] with 1-based index.

    Returns unique, genuine-word permutations only:
    - Duplicate letter arrangements (from repeated letters in `word`) are
      collapsed to a single result.
    - Each candidate must satisfy the fixed letter/position constraints.
    - If a dictionary was loaded, each candidate must also be a real word.
      If no dictionary could be loaded, this check is skipped (all unique,
      constraint-matching arrangements are returned instead).

    Raises ValueError if a fixed position is out of range for the
    requested word length, so the caller can show a clear error instead
    of silently ignoring the constraint or crashing.
    """
    for letter, idx in fixed_data:
        if idx < 1 or idx > req_word_len:
            raise ValueError(
                f"Position {idx} is out of range - it must be between "
                f"1 and {req_word_len}."
            )
        if len(letter) != 1:
            raise ValueError(f"'{letter}' is not a single letter.")

    seen = set()
    result = []

    for p in permutations(word, req_word_len):
        candidate = "".join(p)
        key = candidate.lower()

        if key in seen:
            continue  # already produced this exact arrangement

        if not all(p[idx - 1].lower() == letter.lower() for letter, idx in fixed_data):
            continue

        if DICTIONARY and key not in DICTIONARY:
            continue  # not a genuine dictionary word

        seen.add(key)
        result.append(candidate)

    return result