from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.graphics import Color, Rectangle
from plyer import gps, camera
import requests
from datetime import datetime

class GPSCameraApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=15)

        self.layout.add_widget(Label(
            text="GPS Camera App", 
            font_size=32,
            bold=True,
            size_hint=(1, 0.2),
            halign='center',
            valign='middle',
            color=(0, 0.5, 0.8, 1)))

        self.layout.add_widget(Label(text="Enter Username:", font_size=18, color=(0.3, 0.3, 0.3, 1)))
        self.username_input = TextInput(multiline=False, hint_text="Your username", size_hint=(1, 0.1))
        self.layout.add_widget(self.username_input)

        self.layout.add_widget(Label(text="Enter Email:", font_size=18, color=(0.3, 0.3, 0.3, 1)))
        self.email_input = TextInput(multiline=False, hint_text="Your email address", size_hint=(1, 0.1))
        self.layout.add_widget(self.email_input)

        self.verify_button = Button(
            text="Verify Email", 
            background_color=(0.1, 0.7, 0.3, 1),
            size_hint=(1, 0.1))
        self.verify_button.bind(on_press=self.verify_email)
        self.layout.add_widget(self.verify_button)

        self.layout.add_widget(Label(size_hint=(1, 0.05), text=""))

        self.photo_button = Button(
            text="Take and Submit Photo", 
            background_color=(0.2, 0.5, 0.8, 1),
            size_hint=(1, 0.1))
        self.photo_button.bind(on_press=self.take_photo)
        self.layout.add_widget(self.photo_button)

        self.status_label = Label(
            text="Status will appear here.",
            font_size=14,
            italic=True,
            size_hint=(1, 0.2),
            color=(0.5, 0.2, 0.2, 1))
        self.layout.add_widget(self.status_label)

        return self.layout

    def verify_email(self, instance):
        email = self.email_input.text
        if "@" in email and "." in email:
            self.status_label.text = "\nEmail verified!"
            self.status_label.color = (0, 0.6, 0, 1)
        else:
            self.status_label.text = "\nInvalid email. Please try again."
            self.status_label.color = (0.8, 0, 0, 1)

    def take_photo(self, instance):
        try:
            camera.take_picture('photo.jpg', self.on_photo_taken)
        except NotImplementedError:
            self.status_label.text = "Camera not supported on this device."

    def on_photo_taken(self, path):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            with open(path, 'rb') as photo:
                response = requests.post("http://your-server-url/submit", data={
                    'username': self.username_input.text,
                    'email': self.email_input.text,
                    'timestamp': timestamp
                }, files={'photo': photo})
                if response.status_code == 200:
                    self.status_label.text = "\nPhoto submitted successfully!"
                    self.status_label.color = (0, 0.6, 0, 1)
                else:
                    self.status_label.text = "\nSubmission failed."
                    self.status_label.color = (0.8, 0, 0, 1)
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"

    def on_location(self, **kwargs):
        lat = kwargs['lat']
        lon = kwargs['lon']
        self.status_label.text = f"\nLocation: {lat}, {lon}"
        gps.stop()

if __name__ == "__main__":
    GPSCameraApp().run()