import re
import mysql.connector
import shutil  
from dotenv import load_dotenv

load_dotenv()
import os



class DBManager:


    #crear una conexion a la base de datos MySQL y guardar la factura
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }




    @staticmethod
    def test_mysql_connection():
        try:
            import mysql.connector
            conn = mysql.connector.connect(**DBManager.db_config)
            if conn.is_connected():
                print("¡Conexión exitosa a MySQL!")
                conn.close()
                return True
        except mysql.connector.Error as err:
            print("Error al conectar a MySQL:", err)
            return False

    # Uso:
 #   test_mysql_connection()
    


    @staticmethod
    def guardar_factura_en_mysql(factura_data):
        conn = None
        cursor = None
        try:
            conn = mysql.connector.connect(**DBManager.db_config)
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