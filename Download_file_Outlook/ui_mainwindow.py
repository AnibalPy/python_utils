import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QDateEdit, QHBoxLayout
from search_emails import OutlookEmailHandler
from PyQt6.QtCore import QDate

from datetime import datetime
from downloads_attachtment import PDFDownloader






class FacturaApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        
        self.event_handler()

  #settings
    def settings(self):
        self.setWindowTitle("Invoice Manager")
        self.setGeometry(900, 600, 600, 300)
      #  self.setGeometry(300, 100, 1100, 700)



  # Design
    def initUI(self):
        self.title = QLabel("Invoice Management")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.subtitle = QLabel("Buscar facturas recibidas en pdf en todas mis cuentas de correo electrónico.")
        self.subtitle.setObjectName("subtitle")
        self.btn_opener = QPushButton("Buscar facturas")
        # ...otros widgets...


        self.master = QVBoxLayout()
        self.master.addWidget(self.title)  
        self.master.addWidget(self.subtitle)
      
        self.master.addWidget(self.btn_opener)
        
# ...luego el resto de widgets...


        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: green;")
        self.time_label.hide()  # Ocúltalo al inicio

     #   self.master.addWidget(self.btn_opener)

     # widgets de fechas a buscar 
        self.label_desde = QLabel("Desde:")
        self.date_desde = QDateEdit()
        self.date_desde.setCalendarPopup(True)
        self.date_desde.setDate(QDate.currentDate())
        self.label_hasta = QLabel("Hasta:")
        self.date_hasta = QDateEdit()
        self.date_hasta.setCalendarPopup(True)
        self.date_hasta.setDate(QDate.currentDate())

 

        search_row = QHBoxLayout()
        search_row.addWidget(self.btn_opener)
        search_row.addWidget(self.label_desde)
        search_row.addWidget(self.date_desde)
        search_row.addWidget(self.label_hasta)
        search_row.addWidget(self.date_hasta)
        
        

        self.file_list = QListWidget()
        
        self.btn_download = QPushButton("Descargar facturas")
        self.btn_print= QPushButton("Imprimir Facturas")
        self.btn_print_manual = QPushButton("Impresión Manual")
        
        self.btn_stop = QPushButton("Stop")


    

        #deactivate buttons for now
 

     




        #create layouts

        self.master = QVBoxLayout()
        self.master.addWidget(self.title)
        self.master.addWidget(self.subtitle)
        self.master.addWidget(self.btn_opener)
        self.master.addLayout(search_row)
        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

      
        


        
      #  col1.addWidget(self.btn_opener)
        col1.addWidget(self.btn_download)
        col1.addWidget(self.btn_print) 
        col1.addWidget(self.btn_print_manual)
        col1.addWidget(self.btn_stop) 

        col2.addWidget(self.file_list)

        row.addLayout(col1)
        row.addLayout(col2)

        self.master.addLayout(row)
        self.setLayout(self.master)

        self.style()



  # Style methods

    def style(self):
        self.setStyleSheet("""

                            QWidget {
                                background-color: #04274f;
                            }
                            QPushButton {
                                background-color: #529df1;  
                                color: #333;
                                border-radius: 10px; 
                                padding: 4px 10px;      /* Menos padding vertical para menor altura */
                                font-size: 12px;        /* Tamaño de fuente más pequeño */
                                min-height: 28px;       /* Altura mínima del botón */
                                max-height: 32px;       /* Altura máxima del botón */
                            }
                            QPushButton:hover {
                                background-color: #1A4870;  
                                color: #F9DBBA;                                        
                            }    
                            QLabel {
                                color: #333;

                            }         
                            #title {
                                font-family: 'Arial';
                                font-size:40px;
                                
                            }
                            QSlider:{
                                margin-right: 15px;
                            }
                            QlistWidget {
                                color: #333;
                          
                            }
                            #subtitle {
                                font-size: 18px;
                                color: #2ecc40;   /* Verde */
                                font-family: 'Arial';
                            }

                            """)
     

  


  # Event handlers 
    def event_handler(self):
        self.btn_opener.clicked.connect(self.buscar_facturas)
        self.btn_download.clicked.connect(self.descargar_facturas)

     #   self.btn_opener.clicked.connect(self.audio_methods.open_file)
     #   self.btn_play.clicked.connect(self.audio_methods.play_audio)
     #   self.btn_pause.clicked.connect(self.audio_methods.pause_audio)
     #   self.btn_resume.clicked.connect(self.audio_methods.resume_audio)
     #   self.btn_reset.clicked.connect(self.audio_methods.reset_audio)
     #   self.btn_stop.clicked.connect(self.audio_methods.stop_audio)
       # pass


# metodos para buscar facturas
    def buscar_facturas(self):
        self.file_list.clear()
        self.mensajes_por_cuenta = {}  # <-- Aquí inicializas el diccionario
        fecha_inicio = datetime.combine(self.date_desde.date().toPyDate(), datetime.min.time())
        fecha_fin = datetime.combine(self.date_hasta.date().toPyDate(), datetime.max.time())
        cuentas = OutlookEmailHandler.get_outlook_accounts()
        for cuenta in cuentas:
            try:
                correos_dict, correos_sin_adjuntos, mensajes_a_descargar = OutlookEmailHandler.get_inbox(
                    cuenta, fecha_inicio, fecha_fin
                )
                self.mensajes_por_cuenta[cuenta] = mensajes_a_descargar  # <-- Guardas los mensajes por cuenta
                for fecha, mensaje in zip(correos_dict.keys(), mensajes_a_descargar):
                    self.file_list.addItem(f"{cuenta} | {fecha} | {mensaje.Subject}")
            except Exception as e:
                print(f"Error procesando la cuenta {cuenta}: {e}")

    def descargar_facturas(self):
        # Asume que self.mensajes_por_cuenta es un diccionario: {cuenta: [mensajes]}
        for cuenta, mensajes in self.mensajes_por_cuenta.items():
            carpeta_cuenta = f"./invoices_pdfs_downloads/{cuenta}"
            downloader = PDFDownloader(carpeta_cuenta)
            downloader.descargar_adjuntos(mensajes)
        # Luego, actualiza la lista de archivos PDF encontrados
        self.file_list.clear()
        for root, dirs, files in os.walk("./invoices_pdfs_downloads"):
            for file in files:
                if file.lower().endswith('.pdf'):
                    self.file_list.addItem(file)      



