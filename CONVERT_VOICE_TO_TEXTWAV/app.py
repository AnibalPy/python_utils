# CONVERT_VOICE_TO_TEXT/app.py wave a texto

import speech_recognition as SR
import time
r = SR.Recognizer()


# RUTA

with SR.AudioFile('./Audios/Grabación.wav') as source:
    audio = r.listen(source)

    try:
        print("Espere un momento, el audio se está leyendo...")
        text = r.recognize_google(audio, language='es-ES')
        time.sleep(1.5)
        print("Texto:)", text)

    except:
        
         print("Lo siento, no he podido leer el audio")
         print("Lo siento, no he podido leer el audio")
 