
import os
import shutil 

class FileMover:
    
    def mover_factura_procesada(pdf_file_path, carpeta_destino="processed_invoices"):
        """
        Mueve un archivo PDF procesado a la carpeta de facturas procesadas.
        Asume que la carpeta de destino ya existe.
        """
        try:
            nombre_archivo = os.path.basename(pdf_file_path)
            ruta_destino = os.path.join(carpeta_destino, nombre_archivo)
            shutil.move(pdf_file_path, ruta_destino)
            print(f"Archivo movido a: {ruta_destino}")
            return True
        except Exception as e:
            print(f"Error al mover el archivo {pdf_file_path}: {e}")
            return False