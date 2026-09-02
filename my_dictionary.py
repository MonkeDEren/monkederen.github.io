import os
import nltk
def load_dictionary():
    """Load a set of valid English words used to filter permutations.

    Tries nltk's bundled 'words' corpus first, but ONLY if it is already
    downloaded/cached - we never trigger a network download here, since
    that would block app startup (and fail outright on Android, which has
    no internet access by default in this app). Falls back to a local
    'words.txt' file placed next to this script (one word per line) so
    the app works fully offline, which is what actually ships in the APK.
    """
    words = set()

    try:
       
        from nltk.corpus import words as nltk_words
        try:
            words = set(w.lower() for w in nltk_words.words())
        except LookupError:
            # Corpus isn't cached locally - skip it silently instead of
            # blocking on a network download. words.txt fallback below
            # will be used instead.
            pass
    except ImportError:
        pass

    if not words:
        local_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "words.txt"
        )
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                words = set(line.strip().lower() for line in f if line.strip())

    return words


# Loaded once at import time so every generate() call reuses it.
DICTIONARY = load_dictionary()
