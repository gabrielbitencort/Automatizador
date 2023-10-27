from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(444, 274)
        Dialog.setMaximumSize(QSize(444, 274))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(90, 60, 58, 41))
        self.label_2.setStyleSheet(u"image: url(:/img/user2.svg);")
        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(90, 120, 58, 31))
        self.label_3.setStyleSheet(u"image: url(:/img/lock.svg);")
        self.btn_enter = QPushButton(Dialog)
        self.btn_enter.setObjectName(u"btn_enter")
        self.btn_enter.setGeometry(QRect(50, 180, 90, 28))
        self.btn_exit = QPushButton(Dialog)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(300, 180, 90, 28))
        self.edit_name = QLineEdit(Dialog)
        self.edit_name.setObjectName(u"edit_name")
        self.edit_name.setGeometry(QRect(150, 70, 201, 28))
        self.edit_passwd = QLineEdit(Dialog)
        self.edit_passwd.setObjectName(u"edit_passwd")
        self.edit_passwd.setGeometry(QRect(150, 120, 201, 28))
        self.edit_passwd.setEchoMode(QLineEdit.Password)
        self.verticalLayoutWidget = QWidget(Dialog)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 441, 51))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalLayoutWidget_2 = QWidget(Dialog)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 229, 441, 31))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(10, 0, 0, 0)
        self.label_4 = QLabel(self.verticalLayoutWidget_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><br/></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><br/></p></body></html>", None))
        self.btn_enter.setText(QCoreApplication.translate("Dialog", u"ENTRAR", None))
        self.btn_exit.setText(QCoreApplication.translate("Dialog", u"SAIR", None))
        self.edit_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"Digite seu nome:", None))
        self.edit_passwd.setPlaceholderText(QCoreApplication.translate("Dialog", u"Digite sua senha:", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:11pt; font-weight:600;\">AUTOMATIZADOR DE E-MAILS</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-weight:600; color:#000000;\">Esqueceu sua senha?</span></p></body></html>", None))
    # retranslateUi
