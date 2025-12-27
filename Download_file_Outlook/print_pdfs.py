import os
import shutil
import win32print
import win32api

class PDFPrinter:
    def __init__(self, printer_name=None):
        self.printer_name = printer_name
    def imprimir_pdf(self, ruta_pdf, carpeta_impresos=None):
        try:
            print("Se abrirá el PDF. Imprime manualmente y confirma cuando hayas terminado.")
            os.startfile(ruta_pdf)
            input("Presiona ENTER cuando hayas terminado de imprimir el PDF...")
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
    ruta_base = "./invoices_pdfs_downloads"
    carpeta_impresos = "./Printed_pdf_downloads"
    lista_pdfs = PDFPrinter.obtener_todos_los_pdfs(ruta_base)
    printer = PDFPrinter("Brother MFC-L2710DW series")
    printer.imprimir_varios_pdfs(lista_pdfs, carpeta_impresos)