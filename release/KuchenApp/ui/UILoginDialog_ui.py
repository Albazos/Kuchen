# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UILoginDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(400, 300)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labInfo = QLabel(Dialog)
        self.labInfo.setObjectName(u"labInfo")
        self.labInfo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.labInfo)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.labMail = QLabel(Dialog)
        self.labMail.setObjectName(u"labMail")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.labMail)

        self.labPsw = QLabel(Dialog)
        self.labPsw.setObjectName(u"labPsw")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.labPsw)

        self.ledUser = QLineEdit(Dialog)
        self.ledUser.setObjectName(u"ledUser")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ledUser)

        self.ledPsw = QLineEdit(Dialog)
        self.ledPsw.setObjectName(u"ledPsw")
        self.ledPsw.setEchoMode(QLineEdit.EchoMode.Password)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.ledPsw)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pbnLogin = QPushButton(Dialog)
        self.pbnLogin.setObjectName(u"pbnLogin")

        self.horizontalLayout.addWidget(self.pbnLogin)

        self.pbnCancel = QPushButton(Dialog)
        self.pbnCancel.setObjectName(u"pbnCancel")

        self.horizontalLayout.addWidget(self.pbnCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labInfo.setText(QCoreApplication.translate("Dialog", u"Iserv Mail Login", None))
        self.labMail.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.labPsw.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.pbnLogin.setText(QCoreApplication.translate("Dialog", u"Login", None))
        self.pbnCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
    # retranslateUi

