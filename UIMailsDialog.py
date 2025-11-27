# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIMailsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QRadioButton, QSizePolicy, QTableView, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(694, 409)
        self.horizontalLayout_4 = QHBoxLayout(Dialog)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableView = QTableView(Dialog)
        self.tableView.setObjectName(u"tableView")

        self.horizontalLayout_2.addWidget(self.tableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labSearch = QLabel(Dialog)
        self.labSearch.setObjectName(u"labSearch")
        self.labSearch.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_2.addWidget(self.labSearch)

        self.leSearch = QLineEdit(Dialog)
        self.leSearch.setObjectName(u"leSearch")
        self.leSearch.setClearButtonEnabled(False)

        self.verticalLayout_2.addWidget(self.leSearch)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labSort = QLabel(Dialog)
        self.labSort.setObjectName(u"labSort")
        self.labSort.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.labSort)

        self.rbnName = QRadioButton(Dialog)
        self.rbnName.setObjectName(u"rbnName")
        self.rbnName.setEnabled(True)
        self.rbnName.setChecked(True)

        self.verticalLayout.addWidget(self.rbnName)

        self.rbnMail = QRadioButton(Dialog)
        self.rbnMail.setObjectName(u"rbnMail")

        self.verticalLayout.addWidget(self.rbnMail)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbnQuit = QPushButton(Dialog)
        self.pbnQuit.setObjectName(u"pbnQuit")

        self.gridLayout.addWidget(self.pbnQuit, 3, 1, 1, 1)

        self.pbnImport = QPushButton(Dialog)
        self.pbnImport.setObjectName(u"pbnImport")

        self.gridLayout.addWidget(self.pbnImport, 1, 0, 1, 1)

        self.pbnAdd = QPushButton(Dialog)
        self.pbnAdd.setObjectName(u"pbnAdd")
        self.pbnAdd.setEnabled(True)

        self.gridLayout.addWidget(self.pbnAdd, 2, 1, 1, 1)

        self.pbnSave = QPushButton(Dialog)
        self.pbnSave.setObjectName(u"pbnSave")

        self.gridLayout.addWidget(self.pbnSave, 1, 1, 1, 1)

        self.labInfo = QLabel(Dialog)
        self.labInfo.setObjectName(u"labInfo")

        self.gridLayout.addWidget(self.labInfo, 3, 0, 1, 1)

        self.pbnDelete = QPushButton(Dialog)
        self.pbnDelete.setObjectName(u"pbnDelete")

        self.gridLayout.addWidget(self.pbnDelete, 2, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.labSearch.setText(QCoreApplication.translate("Dialog", u"Search:", None))
        self.labSort.setText(QCoreApplication.translate("Dialog", u"Sort:", None))
        self.rbnName.setText(QCoreApplication.translate("Dialog", u"Name", None))
        self.rbnMail.setText(QCoreApplication.translate("Dialog", u"Mail", None))
        self.pbnQuit.setText(QCoreApplication.translate("Dialog", u"Quit", None))
        self.pbnImport.setText(QCoreApplication.translate("Dialog", u"Import", None))
        self.pbnAdd.setText(QCoreApplication.translate("Dialog", u"Add New", None))
        self.pbnSave.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.labInfo.setText(QCoreApplication.translate("Dialog", u"InfoText", None))
        self.pbnDelete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
    # retranslateUi

