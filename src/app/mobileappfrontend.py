from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.config import Config

Config.set('graphics', 'height', '640')
Config.set('graphics', 'width', '360')

class TitlePage(Screen):
    """Diabe-test title page"""

    def __init__(self, **kwargs):
        super(TitlePage, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Your widgets here
        label = TextInput(text='Your agreement text here', multiline=True)
        layout.add_widget(label)

        self.add_widget(layout)

    def _press_login(self):
        """Login button on_press."""
        self.ids["Get Started"].color = (
            1., 1., 1., 1
        )
        self.ids["Get Started"].background_color = (
            .47734375, .5125, .64375, 1
        )

class ConsentPage(BoxLayout):
    """Diabe-test consent page"""

    def __init__(self, **kwargs):
        super(ConsentPage, self).__init__(**kwargs)

        # Your widgets here

    def _press_agree(self):
        """Agree button on_press."""
        self.ids["Agree"].color = (
            1., 1., 1., 1
        )
        self.ids["Agree"].background_color = (
            .47734375, .5125, .64375, 1
        )

class Diabetest(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()

        # Add screens to the screen manager
        title_page = TitlePage(name='title')
        agreement_page = ConsentPage()
        sm.add_widget(title_page)
        sm.add_widget(agreement_page)

        return sm

if __name__ == '__main__':
    Diabetest().run()

