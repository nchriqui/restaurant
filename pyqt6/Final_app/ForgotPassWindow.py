# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_ForgotWwYRzh.ui'
##
## Created by: Qt User Interface Compiler version 6.2.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

from leftArrowButton import LeftArrowButton

class Ui_Forgot(object):
    def setupUi(self, Forgot):
        if not Forgot.objectName():
            Forgot.setObjectName(u"Forgot")
        Forgot.resize(520, 472)
        Forgot.setMinimumSize(QSize(520, 400))
        Forgot.setMaximumSize(QSize(520, 472))
        self.centralwidget = QWidget(Forgot)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QWidget#centralwidget{\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:1, x2:1, y2:0.023, stop:0 rgba(255, 140, 140, 255), stop:1 rgba(94, 122, 255, 255));\n"
"	border-radius: 20px;\n"
"}\n"
"\n"
"QFrame#frame{\n"
"	margin: 60px;\n"
"	border-radius: 20px;\n"
"	background-color: rgba(225, 228, 221, 120)\n"
"}\n"
"\n"
"QLineEdit{\n"
"	min-height: 45px;\n"
"	border-radius: 20px;\n"
"	background-color: #FFFFFF;\n"
"	padding-left: 20px;\n"
"	color: rgb(140, 140, 140);\n"
"}\n"
"\n"
"QLineEdit:hover{\n"
"	border: 2px solid rgb(139, 142, 139);\n"
"}\n"
"\n"
"QPushButton#valid_button{\n"
"	min-height: 45px;\n"
"	border-radius: 20px;\n"
"	background-color: rgb(140, 140, 140);\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"QPushButton#valid_button:hover{\n"
"	border: 2px solid rgb(255, 255, 255);\n"
"}\n"
"\n"
"QCheckBox{\n"
"	font-size: 10px;\n"
"	color: #FFFFFF;\n"
"}\n"
"\n"
"QLabel{\n"
"	color: rgb(95, 94, 108);\n"
"}\n"
"\n"
"QPushButton#close_button{\n"
"	background-color: rgb(186, 0, 0);\n"
"	border-radius: 6px;\n"
"}\n"
"\n"
"QPushButton#minimize_button{\n"
"	background-color: rgb(226, 226, 0);\n"
"	border-radius: 6px;\n"
"}\n"
"")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.top_bar = QFrame(self.centralwidget)
        self.top_bar.setObjectName(u"top_bar")
        self.top_bar.setMinimumSize(QSize(0, 30))
        self.top_bar.setMaximumSize(QSize(16777215, 30))
        self.top_bar.setFrameShape(QFrame.NoFrame)
        self.top_bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.top_bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.top_bar)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.back_button = LeftArrowButton(self.top_bar)
        self.back_button.setObjectName(u"back_button")
        
        # Ajouter le bouton au layout horizontal
        self.horizontalLayout.addWidget(self.back_button)

        self.horizontalLayout.addWidget(self.frame_4)

        self.frame_3 = QFrame(self.top_bar)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMaximumSize(QSize(60, 16777215))
        self.frame_3.setFrameShape(QFrame.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 5, 0)
        self.minimize_button = QPushButton(self.frame_3)
        self.minimize_button.setObjectName(u"minimize_button")
        self.minimize_button.setMaximumSize(QSize(12, 12))

        self.horizontalLayout_3.addWidget(self.minimize_button)

        self.close_button = QPushButton(self.frame_3)
        self.close_button.setObjectName(u"close_button")
        self.close_button.setMaximumSize(QSize(12, 12))

        self.horizontalLayout_3.addWidget(self.close_button)


        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout_2.addWidget(self.top_bar)

        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 40))
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.frame)
        self.lineEdit.setObjectName(u"lineEdit")

        self.verticalLayout.addWidget(self.lineEdit)

        self.lineEdit_2 = QLineEdit(self.frame)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.lineEdit_2)

        self.lineEdit_3 = QLineEdit(self.frame)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        self.lineEdit_3.setEchoMode(QLineEdit.Password)

        self.verticalLayout.addWidget(self.lineEdit_3)

        self.valid_button = QPushButton(self.frame)
        self.valid_button.setObjectName(u"valid_button")

        self.verticalLayout.addWidget(self.valid_button)



        self.bottom_frame = QFrame(self.frame)
        self.bottom_frame.setObjectName(u"bottom_frame")
        self.bottom_frame.setMaximumSize(QSize(16777215, 20))
        self.bottom_frame.setFrameShape(QFrame.NoFrame)
        self.bottom_frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout.addWidget(self.bottom_frame)


        self.verticalLayout_2.addWidget(self.frame)

        Forgot.setCentralWidget(self.centralwidget)

        self.retranslateUi(Forgot)

        QMetaObject.connectSlotsByName(Forgot)
    # setupUi

    def retranslateUi(self, Forgot):
        Forgot.setWindowTitle(QCoreApplication.translate("Forgot", u"Mot de passe oublié", None))
        self.minimize_button.setText("")
        self.close_button.setText("")
        self.label_2.setText(QCoreApplication.translate("Forgot", u"<html><head/><body><p><span style=\" font-size:20pt;\">Réinitialisation mot de passe</span></p></body></html>", None))
        self.lineEdit.setPlaceholderText(QCoreApplication.translate("Forgot", u"Adresse mail", None))
        self.lineEdit_2.setPlaceholderText(QCoreApplication.translate("Forgot", u"Mot de passe", None))
        self.lineEdit_3.setPlaceholderText(QCoreApplication.translate("Forgot", u"Confirmer mot de passe", None))
        self.valid_button.setText(QCoreApplication.translate("Forgot", u"Valider", None))
    # retranslateUi