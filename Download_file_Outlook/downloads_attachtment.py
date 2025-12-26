import os
import re
from search_emails import OutlookEmailHandler

dir_download = "./invoices_pdfs_downloads"
os.makedirs(dir_download, exist_ok=True)

class PDFDownloader:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)
 

    @staticmethod
    def limpiar_nombre_archivo(nombre):
        import re
        # Reemplaza caracteres no válidos y barras
        nombre = re.sub(r'[<>:"/\\|?*]', '_', nombre)
        # Elimina espacios al inicio/fin
        nombre = nombre.strip()
        # Si queda vacío, pon un nombre por defecto
        if not nombre:
            nombre = 'adjunto'
        # Limita la longitud
        if len(nombre) > 100:
            nombre = nombre[:100]
        return nombre

    def descargar_adjuntos(self, mensajes):
        for message in mensajes:
            try:
                for attachment in message.Attachments:
                    nombre_archivo = self.limpiar_nombre_archivo(attachment.FileName)
                    if nombre_archivo.lower().endswith('.pdf'):
                        ruta_guardado = os.path.abspath(os.path.join(self.download_dir, nombre_archivo))
                        print(f"Nombre archivo: {nombre_archivo} | Longitud: {len(nombre_archivo)}")
                        print(f"Intentando guardar en: {ruta_guardado}")
                        attachment.SaveAsFile(ruta_guardado)
                        print(f"Adjunto guardado: {ruta_guardado}")
            except Exception as e:
                print(f"Error al descargar adjuntos: {e}")
