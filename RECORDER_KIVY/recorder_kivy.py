from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty




kv='''
#: import audio_player plyer.audio

<Audiointerface>:
    audio: audio_player
    orientation: 'vertical'
    padding: '250dp'
    spacing: '20dp'

    MDLabel:
        id: state
        text: 'Audio is :'+str(root.audio.state) 
        size_hint_y: None
        halign: "center"
        font_style: "H4"
    MDLabel:
        id: audio_location
        text: 'Audio is saved at -'+str(root.audio.file_path) 
        size_hint_y: None
        halign: "center"
        font_style: "H4"     

    MDRectangleFlatButton:
        id: record_button    
        text: "Record"
        pos_hint: {"center_x": 0.5}
        on_release: root.start_recording()

    MDRectangleFlatButton:
        id: play_button
        text: "Play"
        pos_hint: {"center_x": 0.5}
        on_release: root.start_playing()


'''
class Audiointerface(MDBoxLayout):
    audio = ObjectProperty(None)

    has_recording = False

    def start_recording(self):
        state = self.audio.state
        if state == 'stopped':
            self.audio.start_recording()
        if state == 'recording':
            self.audio.stop()
            self.has_recording = True

        self.update_labels()

    def  start_playing(self):  
        state = self.audio.state
        if state == 'playing': 
            self.audio.stop()
        else :
            self.audio.start()   

        self.update_labels()     

    def update_labels(self):
        record_label = self.ids['record_button'] 
        Play_button = self.ids['play_button'] 
        state_label = self.ids['state']

        state = self.audio.state
        Play_button.disabled = not self.has_recording

        state_label.text = 'AudioPlayer State:' + str(state)

        if state == 'ready':
            record_label.text = 'Start Recording'

        if state == 'recording':
            record_label.text = 'Stop Recording'
            Play_button.disabled = True
        if state == 'playing':
            Play_button.text = 'Stop Audio'
            record_label.disabled = True
        else:
            Play_button.text = 'Play Audio'
            record_label.disabled = False




    def stop_recording(self):

        self.audio.stop_recording()
           



class AudioApp(MDApp):

    def build(self):
        Builder.load_string(kv)
        return Audiointerface()
       

if __name__ == "__main__":


    AudioApp().run() 
