import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout

from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


# My application

class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
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
        self.slider.valueChanged.connect(self.update_slider) 
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play.clicked.connect(self.play_audio)
        self.btn_pause.clicked.connect(self.pause_audio)
        self.btn_resume.clicked.connect(self.resume_audio)
        self.btn_reset.clicked.connect(self.reset_audio)
        self.btn_stop.clicked.connect(self.stop_audio)




    #change slider speed label
    def update_slider(self):
        speed = self.slider.value() /100
        self.slider_text.setText(f"Speed: {speed:.2f}x")

    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        print(f"Carpeta seleccionada: {path}")
        self.selected_folder = path

        if path:
            self.file_list.clear()
            archivos = os.listdir(path)
            print(f"Archivos en la carpeta: {archivos}")
            for file_name in archivos:
                print(f"Revisando archivo: {file_name}")
                if file_name.endswith((".mp3" , ".wav", ".ogg", ".flac")):
                    print(f"Agregando: {file_name}")
                   # self.file_list.addItem(os.path.join(path, file_name))
                    self.file_list.addItem(file_name)
        else:
            print("No se seleccionó carpeta, abriendo diálogo de archivo...")
            file, _ = QFileDialog.getOpenFileName(self, "Select File", filter="Audio Files (*.mp3)")
            print(f"Archivo seleccionado: {file}")
            if file:
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))


    # Play the audio file
    def play_audio(self):
        if self.file_list.selectedItems():
            file_name = self.file_list.selectedItems()[0].text()
            
    
            file_path = os.path.join(self.selected_folder, file_name)
         #   file_path = os.path.join(folder_path, file_name)
          #  file_path = self.file_list.selectedItems()[0].text()



            file_url = QUrl.fromLocalFile(file_path)
          #  file_name = os.path.basename(file_path)
            self.song_label.setText(f"Reproduciendo: {file_name}")
            self.song_label.show()

            self.media_player.setSource(file_url)
            self.media_player.setPlaybackRate(self.slider.value() / 100.0)
            self.media_player.play()


            self.btn_pause.setEnabled(True)
            self.btn_pause.setStyleSheet("")  # Esto quita el color personalizado y vuelve al original
            self.btn_resume.setDisabled(True)
            self.btn_reset.setEnabled(True)
            self.btn_play.setDisabled(True)
            self.btn_play.setStyleSheet("background-color: lightgray; color: black;")
            self.slider.setDisabled(True)

    def pause_audio(self):
        self.media_player.pause()
        self.btn_pause.setDisabled(True)
        self.btn_pause.setStyleSheet("background-color: lightgray; color: black;")
        self.btn_resume.setEnabled(True)
        self.btn_play.setDisabled(True)
        self.btn_play.setStyleSheet("")  # Esto quita el color personalizado y vuelve al original
        


    def resume_audio(self):
        self.media_player.play()
        self.btn_pause.setEnabled(True)
        self.btn_pause.setDisabled(False)
        self.btn_pause.setStyleSheet("")
        self.btn_resume.setDisabled(True)
        

    def reset_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()    

        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value() / 100.0)
        self.media_player.play()

        self.btn_pause.setEnabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(True)
        
        self.btn_pause.setStyleSheet("")  # Esto quita el color personalizado y vuelve al original
        self.btn_play.setEnabled(True)
        self.btn_play.setStyleSheet("")
        self.time_label.hide()
        self.slider.setValue(100)  # O el valor inicial que prefieras
        self.slider.setDisabled(False)

        QTimer.singleShot(100, lambda: self.btn_reset.setEnabled(True)) 

    def stop_audio(self):
        if self.media_player.isPlaying():
            self.media_player.stop()    

        self.media_player.setPosition(0)
        self.media_player.setPlaybackRate(self.slider.value() / 100.0)

        self.btn_pause.setDisabled(True)
        self.btn_resume.setDisabled(True)
        self.btn_reset.setDisabled(False)
        
       # self.btn_pause.setStyleSheet("background-color: lightgray; color: black;")  # Esto quita el color personalizado y vuelve al original
        self.btn_play.setEnabled(True)
        self.btn_play.setStyleSheet("")   
        self.btn_pause.setStyleSheet("") 
        self.song_label.hide() 
        self.slider.setValue(100)  # O el valor inicial que prefieras
        self.slider.setDisabled(False)


    def update_time_label(self, position):
        seconds = int(position / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        self.time_label.setText(f"Tiempo: {minutes:02d}:{seconds:02d}")
        self.time_label.show()

    def set_total_duration(self, duration):
        self.total_duration = duration
        # Si ya hay una canción seleccionada, actualiza el label
        if self.song_label.isVisible():
            self.update_song_label_with_duration()

    def update_song_label_with_duration(self):
        if self.file_list.selectedItems():
            file_path = self.file_list.selectedItems()[0].text()
            file_name = os.path.basename(file_path)
            total_seconds = int(self.total_duration / 1000)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            self.song_label.setText(f"Reproduciendo: {file_name}  [{minutes:02d}:{seconds:02d}]")


# Boilerplate para la aplicación PyQt6

if __name__ == "__main__":
    app = QApplication([])
    main = AudioApp()
    main.show()
    app.exec()
