import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QPushButton, QLineEdit, QComboBox, QStatusBar
from PyQt5 import uic
import ctypes, psutil, threading

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        
        #Load File gui
        uic.loadUi("./GUI/interface.ui", self)
        
        #Widgets
        self.process = self.findChild(QComboBox, "comboBox")
        self.dll_path = self.findChild(QLineEdit, "lineEdit")
        self.open_dll_btn = self.findChild(QPushButton, "pushButton")
        self.inject_btn = self.findChild(QPushButton, "pushButton_2")
        self.refresh_btn = self.findChild(QPushButton, "pushButton_3")
        self.status_bar = self.findChild(QStatusBar, "statusbar")


        #Variables
        self.BLUEBERRY_INJECTOR_DLL = ctypes.WinDLL("./BlueberryInjector.dll")
        self.BLUEBERRY_INJECTOR_DLL.InjectDLL.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.BLUEBERRY_INJECTOR_DLL.restype = ctypes.c_int

        #Init widgets
        self.existing_process()
        
        #Actions Widgets
        self.open_dll_btn.clicked.connect(self.open_dll)
        self.inject_btn.clicked.connect(lambda : threading.Thread(target=self.inject_dll).start())
        self.refresh_btn.clicked.connect(lambda : threading.Thread(target=self.existing_process).start())

        #Show App
        self.show()
    
    def existing_process(self):
        self.process.clear()
        existing_process = []

        for process in psutil.process_iter():
            try:
                existing_process.append([process.name(), process.pid])
            except:
                pass
        
        self.process.addItems(process[0] for process in sorted(existing_process, key=lambda x: x[0]) if process[0] != "")

    def get_PID(self):
        for process in psutil.process_iter():
            if process.name() == self.process.currentText():
                return process.pid
        return 0

    def open_dll(self):
        file_path = QFileDialog.getOpenFileName(self, "Open DLL", "", "Dynamic Link Library (*.dll)")
        self.dll_path.setText(file_path[0])

    def inject_dll(self):
        self.inject_btn.setEnabled(False)
        
        dll_path = self.dll_path.text()
        if dll_path == "":
            self.status_bar.showMessage("DLL path missing !", 3000)
            return
        
        pid = self.get_PID()
        if pid == 0:
            self.status_bar.showMessage("Process not found !", 3000)
            return

        try:
            self.BLUEBERRY_INJECTOR_DLL.InjectDLL(dll_path.encode(), pid)
            self.status_bar.showMessage("DLL successfully injected !", 3000)
        except:
            self.status_bar.showMessage("Error during DLL injection !", 3000)
        
        self.inject_btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())  