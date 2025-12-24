
import PyPDF2
import os
import re
import mysql.connector  



def extract_invoice_info(pdf_file_path):

    #Open the PDF file
    with open(pdf_file_path, 'rb') as file:

        #create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        #extract text from each page
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() 

       # print(text)    
        # Regular expressions to find invoice number, date, and total amount


# ... después de extraer el texto del PDF en la variable 'text'

        # Patrones regex corregidos
        empresa_pattern = r'General Autonómico\s*\n*([A-ZÁÉÍÓÚÑa-záéíóúñ\s\.\-]+)\s+Campo de Tajonar'
        direccion_pattern = r'AN ENERGETICOS S\.L\.\s*(.*?),\s*\d{5}\s*[A-ZÁÉÍÓÚÑa-záéíóúñ\s\(\)]+,'
        cp_pattern = r'AN ENERGETICOS S\.L\..*?,\s*(\d{5})\s'

        nif_pattern = r'N\.I\.F\s*:?\s*([A-Z0-9]+)'  # Si no lo encuentra, revisa si aparece como "N.I.F" o "NIF"
        telefono_pattern = r'Telefono\s*(\d+)'
        factura_pattern = r'<NumFact>(.*?)</NumFact>'
        fecha_pattern = r'<Fecha>(.*?)</Fecha>'
        codigo_cliente_pattern = r'Código Cliente\s*:?\s*([A-Z0-9]+)'
        cif_cliente_pattern = r'CIF Cliente\s*:?\s*([A-Z0-9]+)'

        codigo_linea_pattern = r':\s*([A-Z0-9]+)\s+([0-9]+)\s+([A-Z0-9]+)'
        codigo_linea_match = re.search(codigo_linea_pattern, text)

        litros_pattern = r'([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)'
        base_iva_pattern = r'([0-9]+(?:\.[0-9]+)?)\s+Importe\s+([0-9]{1,2})\s+([0-9]+(?:\.[0-9]+)?)'

        importe_iva_pattern = r'Importe IVA\s*([0-9]+(?:\.[0-9]+)?)'
        forma_pago_pattern = r'Forma de pago\s*(.+)'
        vencimiento_pattern = r'TOTAL\s*\n*([0-9]{2}/[0-9]{2}/[0-9]{4})'
        vehiculo_pattern = r'(\d{14})\s+(\d{4}\s+[A-Z]{3}\s*-\s*\d{4}\s+[A-Z]{3})'
        # Nuevo patrón para items según tu ejemplo
        items_pattern = r'(\d{2}/\d{2}/\d{2})\s+\S+\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([A-ZÁÉÍÓÚÑa-záéíóúñ\s\-]+)\s+Gasóleo'

        # Extracción de datos
        empresa_match = re.search(empresa_pattern, text)
        direccion_match = re.search(direccion_pattern, text)
        cp_match = re.search(cp_pattern, text)
        nif_match = re.search(nif_pattern, text)
        telefono_match = re.search(telefono_pattern, text)
        factura_match = re.search(factura_pattern, text)
        fecha_match = re.search(fecha_pattern, text)
       # codigo_cliente_match = re.search(codigo_cliente_pattern, text)
       # cif_cliente_match = re.search(cif_cliente_pattern, text)

        
        # Busca la línea con "0.000" seguido de un número
       
       
        base_iva_match = re.search(base_iva_pattern, text)
        importe_iva_match = re.search(importe_iva_pattern, text)
        forma_pago_match = re.search(forma_pago_pattern, text)
        vencimiento_match = re.search(vencimiento_pattern, text)
        vehiculo_match = re.search(vehiculo_pattern, text)
        items_matches = re.findall(items_pattern, text)

        # Guardar los valores
        empresa = empresa_match.group(1).strip() if empresa_match else None
        direccion_empresa = direccion_match.group(1).strip() if direccion_match else None
        cp_empresa = cp_match.group(1) if cp_match else None
        nif = nif_match.group(1).strip() if nif_match else None
        telefono = telefono_match.group(1) if telefono_match else None
        factura = factura_match.group(1).strip() if factura_match else None
        fecha = fecha_match.group(1).strip() if fecha_match else None
        if fecha:
            fecha = fecha.replace(' ', '')
      #  codigo_cliente = codigo_cliente_match.group(1).strip() if codigo_cliente_match else None
      #  cif_cliente = cif_cliente_match.group(1).strip() if cif_cliente_match else None

        codigo_cliente = codigo_linea_match.group(2) if codigo_linea_match else None
        nif = codigo_linea_match.group(3) if codigo_linea_match else None

        

 


        base_iva = base_iva_match.group(1) if base_iva_match else None
        porcentaje_iva = base_iva_match.group(2) if base_iva_match else None
        importe_iva = base_iva_match.group(3) if base_iva_match else None
        importe_iva_simple = importe_iva_match.group(1) if importe_iva_match else None
        forma_pago = forma_pago_match.group(1).strip() if forma_pago_match else None
        vencimiento = vencimiento_match.group(1) if vencimiento_match else None
        codigo_vehiculo = vehiculo_match.group(1) if vehiculo_match else None
        matricula = vehiculo_match.group(2).replace(' ', '').replace('-', ' - ') if vehiculo_match else None
        items = []
        for match in items_matches:
            item = {
                "fecha_albaran": match[0],
                "cantidad": match[1],
                "precio": match[2],
                "importe": match[3],
                "estacion": match[4].strip()
            }
            items.append(item)


        # Imprimir resultados'''
        '''
        print("Empresa:", empresa)
        print("Dirección empresa:", direccion_empresa)
        print("Código Postal empresa:", cp_empresa)
        print("N.I.F:", nif)
        print("Teléfono empresa:", telefono)
        print("Nº Factura:", factura)
        print("Fecha factura:", fecha)
        print("Código Cliente:", codigo_cliente)
      #  print("CIF Cliente:", cif_cliente)

        print("Items:")
        print("Código de vehículo:", codigo_vehiculo)
        print("Matrícula:", matricula)
        for item in items_matches:
            fecha_albaran = item[0]
            cantidad = item[1]
            precio = item[2]
            importe = item[3]
            estacion = item[4].strip()
            print(f"Fecha Albarán: {fecha_albaran}, Estación: {estacion}, Cantidad: {cantidad}, Precio: {precio}, Importe: {importe}")  
       
        print("Base IVA:", base_iva)
        print("% IVA:", porcentaje_iva)
        print("Importe IVA:", importe_iva)
        print("Importe IVA (simple):", importe_iva_simple)
        print("Forma de pago:", forma_pago)
        print("Vencimientos:", vencimiento)'''

        # Retorna un diccionario con los datos extraídos
        return {    
            "empresa": empresa,
            "direccion_empresa": direccion_empresa,
            "cp_empresa": cp_empresa,
            "nif": nif,
            "telefono": telefono,
            "factura": factura,
            "fecha": fecha,
            "codigo_cliente": codigo_cliente,
           # "cif_cliente": cif_cliente,
            "items": items,
            "base_iva": base_iva,
            "porcentaje_iva": porcentaje_iva,
            "importe_iva": importe_iva,
            "importe_iva_simple": importe_iva_simple,
            "forma_pago": forma_pago,
            "vencimiento": vencimiento,
            "codigo_vehiculo": codigo_vehiculo,
            "matricula": matricula
        }
