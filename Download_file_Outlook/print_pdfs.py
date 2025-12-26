import os
import shutil
import win32print
import win32api

class PDFPrinter:
    def __init__(self, printer_name=None):
        self.printer_name = printer_name
    def imprimir_pdf(self, ruta_pdf, carpeta_impresos=None):
        try:
            # Usa la impresora especificada o la predeterminada
            printer = self.printer_name or win32print.GetDefaultPrinter()
            # Ruta al ejecutable de Adobe Reader (ajusta si es necesario)
            acrobat_path = r'C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe'
            # Comando para imprimir en la impresora deseada
            cmd = f'"{acrobat_path}" /t "{os.path.abspath(ruta_pdf)}" "{printer}"'
            print(f"Ejecutando: {cmd}")
            os.system(cmd)
            print(f"Enviando a imprimir: {ruta_pdf} en {printer}")
            if carpeta_impresos:
                os.makedirs(carpeta_impresos, exist_ok=True)
                destino = os.path.join(carpeta_impresos, os.path.basename(ruta_pdf))
                shutil.move(ruta_pdf, destino)
                print(f"Movido a: {destino}")
        except Exception as e:
            print(f"Error al imprimir {ruta_pdf}: {e}")

    def imprimir_varios_pdfs(self, lista_rutas, carpeta_impresos=None):
        for ruta in lista_rutas:
            self.imprimir_pdf(ruta, carpeta_impresos)

    @staticmethod
    def obtener_todos_los_pdfs(ruta_base):
        lista_pdfs = []
        for root, _, files in os.walk(ruta_base):
            for file in files:
                if file.lower().endswith('.pdf'):
                    lista_pdfs.append(os.path.join(root, file))
        return lista_pdfs

if __name__ == "__main__":
   # print("Impresora predeterminada:", win32print.GetDefaultPrinter())
    printer = PDFPrinter("Brother MFC-L2710DW series")
    ruta_base = "./invoices_pdfs_downloads"
    carpeta_impresos = "./Printed_pdf_downloads"
    lista_pdfs = PDFPrinter.obtener_todos_los_pdfs(ruta_base)
    # Cambia el nombre por el de tu impresora Brother
    printer = PDFPrinter("Nombre exacto de tu impresora Brother")
    printer.imprimir_varios_pdfs(lista_pdfs, carpeta_impresos)