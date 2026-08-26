import os
from itertools import permutations

from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


DICTIONARY_FILENAME = "words.txt"


def load_dictionary():
    """Load the bundled English dictionary used for genuine-word filtering."""
    local_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), DICTIONARY_FILENAME
    )

    if not os.path.exists(local_path):
        raise RuntimeError(
            f"Required dictionary '{DICTIONARY_FILENAME}' was not found. "
            "Add it to the project root before building the app."
        )

    with open(local_path, "r", encoding="utf-8") as f:
        words = {line.strip().lower() for line in f if line.strip()}

    if not words:
        raise RuntimeError(f"'{DICTIONARY_FILENAME}' is empty.")

    return words


# Loaded once at import time so every generate() call reuses it.
DICTIONARY = load_dictionary()


def fixed_permutations(word, req_word_len, fixed_data):
    """Return unique dictionary words matching the fixed-position constraints."""
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
            continue

        if not all(
            p[idx - 1].lower() == letter.lower()
            for letter, idx in fixed_data
        ):
            continue

        if key not in DICTIONARY:
            continue

        seen.add(key)
        result.append(candidate)

    return result


class MainWidget(BoxLayout):
    output_text = StringProperty("Results will appear here.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fixed_inputs = []
        self.ids.spinner.bind(text=self.update_fixed_inputs)

    def update_fixed_inputs(self, spinner, value):
        self.ids.fixed_input_area.clear_widgets()
        self.fixed_inputs.clear()

        count = int(value[0])
        for i in range(count):
            box = BoxLayout(spacing=10, size_hint_y=None, height=40)

            letter_in = TextInput(
                hint_text=f"Letter {i + 1}",
                multiline=False,
                background_color=(0.2, 0.2, 0.3, 1),
                foreground_color=(1, 1, 1, 1),
            )

            index_in = TextInput(
                hint_text=f"Position {i + 1}",
                multiline=False,
                input_filter="int",
                background_color=(0.2, 0.2, 0.3, 1),
                foreground_color=(1, 1, 1, 1),
            )

            box.add_widget(letter_in)
            box.add_widget(index_in)
            self.ids.fixed_input_area.add_widget(box)
            self.fixed_inputs.append((letter_in, index_in))

    def generate(self):
        try:
            word = self.ids.word_input.text.strip()
            if not word:
                self.output_text = "Please enter a word."
                return

            length_text = self.ids.length_input.text.strip()
            if not length_text:
                self.output_text = "Please enter a word length."
                return
            req_word_len = int(length_text)

            if req_word_len < 1 or req_word_len > len(word):
                self.output_text = (
                    f"Length must be between 1 and {len(word)} "
                    f"(the length of '{word}')."
                )
                return

            fixed_data = []
            for letter_in, index_in in self.fixed_inputs:
                letter = letter_in.text.strip()
                index_text = index_in.text.strip()
                if not letter and not index_text:
                    continue
                if not letter or not index_text:
                    raise ValueError("Each fixed letter must have a position.")
                fixed_data.append((letter, int(index_text)))

            results = fixed_permutations(word, req_word_len, fixed_data)
            self.output_text = "\n".join(results) if results else "No genuine words found."

        except ValueError as e:
            self.output_text = f"Input error: {e}"
        except Exception as e:
            self.output_text = f"Error: {e}"


class PermutationApp(App):
    def build(self):
        self.load_kv("permapp.kv")
        return MainWidget()


if __name__ == "__main__":
    PermutationApp().run()
