
from search_emails import OutlookEmailHandler
from downloads_attachtment import PDFDownloader
from print_pdfs import PDFPrinter
import pandas as pd



if __name__ == "__main__":
    cuentas = OutlookEmailHandler.get_outlook_accounts()
    todos_sin_adjuntos = []
    for cuenta in cuentas:
        print(f"Procesando cuenta: {cuenta}")
        
        try:
            correos_dict, correos_sin_adjuntos, mensajes_a_descargar = OutlookEmailHandler.get_inbox(cuenta)
            downloader = PDFDownloader(f"./invoices_pdfs_downloads/{cuenta}")
            downloader.descargar_adjuntos(mensajes_a_descargar)
            for correo in correos_sin_adjuntos:
                correo['Cuenta'] = cuenta
            todos_sin_adjuntos.extend(correos_sin_adjuntos)
        except Exception as e:
            print(f"Error procesando la cuenta {cuenta}: {e}")
    if todos_sin_adjuntos:
        df = pd.DataFrame(todos_sin_adjuntos)
        df.to_excel('./invoices_pdfs_downloads/correos_sin_adjuntos_todas_cuentas.xlsx', index=False)
        print("Archivo Excel generado: ./invoices_pdfs_downloads/correos_sin_adjuntos_todas_cuentas.xlsx")    

  #  ruta_base = "./invoices_pdfs_downloads"
  #  lista_pdfs = PDFPrinter.obtener_todos_los_pdfs(ruta_base)
  #  printer = PDFPrinter()
  #  printer.imprimir_varios_pdfs(lista_pdfs)    