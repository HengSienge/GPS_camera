from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from plyer import gps
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class GPSCameraApp(App):
    def build(self):
        self.gps_location = "Waiting for GPS..."
        self.img_widget = Image()
        self.layout = BoxLayout(orientation='vertical')

        # GPS Info
        self.gps_label = Label(text=self.gps_location, size_hint=(1, 0.1))
        self.layout.add_widget(self.gps_label)

        # Camera Display
        self.layout.add_widget(self.img_widget)

        # Buttons
        self.capture_button = Button(text="Capture Image", size_hint=(1, 0.1))
        self.capture_button.bind(on_press=self.capture_image)
        self.layout.add_widget(self.capture_button)

        # Start Camera
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update_camera, 1.0 / 30.0)

        # Start GPS
        gps.configure(on_location=self.update_gps)
        gps.start(minTime=1000, minDistance=0)

        return self.layout

    def update_camera(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convert BGR to RGB for displaying in Kivy
            buffer = cv2.flip(frame, 0).tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buffer, colorfmt='bgr', bufferfmt='ubyte')
            self.img_widget.texture = texture

    def capture_image(self, instance):
        ret, frame = self.capture.read()
        if ret:
            # Save the captured image with GPS coordinates
            file_name = "captured_image.jpg"
            cv2.putText(frame, self.gps_location, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
            cv2.imwrite(file_name, frame)
            print(f"Image saved as {file_name} with GPS overlay.")

    def update_gps(self, **kwargs):
        self.gps_location = f"Lat: {kwargs['lat']}, Lon: {kwargs['lon']}"
        self.gps_label.text = self.gps_location

    def on_stop(self):
        # Stop GPS and Camera
        gps.stop()
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    GPSCameraApp().run()
