import sys
import os

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.append(root_dir)

from src.format.formatting import format_text, BLACK, GREEN, BLUE, RED, WHITE, SMALL_SIZE, MEDIUM_SIZE, LARGE_SIZE
from kivy.core.text import LabelBase

class TitlePage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        title_label = MDLabel(
            text=format_text('Welcome to\nDIABETEST!', color=BLACK, size=LARGE_SIZE),
            font_style='H2',
            halign='center',
            markup=True
        )
        start_button = MDRaisedButton(
            text=format_text('Get Started', color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=GREEN,
            on_release=self.go_to_consent
        )
        
        layout.add_widget(title_label)
        layout.add_widget(start_button)
        self.add_widget(layout)

    def go_to_consent(self, instance):
        self.manager.current = 'consent'

class ConsentPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=dp(10))
        title_label = MDLabel(
            text=format_text('User Consent', color=BLACK, size=LARGE_SIZE),
            font_style='H2',
            height=dp(100),
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
            consent_label = MDLabel(
                text = text,
                font_style='Body1',
                size_hint_y=None,
                height=dp(50)
            )
            text_container.add_widget(consent_label)
        
        consent_text = MDLabel(
            text=format_text("Diabe-test is an application for early type 2\n"
                             "diabetes for those within 21-40 years old. Using\n"
                             "this application requires the user to upload a\n"
                             "facial image. Rest assured that all data obtained\n"
                             "will be handled with utmost privacy and\n"
                             "confidentiality.", 
                    color=BLACK, 
                    size=SMALL_SIZE),
            font_style='Body1',
            size_hint_y=None,
            height=dp(600),
            markup=True
        )
        agree_button = MDRaisedButton(
            text=format_text('I Agree', size=SMALL_SIZE, color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=GREEN,
            on_release=self.go_to_upload
        )

        back_button = MDRaisedButton(
            text='Back',
            size_hint=(None, None), 
            size=(dp(120), dp(50)), 
            md_bg_color=RED,
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_release=self.go_back)
        
        layout.add_widget(title_label)
        layout.add_widget(text_container)
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
        self.layout = BoxLayout(orientation='vertical', spacing=20)

        self.error_label = Label(
            text=format_text(text='Error: please upload a facial image', color=RED),
            size_hint_y=None,
            height=dp(20),
            opacity=0  # Initially hidden
        )

        title_label = Label(
            text=format_text('Upload Image', color=BLACK, size=LARGE_SIZE),
            size_hint_y=None,
            height=dp(50),
            markup=True
        )
        upload_button = Button(
            text=format_text('Choose Photo', size=SMALL_SIZE, color=WHITE),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.6, 0.8, 1, 1),
            markup=True
        )
        upload_button.bind(on_release=self.choose_photo)

        back_button = Button(
            text='Back',
            size_hint_y=None,
            height=dp(50),
            background_color=(1, 0.6, 0.6, 1)
        )
        back_button.bind(on_release=self.go_back)

        self.submit_button = Button(
            text=format_text('Submit', size=SMALL_SIZE, color=WHITE),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.6, 0.8, 1, 1),
            markup=True,
            disabled=True  # Initially disabled
        )
        self.submit_button.bind(on_release=self.go_to_processing)

        self.layout.add_widget(title_label)
        self.layout.add_widget(upload_button)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.error_label)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def choose_photo(self, instance):
        file_chooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        file_chooser.bind(on_submit=lambda value: self.on_file_selected(value))  # Fixed lambda function
        popup = Popup(title='Choose Photo', content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    def on_file_selected(self, value):
        if value:
            self.submit_button.disabled = False
            self.error_label.opacity = 0  # Hide error message
        else:
            self.submit_button.disabled = True
            self.error_label.opacity = 1  # Show error message

    def go_to_processing(self, instance):
        if not self.submit_button.disabled:
            self.manager.current = 'processing'
        else:
            Snackbar(text='Error: Please upload a facial image').show()  # Display error message using Snackbar

    def go_back(self, instance):
        self.manager.current = 'consent'
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10))

        self.error_label = MDLabel(
            text=format_text(text='Error: please upload a facial image', color=RED),
            size_hint_y=None,
            height=dp(20),
            opacity=0  # Initially hidden
        )

        title_label = MDLabel(
            text=format_text('Upload Image', color=BLACK, size=LARGE_SIZE),
            size_hint_y=None,
            height=dp(50),
            markup=True
        )
        upload_button = MDRaisedButton(
            text=format_text('Choose Photo', size=SMALL_SIZE, color=WHITE),
            size_hint_y=None,
            height=dp(50),
            md_bg_color=GREEN,
            on_release=self.choose_photo
        )

        back_button = MDRaisedButton(
            text='Back',
            size_hint_y=None,
            height=dp(50),
            md_bg_color=RED
        )
        back_button.bind(on_release=self.go_back)

        self.submit_button = MDRaisedButton(
            text=format_text('Submit', size=SMALL_SIZE, color=WHITE),
            size_hint_y=None,
            height=dp(50),
            md_bg_color=GREEN,
            disabled=True  # Initially disabled
        )
        self.submit_button.bind(on_release=self.go_to_processing)

        self.layout.add_widget(title_label)
        self.layout.add_widget(upload_button)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(self.error_label)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def choose_photo(self, instance):
        file_chooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        file_chooser.bind(on_submit=lambda instance, value: self.on_file_selected(instance, value))  # Use lambda to pass arguments correctly
        popup = Popup(title='Choose Photo', content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    def on_file_selected(self, instance, value):
        if value:
            self.submit_button.disabled = False
            self.error_label.opacity = 0  # Hide error message
        else:
            self.submit_button.disabled = True
            self.error_label.opacity = 1  # Show error message

    def go_to_processing(self, instance):
        if not self.submit_button.disabled:
            self.manager.current = 'processing'
        else:
            Snackbar(text='Error: Please upload a facial image').show()

    def go_back(self, instance):
        self.manager.current = 'consent'


class ProcessingPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=dp(20))
        processing_label = MDLabel(
            text=format_text('Your photo is being processed...\nPlease wait', color=BLACK, size=MEDIUM_SIZE),
            font_style='H2',
            halign='center',
            markup=True
        )
        layout.add_widget(processing_label)
        self.add_widget(layout)


class MyApp(MDApp):
    def build(self):
        Window.size = (360, 640)
        sm = ScreenManager()
        sm.add_widget(TitlePage(name='title'))
        sm.add_widget(ConsentPage(name='consent'))
        sm.add_widget(UploadPage(name='upload'))
        sm.add_widget(ProcessingPage(name='processing'))

        # Create a BoxLayout with a light gray background
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
    #LabelBase.register(name='FreeSansBold', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\FreeSansBold.ttf')
    #LabelBase.register(name='FreeSans', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\FreeSans.ttf')
    LabelBase.register(name='Times', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\Times New Roman.ttf')
    MyApp().run()
