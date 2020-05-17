import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parts Inventory Manager")
        self.setWindowIcon(QIcon("icons/icon.png"))
        self.setGeometry(10, 50, 1350,650)
        self.setFixedSize(self.size())

        self.UI()
        self.show()

    def UI(self):
        pass

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()