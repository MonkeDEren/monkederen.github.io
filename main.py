import os
from itertools import permutations
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView


def load_dictionary():
    """Load a set of valid English words used to filter permutations.

    Tries nltk's bundled 'words' corpus first (great coverage, one-time
    download). Falls back to a local 'words.txt' file placed next to this
    script (one word per line) so the app can still work fully offline
    without nltk installed, e.g. for the APK build.
    """
    words = set()

    try:
        import nltk
        try:
            from nltk.corpus import words as nltk_words
            words = set(w.lower() for w in nltk_words.words())
        except LookupError:
            # Corpus not downloaded yet - try fetching it once.
            nltk.download("words")
            from nltk.corpus import words as nltk_words
            words = set(w.lower() for w in nltk_words.words())
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


def fixed_permutations(word, req_word_len, fixed_data):
    """fixed_data = [(letter, index), ...]

    Returns unique, genuine-word permutations only:
    - Duplicate letter arrangements (from repeated letters in `word`) are
      collapsed to a single result.
    - Each candidate must satisfy the fixed letter/position constraints.
    - If a dictionary was loaded, each candidate must also be a real word.
      If no dictionary could be loaded, this check is skipped (all unique,
      constraint-matching arrangements are returned instead).
    """
    seen = set()
    result = []

    for p in permutations(word, req_word_len):
        candidate = "".join(p)
        key = candidate.lower()

        if key in seen:
            continue  # already produced this exact arrangement

        if not all(p[idx - 1] == letter for letter, idx in fixed_data):
            continue

        if DICTIONARY and key not in DICTIONARY:
            continue  # not a genuine dictionary word

        seen.add(key)
        result.append(candidate)

    return result


class MainWidget(BoxLayout):
    output_text = StringProperty("Results will appear here.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fixed_inputs = []

        # FIXED: spinner must be accessed via ids
        self.ids.spinner.bind(text=self.update_fixed_inputs)

    def update_fixed_inputs(self, spinner, value):
        # Clear old inputs
        self.ids.fixed_input_area.clear_widgets()
        self.fixed_inputs.clear()

        count = int(value[0])  # '1 Letter Fixed' → 1
        for i in range(count):
            box = BoxLayout(spacing=10, size_hint_y=None, height=40)

            letter_in = TextInput(
                hint_text=f"Letter {i+1}",
                multiline=False,
                background_color=(0.2, 0.2, 0.3, 1),
                foreground_color=(1, 1, 1, 1)
            )

            index_in = TextInput(
                hint_text=f"Position {i+1}",
                multiline=False,
                background_color=(0.2, 0.2, 0.3, 1),
                foreground_color=(1, 1, 1, 1)
            )

            box.add_widget(letter_in)
            box.add_widget(index_in)
            self.ids.fixed_input_area.add_widget(box)
            self.fixed_inputs.append((letter_in, index_in))

    def generate(self):
        try:
            word = self.ids.word_input.text.strip()
            req_word_len = int(self.ids.length_input.text.strip())

            fixed_data = []
            for letter_in, index_in in self.fixed_inputs:
                letter = letter_in.text.strip()
                index = int(index_in.text.strip())
                fixed_data.append((letter, index))

            results = fixed_permutations(word, req_word_len, fixed_data)

            if not DICTIONARY:
                note = "⚠ No dictionary loaded - showing unique letter arrangements (not filtered to real words).\n\n"
                self.output_text = note + ("\n".join(results) if results else "No results found.")
            else:
                self.output_text = "\n".join(results) if results else "No genuine words found."

        except Exception as e:
            self.output_text = f"Error: {e}"


class PermutationApp(App):
    def build(self):
        # FIXED: explicitly load your KV file
        self.load_kv("permapp.kv")
        return MainWidget()


if __name__ == "__main__":
    PermutationApp().run()