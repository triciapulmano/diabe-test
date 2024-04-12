import sys
import os
import cv2
import numpy as np
import requests
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivymd.app import MDApp
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivymd.uix.snackbar import Snackbar

# from android.permissions import request_permissions, Permission
# from android.storage import primary_external_storage_path

from blockExtraction import face_detection
from gabor import preprocess_image, extract_gabor_features
from server import process_features

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
            markup=True,
            pos_hint={"center_x": 0.5, "center_y": 0.8} 
        )
    
        start_button = MDRaisedButton(
            text=format_text('Get Started', color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 0.25},  
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
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10))
        self.image_data = None  # Variable to store image data
        self.file_chooser = None 
        self.error_label = Label(text='', color=(1, 0, 0, 1))  # Error label with red color
        self.filename_label = Label(text='', color=(0, 0, 0, 1), size_hint_y=None, height=dp(50))

        title_label = Label(
            text=format_text('Upload Image', color=BLACK, size=LARGE_SIZE),
            size_hint_y=None,
            height=dp(50),
            markup=True
        )

        upload_button = MDRaisedButton(
            text=format_text('Choose Photo', size=SMALL_SIZE, color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=GREEN
        )
        upload_button.bind(on_release=self.choose_photo)

        back_button = MDRaisedButton(
            text=format_text('Back', size=SMALL_SIZE, color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=RED
        )
        back_button.bind(on_release=self.go_back)
        
        self.submit_button = MDRaisedButton(
            text=format_text('Submit', size=SMALL_SIZE, color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5},
            md_bg_color=BLUE,
            disabled=True  # Initially disabled
        )
        self.submit_button.bind(on_release=self.on_submit)

        self.layout.add_widget(title_label)
        self.layout.add_widget(self.filename_label)  
        self.layout.add_widget(upload_button)
        self.layout.add_widget(self.submit_button)
        self.layout.add_widget(back_button)
        self.add_widget(self.layout)

    def on_enter(self):
        super().on_enter()
        self.filename_label.text = ''

    def choose_photo(self, instance):
        self.file_chooser = FileChooserListView(filters=['*.jpg', '*.jpeg', '*.png'])
        
        select_button = MDRaisedButton(
            text="Select",
            size_hint_y=None,
            height=dp(50),
            on_release=lambda instance: self.on_file_selected(instance, self.file_chooser.selection) if self.file_chooser.selection else None
        )

        layout = BoxLayout(orientation='vertical', spacing=10)
        layout.add_widget(self.file_chooser)
        layout.add_widget(select_button)

        self.popup = Popup(title='Choose Photo', content=layout, size_hint=(None, None), size=(400, 400))
        self.popup.open()

    def on_file_selected(self, instance, value):
        if value:
            selected_file = value[0]
            self.submit_button.disabled = False
            self.error_label.opacity = 0  # Hide error message
            self.filename_label.text = f'Chosen File: {selected_file}' 
        else:
            self.submit_button.disabled = True
            self.error_label.opacity = 1  # Show error message
        
        self.popup.dismiss()  # Close the popup
    
    def on_submit(self, instance):
        print(self.file_chooser, self.file_chooser.selection)
        if self.file_chooser.selection:
            selected_file = self.file_chooser.selection[0]
            self.process_image(selected_file)
        else:
            print("Error: No file selected.")


    def process_image(self, selected_file):
        with open(selected_file, 'rb') as file:
            selected_file = file.read()

        if selected_file is not None: 
            blocks = [] 
            blocks = face_detection(selected_file)

            #TODO: save_path for android
            save_path = r"D:\downloads dump\test"  
            os.makedirs(save_path, exist_ok=True)  

            # Perform Gabor filter and texture analysis for each block
            texture_features = []
            for i, block in enumerate(blocks):
                for j, chunk in enumerate(block):
                    filename = os.path.join(save_path, f'block_{i}_{j}.jpg')
                    cv2.imwrite(filename, chunk)
                    grayscale = preprocess_image(filename)
                    features = extract_gabor_features(grayscale)
                    texture_features.append(features)

            print(texture_features)

            # Send texture features to the server for classification
            url = 'http://127.0.0.1:5000/process_features'
            # url = 'http://192.168.254.104:8080/process_features'  # Update URL with your server's address
            data = {'features': texture_features}
            response = requests.get(url, json=data)

            if response.status_code == 200:
                prediction_data = response.json()  # Get the JSON response
                prediction_value = prediction_data.get('prediction')[0] # Extract 'prediction' value from JSON
                
                result_page = self.manager.get_screen('result')
                result_page.prediction = prediction_value
                result_page.update_result_label_text()  

                self.manager.current = 'result'
            else:
                print("Error occurred while sending data to server.")
        
        else:
            print("Error: No image data available.")

    def go_back(self, instance):
        self.manager.current = 'consent'

class ResultPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=dp(10))
        self.prediction = None # Variable to store prediction

        title_label = Label(
            text=format_text('Result', color=BLACK, size=LARGE_SIZE),
            size_hint_y=None,
            height=dp(50),
            markup=True
        )

        self.result_label = MDLabel(
            text=self.get_result_label_text(),
            font_style='Body1',
            size_hint_y=None,
            height=dp(100)
        )
        ok_button = MDRaisedButton(
            text=format_text('OK', color=WHITE),
            size_hint=(None, None),
            size=(dp(200), dp(50)),
            pos_hint={'center_x': 0.5, 'center_y': 1},  
            md_bg_color=GREEN,
            on_release=self.go_to_title
        )
        
        self.layout.add_widget(title_label)
        self.layout.add_widget(self.result_label)
        self.layout.add_widget(ok_button)
        self.add_widget(self.layout)


    def get_result_label_text(self):
        print(f"Prediction type in get_result_label_text: {type(self.prediction)}")
        print(f"Prediction value in get_result_label_text: {self.prediction}") 
        if self.prediction is None:
            return "Classification result unknown"
        elif self.prediction == 0:
            return "User is classified as not Type 2 diabetic"
        elif self.prediction == 1:
            return "User is classified as possibly Type 2 diabetic. Please consult a doctor to verify diagnosis."
        else:
            return "Invalid prediction value"

    def update_result_label_text(self):
        self.result_label.text = self.get_result_label_text()

    def go_to_title(self, instance):
        result_screen = self.manager.get_screen('result')
        result_screen.clear_uploadimage()
        self.manager.current = 'title'

    def clear_uploadimage(self):
        # Reset image_data to None and disable submit button in UploadPage
        upload_page = self.manager.get_screen('upload')
        upload_page.image_data = None
        upload_page.submit_button.disabled = True

        # Delete the photos created within process_image to ensure data confidentiality
        save_path = r"D:\downloads dump\test"
        if os.path.exists(save_path):  # Check if the directory exists
            for filename in os.listdir(save_path):
                file_path = os.path.join(save_path, filename)
                try:
                    os.remove(file_path)  # Remove the file
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

                    
class MyApp(MDApp):
    def build(self):
        # Window.size = (720, 1600)
        Window.size = (360, 640)
        sm = ScreenManager()

        sm.add_widget(TitlePage(name='title'))
        sm.add_widget(ConsentPage(name='consent'))
        sm.add_widget(UploadPage(name='upload'))
        sm.add_widget(ResultPage(name='result'))
        
        # Create a BoxLayout with a light gray background
        # root = BoxLayout(orientation='vertical', size=(720, 1600))
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
    LabelBase.register(name='Times', fn_regular=r'C:\Users\ASUS\OneDrive\Documents\diabetes app\assets\fonts\Times New Roman.ttf')
    MyApp().run()
