from kivymd.uix.relativelayout import MDRelativeLayout

from kivy.properties import StringProperty
from kivy.clock import Clock

class Password(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

    def setText(self, *args):
        self.ids.text_field.text = ""
        self.text = ""

    def getFocus(self):
        Clock.schedule_once(self.setText, 0.5)
        self.ids.text_field.text = ""