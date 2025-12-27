import win32print

win32print.SetDefaultPrinter("Brother MFC-L2710DW series")

import os
import win32print
from print_pdfs import PDFPrinter

def impresora_activa(nombre_impresora):
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)
    for printer in printers:
        if nombre_impresora.lower() in printer[2].lower():
            handle = win32print.OpenPrinter(printer[2])
            info = win32print.GetPrinter(handle, 2)
            status = info['Status']
            win32print.ClosePrinter(handle)
            # Status 0 normalmente significa "Ready"
            return status == 0
    return False

if __name__ == "__main__":
    import os
    nombre_impresora = "Brother MFC-L2710DW series"
    if impresora_activa(nombre_impresora):
        print(f"La impresora {nombre_impresora} está activa y lista.")

        # (Eliminado: creación y apertura de archivo TXT para impresión manual)

        # Crear PDF de prueba si no existe
        pdf_file = "pagina_prueba.pdf"
        if not os.path.exists(pdf_file):
            try:
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="Página de prueba enviada desde Python a la impresora Brother.", ln=True)
                pdf.ln(10)
                pdf.cell(200, 10, txt="Si ves este texto, la impresora funciona correctamente.", ln=True)
                pdf.output(pdf_file)
                print(f"PDF de prueba creado: {pdf_file}")
            except Exception as e:
                print(f"Error creando PDF de prueba: {e}")

        # Abrir PDF con el visor predeterminado de Windows para impresión manual
        print("Se abrirá el PDF. Selecciona Archivo > Imprimir y elige las opciones de impresión manualmente.")
        try:
            os.startfile(pdf_file)
            print(f"PDF abierto: {pdf_file}")
        except Exception as e:
            print(f"Error al abrir PDF: {e}")
        # pdf.set_font("Arial", size=12)
        # pdf.cell(200, 10, txt="Página de prueba enviada desde Python a la impresora Brother.", ln=True)
        # pdf.output(pdf_file)
        # import subprocess
        # acrobat_path = r'C:\\Program Files\\Adobe\\Acrobat DC\\Acrobat\\Acrobat.exe'
        # cmd = f'"{acrobat_path}" /p "{os.path.abspath(pdf_file)}"'
        # print(f"Ejecutando: {cmd}")
        # subprocess.Popen(cmd)
    else:
        print(f"La impresora {nombre_impresora} no está disponible o no está lista.")
