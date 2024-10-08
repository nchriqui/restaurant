from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QScreen

from LoginWindow import Ui_Login
from login_appli import *

class LoginUI(QMainWindow, Ui_Login):
    def __init__(self):
        super(LoginUI, self).__init__()
        self.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.login_button.clicked.connect(self.authenticate)
        self.inscription_button.clicked.connect(self.goInscription)
        self.forgot_button.clicked.connect(self.goForgot)
        self.manager_button.clicked.connect(self.goManager)
        self.close_button.clicked.connect(self.close)
        self.minimize_button.clicked.connect(self.minimize)

    def close(self):
        return super().close()

    def minimize(self):
        self.showMinimized()

    def authenticate(self):
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()

        user_id = get_user(password, email)
        if user_id != -1:
            from reco import RecoUI
            self.reco_window = RecoUI(user_id)
            self.reco_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Connexion invalide", "Adresse mail ou mot de passe invalide")
            print("Adresse mail ou mot de passe invalide")
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def goInscription(self):
        from inscription import InscriptionUI
        self.inscription_window = InscriptionUI()
        self.inscription_window.show()
        self.close()

    def goForgot(self):
        from forgot import ForgotUI
        self.forgot_window = ForgotUI()
        self.forgot_window.show()
        self.close()

    def goManager(self):
        from ManagerWindow import MainWindow
        self.manager_window = MainWindow()
        self.manager_window.show()
        self.close()    



if __name__ == '__main__':
    app = QApplication([])

    w = LoginUI()
    w.show()

    app.exec()