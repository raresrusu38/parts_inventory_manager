from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication

from styles import classic, dark_orange, dark_blue

import sys, os
from os import path

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

from PyQt5.uic import loadUiType

FORM_CLASS,_ = loadUiType(resource_path("main.ui"))

import sqlite3

app = QApplication(sys.argv)

class Main(QMainWindow, FORM_CLASS):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setGeometry(50, 30, 1265,695)
        self.setFixedSize(self.size())
        self.setupUi(self)
        self.Handle_Buttons()
        self.navigate()  

    def Handle_Buttons(self):
        self.refresh_btn.clicked.connect(self.getData)
        self.search_btn.clicked.connect(self.search)
        self.check_btn.clicked.connect(self.level)
        self.update_btn.clicked.connect(self.update)
        self.delete_btn.clicked.connect(self.delete)
        self.add_btn.clicked.connect(self.add)
        self.theme1_btn.clicked.connect(self.change_theme_1)
        self.theme2_btn.clicked.connect(self.change_theme_2)
        self.theme3_btn.clicked.connect(self.change_theme_3)

    def getData(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        query = ''' SELECT * FROM parts_table'''

        result = cursor.execute(query)

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        # Display references number and type number in Statistics tab
        cursor2 = db.cursor()
        cursor3 = db.cursor()

        parts_nbr = ''' SELECT COUNT (DISTINCT PartName) FROM parts_table '''
        ref_nbr = ''' SELECT COUNT (DISTINCT Reference) FROM parts_table '''

        result_parts_nbr = cursor2.execute(parts_nbr,)
        result_ref_nbr = cursor3.execute(ref_nbr,)

        self.lbl_parts_nbr.setText(str(result_parts_nbr.fetchone()[0]))
        self.lbl_ref_nbr.setText(str(result_ref_nbr.fetchone()[0]))

        # Display 4 results: Min, Max, Nbr of Holes in addition to their respective references number
        cursor4 = db.cursor()
        cursor5 = db.cursor()

        min_hole = ''' SELECT MIN(NumberOfHoles), Reference FROM parts_table '''
        max_hole = ''' SELECT MAX(NumberOfHoles), Reference FROM parts_table '''

        result_min_hole = cursor4.execute(min_hole)
        result_max_hole = cursor5.execute(max_hole)

        r1 = result_min_hole.fetchone()
        r2 = result_max_hole.fetchone()

        self.lbl_min_hole.setText(str(r1[0]))
        self.lbl_max_hole.setText(str(r2[0]))

        self.lbl_min_hole_4.setText(str(r1[1]))
        self.lbl_max_hole_2.setText(str(r2[1]))


    def search(self):
        nbr = int(self.count_filter_txt.text())

        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        query = ''' SELECT * FROM parts_table WHERE count < ?'''

        result = cursor.execute(query, [nbr])

        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def level(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        query = ''' SELECT Reference, PartName, Count FROM parts_table order by Count asc LIMIT 3'''

        result = cursor.execute(query,)

        self.table2.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table2.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    
    def navigate(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        query = ''' SELECT * FROM  parts_table '''

        result = cursor.execute(query,)

        val = result.fetchone()

        self.id.setText(str(val[0]))
        self.reference.setText(str(val[1]))
        self.part_name.setText(str(val[2]))
        self.min_area.setText(str(val[3]))
        self.max_area.setText(str(val[4]))
        self.number_of_holes.setText(str(val[5]))
        self.min_diameter.setText(str(val[6]))
        self.max_diameter.setText(str(val[7]))
        self.count.setValue(val[8])


    def update(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        id_ = int(self.id.text())
        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_, id_)

        query = ''' UPDATE parts_table SET 
                Reference = ?, PartName = ?, MinArea = ?, MaxArea = ?, NumberOfHoles = ?, 
                MinDiameter = ?, MaxDiameter = ?, Count = ? 
                WHERE ID = ?
        '''

        cursor = cursor.execute(query, row)
        db.commit()

    
    def delete(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        d = self.id.text()

        query = ''' DELETE FROM parts_table WHERE ID = ? '''

        cursor.execute(query, d)
        db.commit()


    def add(self):
        # Connect to SQLite and fill GUI table with data
        db = sqlite3.connect(resource_path('parts.db'))
        cursor = db.cursor()

        reference_ = self.reference.text()
        part_name_ = self.part_name.text()
        min_area_ = self.min_area.text()
        max_area_ = self.max_area.text()
        number_of_holes_ = self.number_of_holes.text()
        min_diameter_ = self.min_diameter.text()
        max_diameter_ = self.max_diameter.text()
        count_ = str(self.count.value())

        row = (reference_,part_name_,min_area_,max_area_,number_of_holes_,min_diameter_,max_diameter_,count_)

        query = ''' INSERT INTO parts_table (Reference, PartName, MinArea, MaxArea, NumberOfHoles, MinDiameter, MaxDiameter, Count) 
            VALUES (?,?,?,?,?,?,?,?)
        '''

        cursor = cursor.execute(query, row)
        db.commit()


    def change_theme_1(self):
        app.setStyleSheet(classic.mainWindowStyle())


    def change_theme_2(self):
        app.setStyleSheet(dark_orange.mainWindowStyle())


    def change_theme_3(self):
        app.setStyleSheet(dark_blue.mainWindowStyle())

    
def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()