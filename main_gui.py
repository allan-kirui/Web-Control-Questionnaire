import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog

from main import Questionnaire


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("main_dialog.ui",self)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.browse.clicked.connect(self.browsefiles)
        self.submitButton.clicked.connect(self.submit)

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self,'Pick file with list of Professors')
        self.filename.setText(fname[0])

    def submit(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        filepath = self.filename.text()

        if len(username) != 7 or len(password) == 0 or len(filepath) == 0:
            self.error.setText("Please input all fields")
        else:
            Questionnaire(username,password,filepath)

#menu
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(900)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exit")

