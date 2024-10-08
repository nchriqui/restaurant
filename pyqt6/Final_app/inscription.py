import re
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen

from InscriptionWindow import Ui_Inscription
from login_appli import *


class InscriptionUI(QMainWindow, Ui_Inscription):
    def __init__(self):
        super(InscriptionUI, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.inscription_button.clicked.connect(self.inscription)
        self.login_button.clicked.connect(self.goLogin)
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(self.minimize)

    def inscription(self):
        lastname = self.lineEdit.text()
        firstname = self.lineEdit_2.text()
        mail = self.lineEdit_3.text()
        password = self.lineEdit_4.text()

        # Vérification de l'adresse e-mail
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        is_valid_email = re.match(pattern, mail)

        if is_valid_email:
            # L'adresse e-mail est valide
            print("Adresse e-mail valide")
            if new_user(lastname, firstname, password, mail) == 0:
                from main import LoginUI
                self.login_window = LoginUI()
                self.login_window.show()
                self.close()
            elif new_user(lastname, firstname, password, mail) == -2:
                QMessageBox.critical(self, "Inscription invalide", "Un compte avec cette adresse mail existe déjà")
                print("Un compte avec cette adresse mail existe déjà")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_4.clear()
            else:
                QMessageBox.critical(self, "Inscription invalide", "Nom, Prénom, Adresse mail ou mot de passe invalide")
                print("Nom, Prénom, Adresse mail ou mot de passe invalide")
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_4.clear() 
        else:
            # L'adresse e-mail n'est pas valide
            QMessageBox.critical(self, "Inscription invalide", "Adresse mail invalide")
            print("Adresse e-mail invalide")
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()


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

    w = InscriptionUI()
    w.show()

    app.exec()