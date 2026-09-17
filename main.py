import os
import sys
import ctypes

if sys.platform == 'win32':
    myappid = 'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui import TestWindow

if __name__ == "__main__":
    app = QApplication(sys.argv) #pyinstaller Призёр.spec

    icon_path = "icon.ico" 
    
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
    
    app.setStyle("Fusion") 

    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())