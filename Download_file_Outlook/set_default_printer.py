import win32print

nombre_impresora = "Brother MFC-L2710DW series"

try:
    win32print.SetDefaultPrinter(nombre_impresora)
    print(f"Impresora predeterminada cambiada a: {nombre_impresora}")
except Exception as e:
    print(f"Error al cambiar la impresora predeterminada: {e}")
