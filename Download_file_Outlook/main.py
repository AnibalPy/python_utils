

from PyQt6.QtWidgets import QApplication
from ui_mainwindow import FacturaApp



if __name__ == "__main__":
    app = QApplication([])
    window = FacturaApp()
    window.show()
    app.exec()