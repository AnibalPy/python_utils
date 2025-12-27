import win32com.client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import re
import pandas as pd
import os

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
dir_download = "./invoices_pdfs_downloads"
os.makedirs(dir_download, exist_ok=True)


#or account in outlook.Folders:
  # print(account.Name)

#i_cuenta = outlook.Folders["gestion@arrosia.com"]  # Reemplaza con tu dirección de correo
#nbox = mi_cuenta.Folders["Bandeja de entrada"]  # o "Inbox" según idioma



class OutlookEmailHandler:

    
    def get_inbox(account_name, fecha_inicio, fecha_fin):

        # Busca la cuenta por nombre
       # fecha_inicio = datetime(2025, 7, 1)
      #  fecha_fin = datetime(2025, 9, 30)
        dir_download = "./invoices_pdfs_downloads"
        correos_sin_adjuntos = []
        
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
        mensajes_a_descargar = []
        texto_avast = "Este correo electrónico ha sido analizado en busca de virus por el software antivirus de Avast."
        print("Buscando mensajes con la palabra 'factura'...")
        for message in messages:
            if not hasattr(message, "ReceivedTime"):
                continue  # Salta este elemento si no es un correo
            fecha_msg = message.ReceivedTime.replace(tzinfo=None)
            if (fecha_inicio <= fecha_msg <= fecha_fin) and (re.search(r'\bfactura\b', message.Subject, re.IGNORECASE) or
                re.search(r'\bfactura\b', message.Body, re.IGNORECASE)):
                try: 
                        if message.Attachments.Count > 0:            # Con adjunto                   
                            fecha = str(message.ReceivedTime)
                            body = message.Body
                            correos_dict[fecha] = body
                            mensajes_a_descargar.append(message)
                            print("Mensaje encontrado y leído con éxito (con adjunto).")
            
                        else:
                        # Sin adjunto
                            correos_sin_adjuntos.append({
                                'Fecha': str(message.ReceivedTime),
                                'Remitente': message.SenderName,
                                'Asunto': message.Subject
                        })
                except Exception as e:
                    print(f"Error al leer el correo: {e}")
        print("Resultado de la búsqueda.")    
        print("Total de mensajes encontrados:", len(correos_dict))  
        if correos_sin_adjuntos:
            df = pd.DataFrame(correos_sin_adjuntos)
            df.to_excel(f'{dir_download}/correos_sin_adjuntos.xlsx', index=False)
            print(f"Archivo Excel generado: {dir_download}/correos_sin_adjuntos.xlsx") 
        for fecha, mensaje in zip(correos_dict.keys(), mensajes_a_descargar):
            print(f"Fecha: {fecha} | Asunto: {mensaje.Subject}") 
        return correos_dict,  correos_sin_adjuntos, mensajes_a_descargar

    def get_outlook_accounts():
        #accounts = [store.DisplayName for store in outlook.Stores]
        accounts = []
        for account in outlook.Folders:
            print(account.Name)
            accounts.append(account.Name)
        return accounts

    



