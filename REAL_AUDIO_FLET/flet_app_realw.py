import os
import shutil
import flet as ft
import threading
import time
import asyncio
from methods import Audio_Actions   



def main(page: ft.Page):
    audio = Audio_Actions()
    audio.print_message()



def main(page: ft.Page):
    page.title = "Transcribe audio al momento de Aníbal Ruiz"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER


    page.window.width = 480
    page.window.height = 700
    page.window.min_width = 480  # Ancho mínimo permitido
    page.window.min_height = 700  # Alto mínimo permitido

   

    page.window.resizable = False

    page.window.center()
    page.title = "Transcribe audio al momento de Aníbal Ruiz"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.padding = 20  # Espaciado interno
    page.bgcolor = "#1976D2"


    # Obtener lista de carpetas de usuarios
    users_path = "C:/Users"
    try:
        user_folders = [f.name for f in os.scandir(users_path) if f.is_dir()]
    except Exception as e:
        user_folders = []
        print(f"Error al leer la carpeta Users: {e}")

    # ComboBox para seleccionar wifi detectadas
 

    # Texto de estado/resultado
    status_text = ft.Text("", color=ft.Colors.RED)

#
#   # Event handlers 
    timer_text = ft.Text("Tiempo: 00:00", size=16, color=ft.Colors.RED, weight=ft.FontWeight.BOLD, visible=False)
    #live_text = ft.Text("Texto en vivo: ", size=16, color=ft.Colors.BLUE, weight=ft.FontWeight.NORMAL)
    timer_running = False
    timer_seconds = 0
    current_text = ""
    #spinner de progreso
    spinner = ft.ProgressRing(visible=False)
    

    def on_start_click(e):
        global timer_running, timer_seconds, current_text
        timer_running = True
        timer_seconds = 0
        current_text = ""
        timer_text.visible = True
        page.run_task(update_timer)
        start_button.bgcolor = ft.Colors.ORANGE_300
        start_button.color = ft.Colors.WHITE
        spinner.visible = True


        audio.iniciar_grabacion()  # <-- Aquí inicias la grabación
        page.update()

    def on_stop_click(e):
        global timer_running, timer_seconds, current_text
        timer_running = False
        timer_seconds = 0
        current_text = ""
        timer_text.value = "Tiempo: 00:00"
        timer_text.visible = False
      #  live_text.value = "Texto en vivo: "
        start_button.bgcolor = None
        start_button.color = ft.Colors.GREEN_800
        
        spinner.visible = False
        page.update()



    async def update_timer():
        global timer_seconds, current_text, timer_running
        while timer_running:
            mins, secs = divmod(timer_seconds, 60)
            timer_text.value = f" {mins:02d}:{secs:02d}"
            current_text += f" {secs}"
          #  live_text.value = f"Texto en vivo: {current_text.strip()}"
            page.update()
            await asyncio.sleep(1)
            if timer_running:
                timer_seconds += 1
    def on_clear_click(e):
        transcribed_text.value = ""
        page.update()

    
# Botón para iniciar grabación


    start_button = ft.ElevatedButton(
        "Start",
        icon=ft.Icons.PLAY_ARROW,
       # bgcolor=ft.Colors.ORANGE_300,
        color = ft.Colors.GREEN_800,
        on_click=on_start_click,
    
      #  on_click=delete_temp_files,
        tooltip="Start",
        width=100,
        height=50,
    )

    stop_button = ft.ElevatedButton(
        "Stop",
        icon=ft.Icons.STOP,
        tooltip="Stop",
        on_click=on_stop_click,
        width=100,
        height=50,
        
    )
    # boton para limpiar texto
    clear_button = ft.ElevatedButton(
    "Clear",
    icon=ft.Icons.CLEAR,
    tooltip="Clear",
    on_click=on_clear_click,
    width=100,
    height=50,
)
    transcribed_text = ft.TextField(
    value="Aquí aparecerá el texto transcrito",
    multiline=True,
    read_only=True,
    width=400,   # ancho en píxeles
    height=200   # alto en píxeles
)
    





    # Diseño de la interfaz
    page.add(
    ft.Column(
            [
                
                ft.Text("Convierte tu audio a texto", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Pulsa start y comienza a hablar a tu micrófono", size=10, width=300, color=ft.Colors.GREEN, weight=ft.FontWeight.NORMAL),
                ft.Text("Pulsa stop cuando quiera terminar y veras el texto transcrito y se iniciara un archivo word con ese mismo texto", width=300, color=ft.Colors.GREEN, size=10, weight=ft.FontWeight.NORMAL),
                ft.Row([start_button, stop_button, clear_button], alignment=ft.MainAxisAlignment.CENTER),
                spinner,
                timer_text,
               # live_text,
                transcribed_text,

                
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )




if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.FLET_APP)