#obtener todas las facturas de una carpeta
def get_files_in_folder(folder_path):
    files = []
    #
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            
            files.append(os.path.join(root, filename))
    return files
#extract_invoice_info("invoices/invoice.pdf") 

#crear una conexion a la base de datos MySQL y guardar la factura
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '',
    'database': 'invoice_pdf'
}

def test_mysql_connection():
    try:
        import mysql.connector
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("¡Conexión exitosa a MySQL!")
            conn.close()
            return True
    except mysql.connector.Error as err:
        print("Error al conectar a MySQL:", err)
        return False

# Uso:
test_mysql_connection()


def guardar_factura_en_mysql(factura_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insertar factura
        sql_factura = """
        INSERT INTO factura (
            empresa, direccion_empresa, cp_empresa, nif, telefono, factura, fecha,
            codigo_cliente, base_iva, porcentaje_iva, importe_iva, importe_iva_simple,
            forma_pago, vencimiento, codigo_vehiculo, matricula
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        factura_values = (
            factura_data['empresa'],
            factura_data['direccion_empresa'],
            factura_data['cp_empresa'],
            factura_data['nif'],
            factura_data['telefono'],
            factura_data['factura'],
            factura_data['fecha'],
            factura_data['codigo_cliente'],
            factura_data['base_iva'],
            factura_data['porcentaje_iva'],
            factura_data['importe_iva'],
            factura_data['importe_iva_simple'],
            factura_data['forma_pago'],
            factura_data['vencimiento'],
            factura_data['codigo_vehiculo'],
            factura_data['matricula']
        
        
        )
        cursor.execute(sql_factura, factura_values)
        conn.commit()
        factura_id = cursor.lastrowid

        # Insertar ítems
        sql_item = """
        INSERT INTO item (factura_id, fecha_albaran, estacion, cantidad, precio, importe)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        for item in factura_data['items']:
            item_values = (
                factura_id,
                item['fecha_albaran'],
                item['estacion'],
                item['cantidad'],
                item['precio'],
                item['importe']
            )
        ###
        '''
        print("Datos de factura a guardar:")
        for campo, valor in zip([
            "empresa", "direccion_empresa", "cp_empresa", "nif", "telefono", "factura", "fecha",
            "codigo_cliente", "items", "base_iva", "porcentaje_iva", "importe_iva", "importe_iva_simple",
            "forma_pago", "vencimiento", "codigo_vehiculo", "matricula" 
        ], factura_values):
            print(f"{campo}: {valor}")

        print("\nÍtems a guardar:")
        for item in factura_data['items']:
            print(item)'''
        # 
        # 
        #     
        cursor.execute(sql_item, item_values)
        conn.commit()

        print(f"Factura {factura_data['factura']}  e ítems guardados correctamente.")
    except mysql.connector.Error as err:
        print("Error al guardar en MySQL:", err)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



####
if __name__ == "__main__":
    # Ruta de la carpeta que contiene las facturas PDF
    folder_path = "invoices"
    pdf_files = get_files_in_folder(folder_path)
    for file in pdf_files:
       # print(f"Procesando archivo: {file}")
       # empresa, direccion_empresa, cp_empresa, nif, telefono, factura, fecha, codigo_cliente, items, base_iva, porcentaje_iva, importe_iva, importe_iva_simple, forma_pago, vencimiento, codigo_vehiculo, matricula = extract_invoice_info(file).values()
        #print extracted data
    
        factura_data = extract_invoice_info(file)
      #  print("Claves en factura_data:", factura_data.keys())
        guardar_factura_en_mysql(factura_data)
    '''
        print("Empresa:", empresa)
        print("Dirección empresa:", direccion_empresa)  
        print("Código Postal empresa:", cp_empresa)
        print("N.I.F:", nif)    
        print("Teléfono empresa:", telefono)
        print("Nº Factura:", factura)   
        print("Fecha factura:", fecha)
        print("Código Cliente:", codigo_cliente)
        print("Items:", items)
        print("Base IVA:", base_iva)
        print("% IVA:", porcentaje_iva)
        print("Importe IVA:", importe_iva)
        print("Importe IVA (simple):", importe_iva_simple)
        print("Forma de pago:", forma_pago)
        print("Vencimientos:", vencimiento)
        print("Código de vehículo:", codigo_vehiculo)
        print("Matrícula:", matricula)  '''

           
       

    # Descomentar para probar con un solo archivo
    #


empresa, direccion_empresa, cp_empresa, nif, telefono, factura, fecha, codigo_cliente, items, base_iva, porcentaje_iva, importe_iva, importe_iva_simple, forma_pago, vencimiento, codigo_vehiculo, matricula = extract_invoice_info(file).values()


#creamos la conexion a la base de datos MySQL






  