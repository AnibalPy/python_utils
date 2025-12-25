
import PyPDF2
import os
import re

 
from pdf_utils import PDFInvoiceExtractor
from db_utils import DBManager
from file_utils import FileMover
from db_utils import DBManager


DBManager.test_mysql_connection()


if __name__ == "__main__":
    folder_path = "invoices"
    pdf_files = PDFInvoiceExtractor.get_files_in_folder(folder_path)
    #pdf_files = FileMover.get_files_in_folder(folder_path)  # Si también modularizas esta función
    if not pdf_files:
        print("No hay facturas para procesar.")
    else:
        for file in pdf_files:
            print(f"Procesando archivo: {file}")
            factura_data = PDFInvoiceExtractor.extract_invoice_info(file)
            DBManager.guardar_factura_en_mysql(factura_data)
            FileMover.mover_factura_procesada(file)
 

           
       








  