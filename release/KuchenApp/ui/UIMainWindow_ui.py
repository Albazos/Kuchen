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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QTableView, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 820)
        MainWindow.setStyleSheet(u"QMainWindow, QWidget {\n"
"    background: #23262d;\n"
"    color: #e8edf5;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QFrame#fraSidebar {\n"
"    background: #1b2430;\n"
"    border-radius: 18px;\n"
"}\n"
"\n"
"QFrame#fraClassCard {\n"
"    background: #26364a;\n"
"    border-radius: 14px;\n"
"}\n"
"\n"
"QFrame#fraToolbarCard, QFrame#fraTableCard {\n"
"    background: #2b3038;\n"
"    border: 1px solid #3b4452;\n"
"    border-radius: 16px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    background: #394352;\n"
"    color: #eef4fb;\n"
"    padding: 10px 14px;\n"
"}\n"
"\n"
"QPushButton#pbnAddEntry {\n"
"    background: #2f6ea5;\n"
"    color: white;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QPushButton#pbnSendMail {\n"
"    background: #3e7fba;\n"
"    color: white;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QPushButton#pbnOpenMailList, QPushButton#pbnImport, QPushButton#pbnSave, QPushButton#pbnChangeClass {\n"
"    background: #26364a;\n"
" "
                        "   color: white;\n"
"}\n"
"\n"
"QLineEdit, QComboBox {\n"
"    background: #1f2329;\n"
"    color: #eef4fb;\n"
"    border: 1px solid #465263;\n"
"    border-radius: 10px;\n"
"    padding: 8px 10px;\n"
"    selection-background-color: #3e7fba;\n"
"}\n"
"\n"
"QLabel#lblWindowTitle {\n"
"    color: #7db2e3;\n"
"    font-size: 20pt;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lblSidebarTitle {\n"
"    color: white;\n"
"    font-size: 22pt;\n"
"    font-weight: 700;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lblWindowSubtitle, QLabel#lblTableHint, QLabel#lblTableMeta {\n"
"    color: #97a3b6;\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lblSidebarSubtitle, QLabel#lblSidebarSectionSort {\n"
"    color: rgba(255,255,255,180);\n"
"    background: transparent;\n"
"}\n"
"\n"
"QLabel#lblSidebarActiveClassCaption, QLabel#lblActiveClassName, QLabel#lblTableTitle {\n"
"    background: transparent;\n"
"}\n"
"\n"
"QTableView {\n"
"    background: #2f343d;\n"
"    alt"
                        "ernate-background-color: #313741;\n"
"    border: none;\n"
"    color: #e8edf5;\n"
"    gridline-color: #404958;\n"
"    selection-background-color: #355f8c;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: #353c48;\n"
"    color: #f2f6fb;\n"
"    border: none;\n"
"    padding: 8px;\n"
"    font-weight: 700;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layRoot = QHBoxLayout(self.centralwidget)
        self.layRoot.setSpacing(18)
        self.layRoot.setObjectName(u"layRoot")
        self.layRoot.setContentsMargins(18, 18, 18, 18)
        self.fraSidebar = QFrame(self.centralwidget)
        self.fraSidebar.setObjectName(u"fraSidebar")
        self.fraSidebar.setMinimumSize(QSize(260, 0))
        self.fraSidebar.setMaximumSize(QSize(300, 16777215))
        self.fraSidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.laySidebar = QVBoxLayout(self.fraSidebar)
        self.laySidebar.setSpacing(14)
        self.laySidebar.setObjectName(u"laySidebar")
        self.laySidebar.setContentsMargins(18, 22, 18, 18)
        self.lblSidebarTitle = QLabel(self.fraSidebar)
        self.lblSidebarTitle.setObjectName(u"lblSidebarTitle")

        self.laySidebar.addWidget(self.lblSidebarTitle)

        self.lblSidebarSubtitle = QLabel(self.fraSidebar)
        self.lblSidebarSubtitle.setObjectName(u"lblSidebarSubtitle")
        self.lblSidebarSubtitle.setWordWrap(True)

        self.laySidebar.addWidget(self.lblSidebarSubtitle)

        self.fraClassCard = QFrame(self.fraSidebar)
        self.fraClassCard.setObjectName(u"fraClassCard")
        self.fraClassCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.layClassCard = QVBoxLayout(self.fraClassCard)
        self.layClassCard.setObjectName(u"layClassCard")
        self.layClassCard.setContentsMargins(14, 12, 14, 12)
        self.lblSidebarActiveClassCaption = QLabel(self.fraClassCard)
        self.lblSidebarActiveClassCaption.setObjectName(u"lblSidebarActiveClassCaption")
        self.lblSidebarActiveClassCaption.setStyleSheet(u"color: rgba(255,255,255,180); background: transparent;")

        self.layClassCard.addWidget(self.lblSidebarActiveClassCaption)

        self.lblActiveClassName = QLabel(self.fraClassCard)
        self.lblActiveClassName.setObjectName(u"lblActiveClassName")
        self.lblActiveClassName.setStyleSheet(u"color: white; font-size: 18pt; font-weight: 700; background: transparent;")

        self.layClassCard.addWidget(self.lblActiveClassName)


        self.laySidebar.addWidget(self.fraClassCard)

        self.pbnSendMail = QPushButton(self.fraSidebar)
        self.pbnSendMail.setObjectName(u"pbnSendMail")

        self.laySidebar.addWidget(self.pbnSendMail)

        self.pbnOpenMailList = QPushButton(self.fraSidebar)
        self.pbnOpenMailList.setObjectName(u"pbnOpenMailList")

        self.laySidebar.addWidget(self.pbnOpenMailList)

        self.pbnImport = QPushButton(self.fraSidebar)
        self.pbnImport.setObjectName(u"pbnImport")

        self.laySidebar.addWidget(self.pbnImport)

        self.pbnSave = QPushButton(self.fraSidebar)
        self.pbnSave.setObjectName(u"pbnSave")

        self.laySidebar.addWidget(self.pbnSave)

        self.pbnChangeClass = QPushButton(self.fraSidebar)
        self.pbnChangeClass.setObjectName(u"pbnChangeClass")

        self.laySidebar.addWidget(self.pbnChangeClass)

        self.spcSidebarTop = QSpacerItem(20, 30, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.laySidebar.addItem(self.spcSidebarTop)

        self.lblSidebarSectionSort = QLabel(self.fraSidebar)
        self.lblSidebarSectionSort.setObjectName(u"lblSidebarSectionSort")

        self.laySidebar.addWidget(self.lblSidebarSectionSort)

        self.cmbSortField = QComboBox(self.fraSidebar)
        self.cmbSortField.setObjectName(u"cmbSortField")

        self.laySidebar.addWidget(self.cmbSortField)

        self.cmbSortDirection = QComboBox(self.fraSidebar)
        self.cmbSortDirection.addItem("")
        self.cmbSortDirection.addItem("")
        self.cmbSortDirection.setObjectName(u"cmbSortDirection")

        self.laySidebar.addWidget(self.cmbSortDirection)

        self.spcSidebarBottom = QSpacerItem(20, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.laySidebar.addItem(self.spcSidebarBottom)


        self.layRoot.addWidget(self.fraSidebar)

        self.layContent = QVBoxLayout()
        self.layContent.setSpacing(14)
        self.layContent.setObjectName(u"layContent")
        self.lblWindowTitle = QLabel(self.centralwidget)
        self.lblWindowTitle.setObjectName(u"lblWindowTitle")

        self.layContent.addWidget(self.lblWindowTitle)

        self.lblWindowSubtitle = QLabel(self.centralwidget)
        self.lblWindowSubtitle.setObjectName(u"lblWindowSubtitle")

        self.layContent.addWidget(self.lblWindowSubtitle)

        self.fraToolbarCard = QFrame(self.centralwidget)
        self.fraToolbarCard.setObjectName(u"fraToolbarCard")
        self.fraToolbarCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.layToolbar = QHBoxLayout(self.fraToolbarCard)
        self.layToolbar.setSpacing(12)
        self.layToolbar.setObjectName(u"layToolbar")
        self.layToolbar.setContentsMargins(14, 14, 14, 14)
        self.ledSearch = QLineEdit(self.fraToolbarCard)
        self.ledSearch.setObjectName(u"ledSearch")

        self.layToolbar.addWidget(self.ledSearch)

        self.pbnDelete = QPushButton(self.fraToolbarCard)
        self.pbnDelete.setObjectName(u"pbnDelete")

        self.layToolbar.addWidget(self.pbnDelete)

        self.pbnImportToolbar = QPushButton(self.fraToolbarCard)
        self.pbnImportToolbar.setObjectName(u"pbnImportToolbar")

        self.layToolbar.addWidget(self.pbnImportToolbar)

        self.pbnSaveToolbar = QPushButton(self.fraToolbarCard)
        self.pbnSaveToolbar.setObjectName(u"pbnSaveToolbar")

        self.layToolbar.addWidget(self.pbnSaveToolbar)

        self.pbnAddColumn = QPushButton(self.fraToolbarCard)
        self.pbnAddColumn.setObjectName(u"pbnAddColumn")

        self.layToolbar.addWidget(self.pbnAddColumn)

        self.pbnAddEntry = QPushButton(self.fraToolbarCard)
        self.pbnAddEntry.setObjectName(u"pbnAddEntry")

        self.layToolbar.addWidget(self.pbnAddEntry)


        self.layContent.addWidget(self.fraToolbarCard)

        self.fraTableCard = QFrame(self.centralwidget)
        self.fraTableCard.setObjectName(u"fraTableCard")
        self.fraTableCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.layTableCard = QVBoxLayout(self.fraTableCard)
        self.layTableCard.setSpacing(12)
        self.layTableCard.setObjectName(u"layTableCard")
        self.layTableCard.setContentsMargins(14, 14, 14, 14)
        self.layTableMeta = QHBoxLayout()
        self.layTableMeta.setObjectName(u"layTableMeta")
        self.lblTableTitle = QLabel(self.fraTableCard)
        self.lblTableTitle.setObjectName(u"lblTableTitle")
        self.lblTableTitle.setStyleSheet(u"font-weight: 700; font-size: 11pt; background: transparent;")

        self.layTableMeta.addWidget(self.lblTableTitle)

        self.spcTableMeta = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layTableMeta.addItem(self.spcTableMeta)

        self.lblTableMeta = QLabel(self.fraTableCard)
        self.lblTableMeta.setObjectName(u"lblTableMeta")

        self.layTableMeta.addWidget(self.lblTableMeta)


        self.layTableCard.addLayout(self.layTableMeta)

        self.tbvCakeList = QTableView(self.fraTableCard)
        self.tbvCakeList.setObjectName(u"tbvCakeList")

        self.layTableCard.addWidget(self.tbvCakeList)

        self.lblTableHint = QLabel(self.fraTableCard)
        self.lblTableHint.setObjectName(u"lblTableHint")

        self.layTableCard.addWidget(self.lblTableHint)


        self.layContent.addWidget(self.fraTableCard)

        self.layBottomBar = QHBoxLayout()
        self.layBottomBar.setObjectName(u"layBottomBar")
        self.spcBottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layBottomBar.addItem(self.spcBottom)

        self.pbnQuit = QPushButton(self.centralwidget)
        self.pbnQuit.setObjectName(u"pbnQuit")

        self.layBottomBar.addWidget(self.pbnQuit)


        self.layContent.addLayout(self.layBottomBar)


        self.layRoot.addLayout(self.layContent)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Kuchen", None))
        self.lblSidebarTitle.setText(QCoreApplication.translate("MainWindow", u"Kuchen", None))
        self.lblSidebarSubtitle.setText(QCoreApplication.translate("MainWindow", u"Cake management for classes", None))
        self.lblSidebarActiveClassCaption.setText(QCoreApplication.translate("MainWindow", u"ACTIVE CLASS", None))
        self.lblActiveClassName.setText(QCoreApplication.translate("MainWindow", u"EITB23A", None))
        self.pbnSendMail.setText(QCoreApplication.translate("MainWindow", u"Send mails", None))
        self.pbnOpenMailList.setText(QCoreApplication.translate("MainWindow", u"Open mail list", None))
        self.pbnImport.setText(QCoreApplication.translate("MainWindow", u"Import CSV", None))
        self.pbnSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pbnChangeClass.setText(QCoreApplication.translate("MainWindow", u"Change class", None))
        self.lblSidebarSectionSort.setText(QCoreApplication.translate("MainWindow", u"SORTING", None))
        self.cmbSortDirection.setItemText(0, QCoreApplication.translate("MainWindow", u"Ascending", None))
        self.cmbSortDirection.setItemText(1, QCoreApplication.translate("MainWindow", u"Descending", None))

        self.lblWindowTitle.setText(QCoreApplication.translate("MainWindow", u"Manage entries", None))
        self.lblWindowSubtitle.setText(QCoreApplication.translate("MainWindow", u"Edit the list directly in the table and send reminders afterwards.", None))
        self.ledSearch.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Search", None))
        self.pbnDelete.setText(QCoreApplication.translate("MainWindow", u"Delete", None))
        self.pbnImportToolbar.setText(QCoreApplication.translate("MainWindow", u"Import", None))
        self.pbnSaveToolbar.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.pbnAddColumn.setText(QCoreApplication.translate("MainWindow", u"+ Add column", None))
        self.pbnAddEntry.setText(QCoreApplication.translate("MainWindow", u"+ New entry", None))
        self.lblTableTitle.setText(QCoreApplication.translate("MainWindow", u"Cake list", None))
        self.lblTableMeta.setText(QCoreApplication.translate("MainWindow", u"0 entries", None))
        self.lblTableHint.setText(QCoreApplication.translate("MainWindow", u"Double-click to edit directly. Add a column to rebuild the table with more fields.", None))
        self.pbnQuit.setText(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi

