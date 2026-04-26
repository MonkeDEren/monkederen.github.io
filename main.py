from itertools import permutations
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView


def fixed_permutations(word, req_word_len, fixed_data):
    """fixed_data = [(letter, index), ...]"""
    result = []
    for p in permutations(word, req_word_len):
        if all(p[idx - 1] == letter for letter, idx in fixed_data):
            result.append("".join(p))
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
            self.output_text = "\n".join(results) if results else "No results found."

        except Exception as e:
            self.output_text = f"Error: {e}"


class PermutationApp(App):
    def build(self):
        # FIXED: explicitly load your KV file
        self.load_kv("permapp.kv")
        return MainWidget()


if __name__ == "__main__":
    PermutationApp().run()
