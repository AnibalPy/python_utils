

import os
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import QTimer


class AudioMethods:
    def __init__(self, app):
        self.app = app

    def update_slider(self):
        speed = self.app.slider.value() / 100
        self.app.slider_text.setText(f"Speed: {speed:.2f}x")

    def open_file(self):

        path = QFileDialog.getExistingDirectory(self.app, "Select Folder")
        self.app.selected_folder = path
        if path:
            self.app.file_list.clear()
            archivos = os.listdir(path)
            for file_name in archivos:
                if file_name.endswith((".mp3", ".wav", ".ogg", ".flac")):
                    self.app.file_list.addItem(file_name)
        else:
            file, _ = QFileDialog.getOpenFileName(self.app, "Select File", filter="Audio Files (*.mp3)")
            if file:
                self.app.file_list.clear()
                self.app.file_list.addItem(os.path.basename(file))

    def play_audio(self):
        
        if self.app.file_list.selectedItems():
            file_name = self.app.file_list.selectedItems()[0].text()
            file_path = os.path.join(self.app.selected_folder, file_name)
            file_url = QUrl.fromLocalFile(file_path)
            self.app.song_label.setText(f"Reproduciendo: {file_name}")
            self.app.song_label.show()
            self.app.media_player.setSource(file_url)
            self.app.media_player.setPlaybackRate(self.app.slider.value() / 100.0)
            self.app.media_player.play()
            self.app.btn_pause.setEnabled(True)
            self.app.btn_pause.setStyleSheet("")
            self.app.btn_resume.setDisabled(True)
            self.app.btn_reset.setEnabled(True)
            self.app.btn_play.setDisabled(True)
            self.app.btn_play.setStyleSheet("background-color: lightgray; color: black;")
            self.app.slider.setDisabled(True)

    def pause_audio(self):
        self.app.media_player.pause()
        self.app.btn_pause.setDisabled(True)
        self.app.btn_pause.setStyleSheet("background-color: lightgray; color: black;")
        self.app.btn_resume.setEnabled(True)
        self.app.btn_play.setDisabled(True)
        self.app.btn_play.setStyleSheet("")

    def resume_audio(self):
        self.app.media_player.play()
        self.app.btn_pause.setEnabled(True)
        self.app.btn_pause.setDisabled(False)
        self.app.btn_pause.setStyleSheet("")
        self.app.btn_resume.setDisabled(True)

    def reset_audio(self):
        
        if self.app.media_player.isPlaying():
            self.app.media_player.stop()
        self.app.media_player.setPosition(0)
        self.app.media_player.setPlaybackRate(self.app.slider.value() / 100.0)
        self.app.media_player.play()
        self.app.btn_pause.setEnabled(True)
        self.app.btn_resume.setDisabled(True)
        self.app.btn_reset.setDisabled(True)
        self.app.btn_pause.setStyleSheet("")
        self.app.btn_play.setEnabled(True)
        self.app.btn_play.setStyleSheet("")
        self.app.time_label.hide()
        self.app.slider.setValue(100)
        self.app.slider.setDisabled(False)
        QTimer.singleShot(100, lambda: self.app.btn_reset.setEnabled(True))

    def stop_audio(self):
        if self.app.media_player.isPlaying():
            self.app.media_player.stop()
        self.app.media_player.setPosition(0)
        self.app.media_player.setPlaybackRate(self.app.slider.value() / 100.0)
        self.app.btn_pause.setDisabled(True)
        self.app.btn_resume.setDisabled(True)
        self.app.btn_reset.setDisabled(False)
        self.app.btn_play.setEnabled(True)
        self.app.btn_play.setStyleSheet("")
        self.app.btn_pause.setStyleSheet("")
        self.app.song_label.hide()
        self.app.slider.setValue(100)
        self.app.slider.setDisabled(False)

    def update_time_label(self, position):
        seconds = int(position / 1000)
        minutes = seconds // 60
        seconds = seconds % 60
        self.app.time_label.setText(f"Tiempo: {minutes:02d}:{seconds:02d}")
        self.app.time_label.show()

    def set_total_duration(self, duration):
        self.app.total_duration = duration
        if self.app.song_label.isVisible():
            self.update_song_label_with_duration()

    def update_song_label_with_duration(self):
     
        if self.app.file_list.selectedItems():
            file_path = self.app.file_list.selectedItems()[0].text()
            file_name = os.path.basename(file_path)
            total_seconds = int(self.app.total_duration / 1000)
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            self.app.song_label.setText(f"Reproduciendo: {file_name}  [{minutes:02d}:{seconds:02d}]")
