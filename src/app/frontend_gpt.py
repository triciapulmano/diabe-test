import sys
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp


root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.append(root_dir)

from src.format.formatting import format_text, BLACK, GREEN, BLUE, WHITE, SMALL_SIZE, MEDIUM_SIZE, LARGE_SIZE

from kivy.core.text import LabelBase

class TitlePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=20)
        title_label = Label(
            text=format_text('Welcome to\nDIABETEST!', color=BLACK, size=LARGE_SIZE),
            font_name='FreeSansBold',
            size_hint_y=None,
            height = 1000,
            width = 100, 
            markup=True
        )
        start_button = Button(
            text=format_text('Get Started', color=WHITE),
            size_hint=(None, None),
            size=(200, 50),
            background_color=(0.6, 0.8, 1, 1),
            pos_hint={'center_x': 0.5, 'y': 0.3},
            markup=True
        )
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
        title_label = Label(
            text=format_text('User Consent', color=BLACK, size=LARGE_SIZE),
            font_name='FreeSansBold',
            size_hint_y=None,
            height = 50,
            width = 100, 
            markup=True
        )

        text_container = BoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )

        # Add your consent text labels to the text container
        consent_texts = [
            "Diabe-test is an application for early type 2 diabetes for those within 21-40 years old.",
            "Using this application requires the user to upload a facial image.",
            "Rest assured that all data obtained will be handled with utmost privacy and confidentiality."
        ]
        for text in consent_texts:
            consent_label = Label(
                text = text,
                font_size = 14,
                size_hint_y = None,
                height = dp(50)
            )
        text_container.add_widget(consent_label)
        layout.add_widget(text_container)

        consent_text = Label(
            text=format_text("Diabe-test is an application for early type 2\n"
                             "diabetes for those within 21-40 years old. Using\n"
                             "this application requires the user to upload a\n"
                             "facial image. Rest assured that all data obtained\n"
                             "will be handled with utmost privacy and\n"
                             "confidentiality.", 
                    color=BLACK, 
                    size=SMALL_SIZE),
            font_name='FreeSans',
            size_hint_y=None,
            height = 600,
            width = 100, 
            markup=True
        )
        agree_button = Button(
            text=format_text('I Agree', size=SMALL_SIZE, color=WHITE),
            size_hint=(None, None),
            background_color=(0.6, 0.8, 1, 1),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'y': 0.7},
            markup=True
        )
        agree_button.bind(on_release=self.go_to_upload)

        back_button = Button(
            size_hint=(None, None), 
            size=(50, 50), 
            pos=(0, 750), 
            background_normal='circle.png', 
            background_down='circle.png'
        )
        back_button.bind(on_release=self.go_back)
        
        layout.add_widget(title_label)
        layout.add_widget(consent_text)
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
        layout = FloatLayout(size=(360, 640))
        title_label = Label(
            text=format_text('Upload Image', color=BLACK, size=LARGE_SIZE),
            font_name='FreeSansBold',
            size_hint_y=None,
            pos_hint={'center_x': 0.5, 'top': 0.9},
            markup=True
        )
        upload_button = Button(
            text=format_text('Choose Photo', size = SMALL_SIZE, color=WHITE), 
            size_hint=(None, None),  
            pos_hint={'center_x': 0.5, 'center_y': 0.6}, 
            background_color=(0.6, 0.8, 1, 1),
            size=(200, 50),
            markup=True
        )
        
        upload_button.bind(on_release=self.choose_photo)
        submit_button = Button(
            text=format_text('Submit', size = SMALL_SIZE, color=WHITE),
            size_hint=(None, None), 
            size=(200, 50), 
            pos_hint={'center_x': 0.5, 'y': 0.05}, 
            background_color=(0.6, 0.8, 1, 1),
            markup=True
        )

        back_button = Button(
            size_hint=(None, None), 
            size=(50, 50), 
            pos=(0, 750), 
            background_normal='circle.png', 
            background_down='circle.png'
        )
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
        Window.size = (360, 640)
        sm = ScreenManager()
        sm.add_widget(TitlePage(name='title'))
        sm.add_widget(ConsentPage(name='consent'))
        sm.add_widget(UploadPage(name='upload'))

        # Create a BoxLayout with a gray background
        root = BoxLayout(orientation='vertical', size=(360, 640))
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
    LabelBase.register(name='FreeSansBold', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\FreeSansBold.ttf')
    LabelBase.register(name='FreeSans', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\FreeSans.ttf')
    MyApp().run()
