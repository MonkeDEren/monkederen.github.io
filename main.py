
from kivy.app import App
from widgets import MainWidget


class PermutationApp(App):
    def build(self):
        self.load_kv("permapp.kv")
        return MainWidget()
# I am teaching guthub to MObina

if __name__ == "__main__":
    PermutationApp().run()
