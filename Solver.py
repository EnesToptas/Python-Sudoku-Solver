from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import numpy as np
from collections import deque


class myWidget(QtWidgets.QLineEdit):
    def __init__(self,form,index):
        super().__init__(form)
        self.this_index = index
    def updateValue(self):
        if(self.text() == ''):
            theGame.board[self.this_index//9,self.this_index%9] = 0
        else:
            theGame.board[self.this_index//9,self.this_index%9] = int(self.text())

class Ui_Form(QWidget):

    def clearTable(self):
        for i in range(81):
            self.boxes[i].setText("")
            self.boxes[i].setStyleSheet("background-color: rgb(245, 245, 245); border: 1px solid white")
            theGame.board[i//9,i%9] = 0
    
    def colorful(self,new_boxes):
        for i in new_boxes:
            self.boxes[i].setText(str(theGame.board[i//9,i%9]))
            self.boxes[i].setStyleSheet("background-color: #ffb0cd; border: 1px solid white; color: #FFFFFF")
    
    def setupUi(self, Form):
        self.setStyleSheet("border-top-left-radius:15px;border-top-right-radius:5px")
        Form.setObjectName("Form")
        Form.resize(610, 540)
        
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(22)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        validator = QtGui.QRegularExpressionValidator()
        validator.setRegularExpression(QtCore.QRegularExpression("[1-9]*"))

        self.boxes = []
        for i in range(81):
            self.boxes.append(myWidget(Form,i))
            self.boxes[i].setGeometry(QtCore.QRect((i%9)*60, (i//9)*60, 60, 60))
            self.boxes[i].setSizePolicy(sizePolicy)
            self.boxes[i].setFont(font)
            self.boxes[i].setStyleSheet("background-color: rgb(245, 245, 245); border: 1px solid white")
            self.boxes[i].setAlignment(QtCore.Qt.AlignCenter)
            self.boxes[i].raise_()
            self.boxes[i].setValidator(validator)
            self.boxes[i].editingFinished.connect(self.boxes[i].updateValue)

        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(180, 0, 5, 540))
        self.line.setStyleSheet("color:#9e9e9e")
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Form)
        self.line_2.setGeometry(QtCore.QRect(360, 0, 5, 540))
        self.line_2.setStyleSheet("color:#9e9e9e")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setLineWidth(5)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(Form)
        self.line_3.setGeometry(QtCore.QRect(0, 180, 540, 5))
        self.line_3.setStyleSheet("color:#9e9e9e")
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setLineWidth(5)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(Form)
        self.line_4.setGeometry(QtCore.QRect(0, 360, 540, 5))
        self.line_4.setStyleSheet("color:#9e9e9e")
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setLineWidth(5)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setObjectName("line_4")


        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(540, 0, 70, 270))
        self.pushButton.setStyleSheet("background-color : #212121; color : #FFFFFF")
        self.pushButton.setFont(font)
        self.pushButton.setText("Solve")
        self.pushButton.clicked.connect(theGame.solve)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(540, 270, 70, 230))
        self.pushButton_2.setStyleSheet("background-color : #212121; color : #FFFFFF")
        self.pushButton_2.setFont(font)
        self.pushButton_2.setText("Clear")
        self.pushButton_2.clicked.connect(self.clearTable)
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(540, 500, 70, 40))
        self.pushButton_3.setStyleSheet("background-color : #ff8a80; color : #FFFFFF")
        self.pushButton_3.setFont(font)
        self.pushButton_3.setText("X")
        self.pushButton_3.clicked.connect(w.close)

        

        self.pushButton.raise_()
        self.pushButton_2.raise_()
        
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.line_4.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

class SudokuGame():

    def __init__(self):
        self.board = np.zeros([9,9],dtype ='int8')

    def checkConstraints(self,x,y,v):
        boxx= int(x/3)
        boxy= int(y/3)
        for i in range(9):
            if(v == self.board[y][i] and x!=i):
                return False
            if(v == self.board[i][x] and y!=i):
                return False
        for i in range(3*boxy,3*boxy+3):
            for j in range(3*boxx , 3*boxx+3):
                if(v == self.board[i][j] and (i,j)!=(y,x)):
                    return False
        return True

    def cellToFill(self):
        if(len(self.emptyEntries) == 0):
            return True
        cell = self.emptyEntries.popleft()
        cell_x = cell%9;
        cell_y = int(cell/9);
        for numb in range(1,10):
            if(self.checkConstraints(cell_x,cell_y,numb)):
                self.board[cell_y,cell_x] = numb
                if(not self.cellToFill()):
                    self.board[cell_y,cell_x] = 0
                    continue
        if (self.board[cell_y,cell_x] == 0):
            self.emptyEntries.appendleft(cell)
            return False
        return True

    def solve(self):
        self.emptyEntries = deque()
        for i in range(9):
            for j in range(9):
                if(not self.checkConstraints(j,i,self.board[i,j]) and self.board[i,j]!=0):
                    error_dialog = QtWidgets.QErrorMessage()
                    error_dialog.showMessage('Oh no! Please clean the table >:(')
                    error_dialog.exec_()
                    return
                if(self.board[i,j] == 0):
                    self.emptyEntries.append(i*9+j)
        self.pink_boxes = self.emptyEntries.copy()
        self.cellToFill()
        ui.colorful(self.pink_boxes)


import sys
theGame = SudokuGame()
app = QtWidgets.QApplication(sys.argv)
w = QtWidgets.QMainWindow()
ui = Ui_Form()
w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
ui.setupUi(w)
w.show()
sys.exit(app.exec_())
