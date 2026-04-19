# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIMainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTableView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionImport = QAction(MainWindow)
        self.actionImport.setObjectName(u"actionImport")
        self.actionExport = QAction(MainWindow)
        self.actionExport.setObjectName(u"actionExport")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")

        self.horizontalLayout_2.addWidget(self.tableView)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.labSearch = QLabel(self.centralwidget)
        self.labSearch.setObjectName(u"labSearch")
        self.labSearch.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout_2.addWidget(self.labSearch)

        self.leSearch = QLineEdit(self.centralwidget)
        self.leSearch.setObjectName(u"leSearch")
        self.leSearch.setClearButtonEnabled(False)

        self.verticalLayout_2.addWidget(self.leSearch)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labSort = QLabel(self.centralwidget)
        self.labSort.setObjectName(u"labSort")
        self.labSort.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.verticalLayout.addWidget(self.labSort)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.pbnSave = QPushButton(self.centralwidget)
        self.pbnSave.setObjectName(u"pbnSave")

        self.gridLayout.addWidget(self.pbnSave, 1, 1, 1, 1)

        self.pbnImport = QPushButton(self.centralwidget)
        self.pbnImport.setObjectName(u"pbnImport")

        self.gridLayout.addWidget(self.pbnImport, 1, 0, 1, 1)

        self.pbnQuit = QPushButton(self.centralwidget)
        self.pbnQuit.setObjectName(u"pbnQuit")

        self.gridLayout.addWidget(self.pbnQuit, 4, 1, 1, 1)

        self.labInfo = QLabel(self.centralwidget)
        self.labInfo.setObjectName(u"labInfo")

        self.gridLayout.addWidget(self.labInfo, 4, 0, 1, 1)

        self.pbnAdd = QPushButton(self.centralwidget)
        self.pbnAdd.setObjectName(u"pbnAdd")
        self.pbnAdd.setEnabled(True)

        self.gridLayout.addWidget(self.pbnAdd, 2, 1, 1, 1)

        self.pbnDelete = QPushButton(self.centralwidget)
        self.pbnDelete.setObjectName(u"pbnDelete")

        self.gridLayout.addWidget(self.pbnDelete, 2, 0, 1, 1)

        self.pbnSendMail = QPushButton(self.centralwidget)
        self.pbnSendMail.setObjectName(u"pbnSendMail")

        self.gridLayout.addWidget(self.pbnSendMail, 3, 1, 1, 1)

        self.pbnOpenMailList = QPushButton(self.centralwidget)
        self.pbnOpenMailList.setObjectName(u"pbnOpenMailList")

        self.gridLayout.addWidget(self.pbnOpenMailList, 3, 0, 1, 1)


        self.horizontalLayout.addLayout(self.gridLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_2.addLayout(self.horizontalLayout_3)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.actionExport.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.labSearch.setText(QCoreApplication.translate("MainWindow", u"Search:", None))
        self.labSort.setText(QCoreApplication.translate("MainWindow", u"Sort:", None))
        self.pbnSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pbnImport.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.pbnQuit.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.labInfo.setText(QCoreApplication.translate("MainWindow", u"InfoText", None))
        self.pbnAdd.setText(QCoreApplication.translate("MainWindow", u"Add New", None))
        self.pbnDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pbnSendMail.setText(QCoreApplication.translate("MainWindow", u"SendMails", None))
        self.pbnOpenMailList.setText(QCoreApplication.translate("MainWindow", u"View/Edit Mail List", None))
    # retranslateUi

