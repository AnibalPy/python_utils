import psutil
import datetime
import time
import os
import sys

# Define horario restringido (ejemplo: de 8:00 a 18:00)
start_hour = 8
end_hour = 18

while True:
    now = datetime.datetime.now()
        # Mostrar recursos usados por el proceso Python actual
    proc_self = psutil.Process(os.getpid())
    mem_used = proc_self.memory_info().rss / (1024 * 1024)
    mem_total = psutil.virtual_memory().total / (1024 * 1024)
    cpu = proc_self.cpu_percent(interval=1)
    mem_percent = (mem_used / mem_total) * 100 if mem_total > 0 else 0
    print(f"[Recursos] Memoria usada: {mem_used:.2f} MB de un total de {mem_total:.2f} MB ({mem_percent:.4f}%) | CPU usada: {cpu:.2f} %")
    
    if start_hour <= now.hour < end_hour:
        # Busca procesos Brave
        closed_count = 0
        close_time = None
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'brave' in proc.info['name'].lower():
                try:
                    proc.kill()
                    closed_count += 1
                    if not close_time:
                        close_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    print(f"Error cerrando Brave: {e}")
        if closed_count > 0 and close_time:
            print(f"Brave cerrado por restricción horaria a las {close_time}. ({closed_count} procesos)")
    time.sleep(10)  # Revisa cada 10 segundos