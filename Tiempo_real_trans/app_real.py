import os
import tempfile
import wave
import pyaudio  
import keyboard
import pyautogui
import pyperclip
from groq import Groq 

client = Groq(api_key="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")

def grabar_audio(frecuencia_muestreo=16000, canales=1, fragmento=1024):
    #formato = pyaudio.paInt16
    #chunk = 1024
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=pyaudio.paInt16, 
        channels=canales,
                        
        rate=frecuencia_muestreo, 
        input=True,
        frames_per_buffer=fragmento)

    print("Presiona 'insert' para iniciar la grabación.")
    
   

    frames = []
    keyboard.wait('insert')
    print("Grabando... Suelta 'insert' para detener la grabación.")


    while keyboard.is_pressed('insert'):
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
        pyperclip.copy(texto)
        pyautogui.hotkey("ctrl", "v")
        print("Transcripción copiada al portapapeles.") 

def main():
    while True:
        frames, frecuencia_muestreo = grabar_audio()
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
        print("\nListo para la próxima grabación.Presiona 'insert' para grabar de nuevo o 'esc' para salir.")   

if __name__ == "__main__":   
    main()




