from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle

from kivy.core.text import LabelBase

class TitlePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20)
        title_label = Label(text='diabetest', font_name='FreeSansBold', font_size=60, size_hint_y=None, height=100)
        start_button = Button(text='Get Started', size_hint=(None, None), size=(200, 50), background_color=(0.6, 0.8, 1, 1))
        start_button.bind(on_release=self.go_to_consent)
        layout.add_widget(title_label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_consent(self, instance):
        self.manager.current = 'consent'

class ConsentPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20)
        consent_text = (
            "Diabe-test is an application for early type 2 diabetes for those within 21-40 years old. "
            "Using this application requires the user to upload a facial image. "
            "Rest assured that all data obtained will be handled with utmost privacy and confidentiality."
        )
        consent_label = Label(text=consent_text, font_size=18, font_name='FreeSansBold', size_hint_y=None, height=200)
        agree_button = Button(text='I Agree', size_hint=(None, None), size=(200, 50), background_color=(0.6, 0.8, 1, 1))
        agree_button.bind(on_release=self.go_to_upload)
        
        back_button = MDIconButton(icon='arrow-left.png', pos_hint={'center_x': 0.1, 'center_y': 0.1}, icon_size="30sp")
        back_button.bind(on_release=self.go_back)
        
        layout.add_widget(consent_label)
        layout.add_widget(agree_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_to_upload(self, instance):
        self.manager.current = 'upload'
        
    def go_back(self, instance):
        self.manager.current = 'title'

class UploadPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        title_label = Label(text='Upload Image', font_size=30, font_name='FreeSansBold', size_hint=(None, None), size=(300, 50), pos_hint={'center_x': 0.5, 'top': 0.9})
        upload_button = Button(text='Choose Photo', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'center_y': 0.6}, background_color=(0.6, 0.8, 1, 1))
        upload_button.bind(on_release=self.choose_photo)
        submit_button = Button(text='Submit', size_hint=(None, None), size=(200, 50), pos_hint={'center_x': 0.5, 'y': 0.05}, background_color=(0.6, 0.8, 1, 1))

        back_button = Button(size_hint=(None, None), size=(50, 50), pos_hint={'x': 0, 'top': 1}, background_normal='circle.png', background_down='circle.png')
        back_button.bind(on_release=self.go_back)

        layout.add_widget(title_label)
        layout.add_widget(upload_button)
        layout.add_widget(submit_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def choose_photo(self, instance):
        file_chooser = FileChooserListView()
        popup = Popup(title='Choose Photo', content=file_chooser, size_hint=(None, None), size=(400, 400))
        file_chooser.bind(on_submit=self.dismiss_popup)
        popup.open()

    def dismiss_popup(self, instance):
        popup = instance.parent.parent
        popup.dismiss()

    def go_back(self, instance):
        self.manager.current = 'consent'

class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(TitlePage(name='title'))
        sm.add_widget(ConsentPage(name='consent'))
        sm.add_widget(UploadPage(name='upload'))

        # Create a BoxLayout with a gray background
        root = BoxLayout(orientation='vertical')
        with root.canvas.before:
            Color(0.9, 0.9, 0.9, 1)  # Set the color to light gray
            self.rect = Rectangle(size=root.size, pos=root.pos)

        root.bind(size=self.update_rect, pos=self.update_rect)
        root.add_widget(sm)
        return root

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
    

if __name__ == '__main__':
    LabelBase.register(name='FreeSansBold', fn_regular='FreeSansBold.ttf')
    MyApp().run()
