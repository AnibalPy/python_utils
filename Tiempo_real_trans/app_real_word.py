import os
import tempfile
import wave
import pyaudio  
import keyboard
import pyautogui
import pyperclip
from groq import Groq 
import win32com.client 
<<<<<<< HEAD
import time
=======
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb


from dotenv import load_dotenv

load_dotenv()


#host = os.getenv("DB_HOST")
#api_keygroq = os.getenv('apikey_groq')
import os
apikey_groq = os.getenv('GROQ_API_KEY')

# ...existing code...


client = Groq(api_key=apikey_groq)

def grabar_audio(frecuencia_muestreo=16000, canales=1, fragmento=1024):
    frames = []
    print("Presiona 'insert' para iniciar la grabación o 'esc' para salir.")
    while True:
        if keyboard.is_pressed('esc'):
            print("Grabación cancelada por el usuario (ESC). Programa terminado.")
            exit(0)
        if keyboard.is_pressed('insert'):
            break
    print("Grabando... Suelta 'insert' para detener la grabación o pulsa 'esc' para salir.")

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16, 
        channels=canales,
        rate=frecuencia_muestreo, 
        input=True,
        frames_per_buffer=fragmento)

<<<<<<< HEAD
<<<<<<< HEAD
    print("Presiona 'insert' para iniciar la grabación.")
    
   

    frames = []
    #keyboard.wait('insert')
    while not keyboard.is_pressed('insert'):
        if keyboard.is_pressed('esc'):
            return [], frecuencia_muestreo  # Retorna vacío si se presiona ESC
    time.sleep(0.1)
    print("Grabando... Suelta 'insert' para detener la grabación.")


=======
>>>>>>> master
=======
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb
    while keyboard.is_pressed('insert'):
        if keyboard.is_pressed('esc'):
            print("Grabación cancelada por el usuario (ESC). Programa terminado.")
            stream.stop_stream()
            stream.close()
            audio.terminate()
            exit(0)
        data = stream.read(fragmento)
        frames.append(data)
    print('Grabación finalizada.')
    stream.stop_stream()
    stream.close()
    audio.terminate()   
    return frames, frecuencia_muestreo
def guardar_audio(frames, frecuencia_muestreo):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as audio_temp:
        wf = wave.open(audio_temp.name, mode="wb")
        wf.setnchannels(1)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        wf.setframerate(frecuencia_muestreo)
        wf.writeframes(b"".join(frames))
        wf.close()
        return audio_temp.name
    
def transcribir_audio(ruta_archivo_audio):
    try:
        with open(ruta_archivo_audio, "rb") as archivo:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(ruta_archivo_audio), archivo.read()),
                model="whisper-large-v3",
                prompt="""el audio de una persona hablando en español de manera clara y pausada""",
                response_format="text",
                language="es"
            )
        return transcription
    except Exception as e:
        print(f"Error al transcribir el audio: {e}")
        return None
def copiar_al_portapapeles(texto):
    try:
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

def main():
<<<<<<< HEAD
    
    while True:
        #verificar si has presionado esc o insert
  
        if keyboard.is_pressed('esc'):
                print("Saliendo del programa...")
                return

        time.sleep(0.1)  # Pequeña pausa para no saturar la CPU

        frames, frecuencia_muestreo = grabar_audio()


        if not frames:  # Si está vacío, salir
            print("Operación cancelada.")
            return


=======
    while True:
        frames, frecuencia_muestreo = grabar_audio()
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb
        archivo_audio_temp = guardar_audio(frames, frecuencia_muestreo)
        print("Transcribiendo...")
        transcripcion = transcribir_audio(archivo_audio_temp)
        
        if transcripcion:
            print("\nTranscripción:")
            print("Copiando transcripción al portapapeles... ")
           
            copiar_al_portapapeles(transcripcion)
            print("Transcripción copiada al portapapeles y pegada en la aplicación activa.")
        else:
            print("No se pudo obtener la transcripción.")

        os.unlink(archivo_audio_temp)
<<<<<<< HEAD
        print("\nListo para la próxima grabación.Presiona 'insert' para grabar de nuevo o 'esc' para salir.")  

if __name__ == "__main__":   
    try:
        main()
    except Exception as e:
        print(f"\nError: {e}")
        input("Presiona Enter para salir...")
=======
        print("\nListo para la próxima grabación.Presiona 'insert' para grabar de nuevo o 'esc' para salir.")   

if __name__ == "__main__":   
    main()
>>>>>>> 9fe2ee77a053c99aefda04af90accce2fd7d77fb
