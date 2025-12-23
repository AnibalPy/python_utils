import os
import tempfile
import wave
import pyaudio  
import keyboard
import pyautogui
import pyperclip
from groq import Groq 
import win32com.client 
import threading


from dotenv import load_dotenv

load_dotenv()




apikey_groq = os.getenv('GROQ_API_KEY')


#print("API KEY:", apikey_groq)  # <-- Añade este print

# ...existing code...


#client = Groq(api_key=apikey_groq)

class Audio_Actions:
    def __init__(self):
        self.grabando = False
        self.frames = []
        self.frecuencia_muestreo = 16000
        self.client = Groq(api_key=apikey_groq)
      #  print("API KEY:", apikey_groq)

    def print_message(self):
      #  print("Audio Actions Initialized")
      #  print("API KEY:", apikey_groq)
        pass

    def iniciar_grabacion(self, frecuencia_muestreo=16000, canales=1, fragmento=1024):
        self.grabando = True
        self.frames = []
        self.frecuencia_muestreo = frecuencia_muestreo
        hilo = threading.Thread(target=self.grabar_audio, args=(frecuencia_muestreo, canales, fragmento))
        hilo.start()  

    def grabar_audio(self, frecuencia_muestreo=16000, canales=1, fragmento=1024):
        self.frames = []
       # self.grabando = True 

        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16, 
            channels=canales,
            rate=frecuencia_muestreo, 
            input=True,
            frames_per_buffer=fragmento)
        print('Grabando..')

        while self.grabando:
            data = stream.read(fragmento)
            self.frames.append(data)
        print('Grabación finalizada.')
        stream.stop_stream()
        stream.close()
        audio.terminate()   
        self.frecuencia_muestreo = frecuencia_muestreo
       # print("Fragmentos grabados:", len(self.frames))
        
    
    def guardar_audio(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_temp:
            wf = wave.open(audio_temp.name, mode="wb")
            wf.setnchannels(1)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.frecuencia_muestreo)
            wf.writeframes(b"".join(self.frames))
            wf.close()
            return audio_temp.name
        
    def transcribir_audio(self, ruta_archivo_audio):
        try:
            with open(ruta_archivo_audio, "rb") as archivo:
                print("API KEY:", apikey_groq)
                transcription = self.client.audio.transcriptions.create(
                    file=(os.path.basename(ruta_archivo_audio), archivo.read()),
                    model="whisper-large-v3",
                    prompt="el audio de una persona hablando en español de manera clara y pausada",
                    response_format="text",
                    language="es"
                )
            return transcription
        except Exception as e:
            print(f"Error al transcribir el audio: {e}")
            return None
    def copiar_al_portapapeles(self, texto):
        import pythoncom
        pythoncom.CoInitialize()
        try:
            if texto is None:
                print("No hay texto para copiar al portapapeles.")
                return
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = True
            if len(word.Documents) == 0:
                doc = word.Documents.Add()
            else:
                doc = word.ActiveDocument
            doc.Content.InsertAfter(texto + "\n")
            print("Transcripción agregada a Word.")
        except Exception as e:
            print(f"Error al escribir en Word: {e}")
    # En tu clase Audio_Actions

    def detener_grabacion(self):
        self.grabando = False  # Esto detiene el bucle en grabar_audio

    def flujo_stop(self):
        ruta_audio = self.guardar_audio()
        texto = self.transcribir_audio(ruta_audio)
        self.copiar_al_portapapeles(texto)
        return texto  # <-- Añade este return



