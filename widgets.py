from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty
from permute import fixed_permutations
from my_dictionary import DICTIONARY


class MainWidget(BoxLayout):
    output_text = StringProperty("Results will appear here.")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fixed_inputs = []

        self.ids.spinner.bind(text=self.update_fixed_inputs)

    def update_fixed_inputs(self, spinner, value):
        self.ids.fixed_input_area.clear_widgets()
        self.fixed_inputs.clear()

        count = int(value[0])  # '1 Letter Fixed' -> 1
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
                input_filter="int",
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
                if not letter or not index_text:
                    continue  # skip blank rows instead of erroring
                fixed_data.append((letter, int(index_text)))

            results = fixed_permutations(word, req_word_len, fixed_data)

            if not DICTIONARY:
                note = "⚠ No dictionary loaded - showing unique letter arrangements (not filtered to real words).\n\n"
                self.output_text = note + ("\n".join(results) if results else "No results found.")
            else:
                self.output_text = "\n".join(results) if results else "No genuine words found."

        except ValueError as e:
            self.output_text = f"Input error: {e}"
        except Exception as e:
            self.output_text = f"Error: {e}"

