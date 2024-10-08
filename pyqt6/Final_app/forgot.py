from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen

from ForgotPassWindow import Ui_Forgot
from login_appli import *

class ForgotUI(QMainWindow, Ui_Forgot):
    def __init__(self):
        super(ForgotUI, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.valid_button.clicked.connect(self.update)
        self.back_button.clicked.connect(self.goLogin)
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(self.minimize)

    def update(self):
        mail = self.lineEdit.text()
        password = self.lineEdit_2.text()   
        conf_password = self.lineEdit_3.text()

        if password == conf_password:
            if update_password(password, mail) == 0:
                from main import LoginUI
                self.login_window = LoginUI()
                self.login_window.show()
                self.close()  
            elif update_password(password, mail) == -2:
                QMessageBox.critical(self, "Modification invalide", "Il n'existe pas de compte avec cette adresse mail")
                print("Il n'existe pas de compte avec cette adresse mail")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
            else:
                QMessageBox.critical(self, "Modification invalide", "Adresse mail ou mot de passe invalide")
                print("Adresse mail ou mot de passe invalide")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
        else:
            QMessageBox.critical(self, "Modification invalide", "Mots de passe différents")
            print("Mots de passe différents")

    def goLogin(self):
        from main import LoginUI
        self.login_window = LoginUI()
        self.login_window.show()
        self.close()  

    def close(self):
        return super().close()

    def minimize(self):
        self.showMinimized()

if __name__ == '__main__':
    app = QApplication([])

    w = ForgotUI()
    w.show()

    app.exec()