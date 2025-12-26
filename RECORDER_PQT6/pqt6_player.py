
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from pqt6_methods import AudioMethods


class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.audio_methods = AudioMethods(self)
        self.event_handler()

  #settings
    def settings(self):
        self.setWindowTitle("Aud-just")
        self.setGeometry(900, 600, 600, 300)



  # Design
    def initUI(self):
        self.title = QLabel("Audio Adjuster")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.song_label = QLabel()
        self.song_label.setStyleSheet("color: green;")
        self.song_label.hide()
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: green;")
        self.time_label.hide()  # Ocúltalo al inicio

        
        

        self.file_list = QListWidget()
        self.btn_opener = QPushButton("Choose a File")
        self.btn_play = QPushButton("Play")
        self.btn_pause = QPushButton("Pause")
        self.btn_resume = QPushButton("Resume")
        self.btn_reset = QPushButton("Reset")
        self.btn_stop = QPushButton("Stop")

        #deactivate buttons for now
        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(True)

     

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(50)    
        self.slider.setMaximum(150)
        self.slider.setValue(100)
        self.slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.slider.setTickInterval(10)

        self.slider_text = QLabel("Speed: 100%")
        self.slider_text.setAlignment(Qt.AlignmentFlag.AlignCenter) 


        slider_layout = QVBoxLayout()
        
        slider_layout.addWidget(self.slider_text)
        slider_layout.addWidget(self.slider)


        #create layouts

        self.master = QVBoxLayout()
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        self.master.addWidget(self.title)
        self.master.addWidget(self.song_label)
        self.master.addWidget(self.time_label)
        self.master.addLayout(slider_layout)


        col1.addWidget(self.file_list)
        col2.addWidget(self.btn_opener)
        col2.addWidget(self.btn_play)
        col2.addWidget(self.btn_pause) 
        col2.addWidget(self.btn_resume)
        col2.addWidget(self.btn_reset) 
        col2.addWidget(self.btn_stop) 

        row.addLayout(col1)
        row.addLayout(col2)

        self.master.addLayout(row)
        self.setLayout(self.master)

        self.style()

        #Special Audio Clases from PyQt6
        self.audio_output = QAudioOutput()
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.positionChanged.connect(self.update_time_label)
        self.media_player.durationChanged.connect(self.set_total_duration)
        self.total_duration = 0  # Inicializa la variable

  # Style methods

    def style(self):
        self.setStyleSheet("""

                            QWidget {
                                background-color: #04274f;
                            }
                            QPushButton {
                                background-color: #529df1;  
                                color: #333;
                                border-radius: 10px; 
                                padding: 15px;
                            }
                            QPushButton:hover {
                                background-color: #1A4870;  
                                color: #F9DBBA;                                        
                            }    
                            QLabel {
                                color: #333;

                            }         
                            #title {
                                font-family: 'Arial';
                                font-size:40px;
                                
                            }
                            QSlider:{
                                margin-right: 15px;
                            }
                            QlistWidget {
                                color: #333;
                          
                            }

                            """)
     

  


  # Event handlers 
    def event_handler(self):
        self.slider.valueChanged.connect(self.audio_methods.update_slider)
        self.btn_opener.clicked.connect(self.audio_methods.open_file)
        self.btn_play.clicked.connect(self.audio_methods.play_audio)
        self.btn_pause.clicked.connect(self.audio_methods.pause_audio)
        self.btn_resume.clicked.connect(self.audio_methods.resume_audio)
        self.btn_reset.clicked.connect(self.audio_methods.reset_audio)
        self.btn_stop.clicked.connect(self.audio_methods.stop_audio)




    # Métodos delegados a AudioMethods
    def update_time_label(self, position):
        self.audio_methods.update_time_label(position)

    def set_total_duration(self, duration):
        self.audio_methods.set_total_duration(duration)

    def update_song_label_with_duration(self):
        self.audio_methods.update_song_label_with_duration()


# Boilerplate para la aplicación PyQt6

if __name__ == "__main__":
    app = QApplication([])
    main = AudioApp()
    main.show()
    app.exec()
