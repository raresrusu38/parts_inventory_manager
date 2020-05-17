from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

import sys
from os import path

from PyQt5.uic import loadUiType

FORM_CLASS,_ = loadUiType(path.join(path.dirname('__file__'), 'main.ui'))

import sqlite3

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setGeometry(50, 30, 1265,695)
        self.setFixedSize(self.size())
        self.setupUi(self)
        self.Handle_Buttons()


    def Handle_Buttons(self):
        self.refresh_btn.clicked.connect(self.getData)
        self.search_btn.clicked.connect(self.search)

    def getData(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect('parts.db')
        cursor = db.cursor()

        query = ''' SELECT * FROM parts_table'''

        result = cursor.execute(query)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Display references number and type number in Statistics tab



        # Display 4 results: Min, Max, Nbr of Holes in addition to their respective references number

    def search(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect('parts.db')
        cursor = db.cursor()

        nbr = int(self.count_filter_txt.text())

        query = ''' SELECT * FROM parts_table WHERE count < ?'''

        result = cursor.execute(query, [nbr])

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


        

    
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()