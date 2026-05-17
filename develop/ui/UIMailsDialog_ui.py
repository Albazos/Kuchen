# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UIMailsDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QTableView,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1180, 760)
        Dialog.setStyleSheet(u"QDialog, QWidget {\n"
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
"QPushButton#pbnAddRecipient {\n"
"    background: #2f6ea5;\n"
"    color: white;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QPushButton#pbnSaveRecipientList {\n"
"    background: #3e7fba;\n"
"    color: white;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QPushButton#pbnImport, QPushButton#pbnSave {\n"
"    background: #26364a;\n"
"    color: white;\n"
"}\n"
"\n"
"QLabel#lblWindowTitle {\n"
"    color: #7db2e3;\n"
"    font-size: 18pt;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
""
                        "QLabel#lblSidebarTitle {\n"
"    color: white;\n"
"    font-size: 20pt;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lblSidebarSubtitle, QLabel#lblWindowSubtitle, QLabel#lblTableMeta, QLabel#lblTableHint {\n"
"    color: #75767b;\n"
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
"QTableView {\n"
"    background: transparent;\n"
"    border: none;\n"
"    color: #e8edf5;\n"
"    gridline-color: #3b4452;\n"
"    selection-background-color: #2f6ea5;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background: #313844;\n"
"    color: #eef4fb;\n"
"    border: none;\n"
"    padding: 8px;\n"
"    font-weight: 700;\n"
"}")
        self.layRoot = QHBoxLayout(Dialog)
        self.layRoot.setSpacing(18)
        self.layRoot.setObjectName(u"layRoot")
        self.layRoot.setContentsMargins(18, 18, 18, 18)
        self.fraSidebar = QFrame(Dialog)
        self.fraSidebar.setObjectName(u"fraSidebar")
        self.fraSidebar.setMinimumSize(QSize(250, 0))
        self.fraSidebar.setMaximumSize(QSize(290, 16777215))
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
        self.lblSidebarSubtitle.setStyleSheet(u"color: rgba(255,255,255,180); background: transparent;")
        self.lblSidebarSubtitle.setWordWrap(True)

        self.laySidebar.addWidget(self.lblSidebarSubtitle)

        self.pbnSaveRecipientList = QPushButton(self.fraSidebar)
        self.pbnSaveRecipientList.setObjectName(u"pbnSaveRecipientList")

        self.laySidebar.addWidget(self.pbnSaveRecipientList)

        self.pbnImport = QPushButton(self.fraSidebar)
        self.pbnImport.setObjectName(u"pbnImport")

        self.laySidebar.addWidget(self.pbnImport)

        self.pbnSave = QPushButton(self.fraSidebar)
        self.pbnSave.setObjectName(u"pbnSave")

        self.laySidebar.addWidget(self.pbnSave)

        self.spcSidebar = QSpacerItem(20, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.laySidebar.addItem(self.spcSidebar)

        self.lblSidebarSectionSort = QLabel(self.fraSidebar)
        self.lblSidebarSectionSort.setObjectName(u"lblSidebarSectionSort")
        self.lblSidebarSectionSort.setStyleSheet(u"color: rgba(255,255,255,180); background: transparent;")

        self.laySidebar.addWidget(self.lblSidebarSectionSort)

        self.cmbSortField = QComboBox(self.fraSidebar)
        self.cmbSortField.setObjectName(u"cmbSortField")

        self.laySidebar.addWidget(self.cmbSortField)

        self.cmbSortDirection = QComboBox(self.fraSidebar)
        self.cmbSortDirection.addItem("")
        self.cmbSortDirection.addItem("")
        self.cmbSortDirection.setObjectName(u"cmbSortDirection")

        self.laySidebar.addWidget(self.cmbSortDirection)


        self.layRoot.addWidget(self.fraSidebar)

        self.layContent = QVBoxLayout()
        self.layContent.setSpacing(14)
        self.layContent.setObjectName(u"layContent")
        self.lblWindowTitle = QLabel(Dialog)
        self.lblWindowTitle.setObjectName(u"lblWindowTitle")

        self.layContent.addWidget(self.lblWindowTitle)

        self.lblWindowSubtitle = QLabel(Dialog)
        self.lblWindowSubtitle.setObjectName(u"lblWindowSubtitle")

        self.layContent.addWidget(self.lblWindowSubtitle)

        self.fraToolbarCard = QFrame(Dialog)
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

        self.pbnAddColumn = QPushButton(self.fraToolbarCard)
        self.pbnAddColumn.setObjectName(u"pbnAddColumn")

        self.layToolbar.addWidget(self.pbnAddColumn)

        self.pbnAddRecipient = QPushButton(self.fraToolbarCard)
        self.pbnAddRecipient.setObjectName(u"pbnAddRecipient")

        self.layToolbar.addWidget(self.pbnAddRecipient)


        self.layContent.addWidget(self.fraToolbarCard)

        self.fraTableCard = QFrame(Dialog)
        self.fraTableCard.setObjectName(u"fraTableCard")
        self.fraTableCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.layTableCard = QVBoxLayout(self.fraTableCard)
        self.layTableCard.setSpacing(12)
        self.layTableCard.setObjectName(u"layTableCard")
        self.layTableCard.setContentsMargins(14, 14, 14, 14)
        self.layMeta = QHBoxLayout()
        self.layMeta.setObjectName(u"layMeta")
        self.lblTableTitle = QLabel(self.fraTableCard)
        self.lblTableTitle.setObjectName(u"lblTableTitle")
        self.lblTableTitle.setStyleSheet(u"font-weight: 700; font-size: 11pt; background: transparent;")

        self.layMeta.addWidget(self.lblTableTitle)

        self.spcMeta = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layMeta.addItem(self.spcMeta)

        self.lblTableMeta = QLabel(self.fraTableCard)
        self.lblTableMeta.setObjectName(u"lblTableMeta")

        self.layMeta.addWidget(self.lblTableMeta)


        self.layTableCard.addLayout(self.layMeta)

        self.tbvMailList = QTableView(self.fraTableCard)
        self.tbvMailList.setObjectName(u"tbvMailList")

        self.layTableCard.addWidget(self.tbvMailList)

        self.lblTableHint = QLabel(self.fraTableCard)
        self.lblTableHint.setObjectName(u"lblTableHint")

        self.layTableCard.addWidget(self.lblTableHint)


        self.layContent.addWidget(self.fraTableCard)

        self.layBottomBar = QHBoxLayout()
        self.layBottomBar.setObjectName(u"layBottomBar")
        self.spcBottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layBottomBar.addItem(self.spcBottom)

        self.pbnQuit = QPushButton(Dialog)
        self.pbnQuit.setObjectName(u"pbnQuit")

        self.layBottomBar.addWidget(self.pbnQuit)


        self.layContent.addLayout(self.layBottomBar)


        self.layRoot.addLayout(self.layContent)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Mail list", None))
        self.lblSidebarTitle.setText(QCoreApplication.translate("Dialog", u"Mail list", None))
        self.lblSidebarSubtitle.setText(QCoreApplication.translate("Dialog", u"Manage recipients and mail-related columns in the same visual system.", None))
        self.pbnSaveRecipientList.setText(QCoreApplication.translate("Dialog", u"Save recipient list", None))
        self.pbnImport.setText(QCoreApplication.translate("Dialog", u"Import CSV", None))
        self.pbnSave.setText(QCoreApplication.translate("Dialog", u"Save", None))
        self.lblSidebarSectionSort.setText(QCoreApplication.translate("Dialog", u"SORTING", None))
        self.cmbSortDirection.setItemText(0, QCoreApplication.translate("Dialog", u"Ascending", None))
        self.cmbSortDirection.setItemText(1, QCoreApplication.translate("Dialog", u"Descending", None))

        self.lblWindowTitle.setText(QCoreApplication.translate("Dialog", u"Manage recipient list", None))
        self.lblWindowSubtitle.setText(QCoreApplication.translate("Dialog", u"Edit recipient data, add columns if needed, and keep the structure aligned with your mail workflow.", None))
        self.ledSearch.setPlaceholderText(QCoreApplication.translate("Dialog", u"Search by name, mail or custom column", None))
        self.pbnDelete.setText(QCoreApplication.translate("Dialog", u"Delete", None))
        self.pbnAddColumn.setText(QCoreApplication.translate("Dialog", u"+ Add column", None))
        self.pbnAddRecipient.setText(QCoreApplication.translate("Dialog", u"+ New recipient", None))
        self.lblTableTitle.setText(QCoreApplication.translate("Dialog", u"Recipient table", None))
        self.lblTableMeta.setText(QCoreApplication.translate("Dialog", u"0 recipients", None))
        self.lblTableHint.setText(QCoreApplication.translate("Dialog", u"Double-click to edit directly. Add a column to rebuild the recipient structure.", None))
        self.pbnQuit.setText(QCoreApplication.translate("Dialog", u"Close", None))
    # retranslateUi

