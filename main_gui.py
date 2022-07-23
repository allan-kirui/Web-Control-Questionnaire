import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QFileDialog, QPushButton, QHBoxLayout

from main import Questionnaire


class WelcomeScreen(QDialog):
    browser = None

    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("UI/main_dialog.ui", self)
        self.passwordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.browse.clicked.connect(self.browsefiles)

        self.browserButton(self.edgeButton,"edge.ico")
        self.browserButton(self.firefoxButton, "firefox.ico")
        self.browserButton(self.chromeButton,"chrome.ico")
        self.submitButton.setStyleSheet("QPushButton { border-radius: 50px;}")

        # Browser handling
        if self.edgeButton.clicked.connect(lambda: self.browserSelect("Edge")):
            print("Edge")
        if self.firefoxButton.clicked.connect(lambda: self.browserSelect("Firefox")):
            print("Firefox")
        if self.chromeButton.clicked.connect(lambda: self.browserSelect("Chrome")):
            print("Chrome")

        # Submit button
        if self.submitButton.clicked.connect(self.submit):
            self.submitButton.setStyleSheet("QPushButton:pressed { background-color: green }")

    def browsefiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Pick file with list of Professors')
        self.filename.setText(fname[0])

    def submit(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        filepath = self.filename.text()

        if len(username) != 7 or len(password) == 0 or len(filepath) == 0:
            self.error.setText("Please input all fields")
        else:
            Questionnaire(username, password, filepath,self.browser)

    def browserButton(self,browserButton,iconName):
        browserButton.setStyleSheet("QPushButton { background-color: white;"
                                      "min-width:  60px; max-width:  60px;"
                                      "min-height: 60px; max-height: 60px;"
                                      "border-radius: 30px; }"
                                      "QPushButton:pressed { background-color: green }"
                                      "QPushButton:focus { background-color: green}"
                                      )
        browserButton.setIcon(QIcon("browser-icons/"+iconName))
        browserButton.setIconSize(QSize(30, 30))

    def browserSelect(self,browser):
        self.browser = browser

# menu
app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(600)
widget.setFixedWidth(900)
widget.show()
try:
    sys.exit(app.exec())
except Exception as e:
    print(e)
