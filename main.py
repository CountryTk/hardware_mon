from PyQt5 import QtTest
import subprocess
from PyQt5.QtWidgets import QWidget, QProgressBar, QApplication, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QPoint, QProcess
import sys
import psutil
import time


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
       # self.setFixedSize(230,60)
        
        self.setWindowFlags(
            Qt.Widget |
            Qt.WindowCloseButtonHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )
        
        self.setParent(None)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle("Monitor")
        self.threading = ThreadClass()
        self.m_nMouseClick_X_Coordinate = None
        self.m_nMouseClick_Y_Coordinate = None
        self.threading2 = ThreadClass2()
        self.threading3 = Temperature_thread()
        self.threading3.start()
        self.threading2.start()
        self.threading.start()
        self.progress_stylesheet = """
        
        
        QProgressBar {
        border: 2px solid transparent;
        
        background-color: transparent;
        font-weight: bold;
        font-size: 13px;
        margin-left: -6px;
        }

        QProgressBar::chunk {
        background-color: #00ff00;
        width: 29px;
        
        
        }
        
        """
        
        self.temp_stylesheet = """
        
        QProgressBar {
        border: 2px solid transparent;
        
        background-color: transparent;
        font-weight: bold;
        font-size: 13px;
        margin-left: -6px;
        }

        QProgressBar::chunk {
        background-color: #00ff00;
        
        }
        
        """
        
        self.oldPos = self.pos()
        self.threading2.signal2.connect(self.ram_val)
        self.threading.signal.connect(self.cpu_val)
        self.threading3.signal3.connect(self.cpu_temp_val)

        self.initUI()


    def initUI(self):
        
        self.ram = QProgressBar(self)
        self.ram.setValue(100)
        
        self.cpu = QProgressBar(self)
        self.cpu.setValue(100)
        
        self.cpu_temp = QProgressBar(self)
        self.cpu_temp.setValue(100)
        self.cpu_temp.setFormat("%p°C")
        
        self.main_layout = QVBoxLayout()
        self.ram_layout = QHBoxLayout()
        self.cpu_layout = QHBoxLayout()
        self.cpu_temp_layout = QHBoxLayout()
        
        self.ram_text = QLabel("<h3>RAM USAGE:</h3> ", self)
        self.ram_text.setStyleSheet("color: #00ff00")
        
        self.cpu_value_text = QLabel("<h3>CPU TEMP:</h3> ", self)
        self.cpu_value_text.setStyleSheet("color: #00ff00") 
               
        self.cpu_text = QLabel("<h3>CPU USAGE:</h3> ", self)
        self.cpu_text.setStyleSheet("color: #00ff00")
        
        
        self.cpu_temp_layout.addWidget(self.cpu_value_text)
        self.cpu_temp_layout.addWidget(self.cpu_temp)
        
        self.ram_layout.addWidget(self.ram_text)
        self.ram_layout.addWidget(self.ram)
        
        self.cpu_layout.addWidget(self.cpu_text)
        self.cpu_layout.addWidget(self.cpu)
        
        self.main_layout.addLayout(self.ram_layout)
        self.main_layout.addLayout(self.cpu_layout)
        self.main_layout.addLayout(self.cpu_temp_layout)
        
        self.cpu.setStyleSheet(self.progress_stylesheet)
        self.ram.setStyleSheet(self.progress_stylesheet)
        self.cpu_temp.setStyleSheet(self.temp_stylesheet)
        self.cpu_text.move(0, 35)
        
        self.setLayout(self.main_layout)
        self.show()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def ram_val(self, ram_value):
        self.ram.setValue(ram_value)

    def cpu_val(self, cpu_value):
        self.cpu.setValue(cpu_value)
        
    def cpu_temp_val(self, temp_value):
        self.cpu_temp.setValue(temp_value)


class ThreadClass(QThread):
    signal = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            value = psutil.cpu_percent(interval=1, percpu=True)
            cpu_value = sum(value) / len(value)


            self.signal.emit(cpu_value)
            time.sleep(0.3)


class ThreadClass2(QThread):
    signal2 = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            r_value = psutil.virtual_memory()
            ram_value = r_value[2]

            self.signal2.emit(ram_value)
            time.sleep(0.3)


class Temperature_thread(QThread):
    
    signal3 = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        
    def run(self):
        self.process = QProcess()
        
        while True:
            self.process.start("cat /sys/class/thermal/thermal_zone0/temp")
            self.process.waitForFinished(-1)
            temp_value = int(self.process.readAllStandardOutput())/1000
            self.signal3.emit(temp_value)
            time.sleep(0.3)
            
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Window()
    sys.exit(app.exec_())
    





