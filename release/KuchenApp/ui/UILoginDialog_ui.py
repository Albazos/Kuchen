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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(640, 420)
        Dialog.setStyleSheet(u"QDialog, QWidget {\n"
"    background: #23262d;\n"
"    color: #e8edf5;\n"
"    font-family: \"Segoe UI\";\n"
"    font-size: 10pt;\n"
"}\n"
"\n"
"QFrame#fraFormCard, QFrame#fraSummaryCard {\n"
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
"QPushButton#pbnSendMails {\n"
"    background: #2f6ea5;\n"
"    color: white;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lblWindowTitle {\n"
"    color: #7db2e3;\n"
"    font-size: 18pt;\n"
"    font-weight: 700;\n"
"}\n"
"\n"
"QLabel#lblWindowSubtitle, QLabel#lblWindowHint {\n"
"    color: #75767b;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background: #1f2329;\n"
"    color: #eef4fb;\n"
"    border: 1px solid #465263;\n"
"    border-radius: 10px;\n"
"    padding: 8px 10px;\n"
"    selection-background-color: #3e7fba;\n"
"}")
        self.layRoot = QVBoxLayout(Dialog)
        self.layRoot.setSpacing(14)
        self.layRoot.setObjectName(u"layRoot")
        self.layRoot.setContentsMargins(18, 18, 18, 18)
        self.lblWindowTitle = QLabel(Dialog)
        self.lblWindowTitle.setObjectName(u"lblWindowTitle")

        self.layRoot.addWidget(self.lblWindowTitle)

        self.lblWindowSubtitle = QLabel(Dialog)
        self.lblWindowSubtitle.setObjectName(u"lblWindowSubtitle")

        self.layRoot.addWidget(self.lblWindowSubtitle)

        self.fraSummaryCard = QFrame(Dialog)
        self.fraSummaryCard.setObjectName(u"fraSummaryCard")
        self.fraSummaryCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.laySummary = QHBoxLayout(self.fraSummaryCard)
        self.laySummary.setObjectName(u"laySummary")
        self.laySummary.setContentsMargins(14, 14, 14, 14)
        self.lblSummaryRecipients = QLabel(self.fraSummaryCard)
        self.lblSummaryRecipients.setObjectName(u"lblSummaryRecipients")

        self.laySummary.addWidget(self.lblSummaryRecipients)

        self.laySubjectRow = QHBoxLayout()
        self.laySubjectRow.setObjectName(u"laySubjectRow")
        self.lblSubject = QLabel(self.fraSummaryCard)
        self.lblSubject.setObjectName(u"lblSubject")

        self.laySubjectRow.addWidget(self.lblSubject)

        self.ledSubject = QLineEdit(self.fraSummaryCard)
        self.ledSubject.setObjectName(u"ledSubject")

        self.laySubjectRow.addWidget(self.ledSubject)


        self.laySummary.addLayout(self.laySubjectRow)


        self.layRoot.addWidget(self.fraSummaryCard)

        self.fraFormCard = QFrame(Dialog)
        self.fraFormCard.setObjectName(u"fraFormCard")
        self.fraFormCard.setFrameShape(QFrame.Shape.StyledPanel)
        self.layFormCard = QVBoxLayout(self.fraFormCard)
        self.layFormCard.setSpacing(14)
        self.layFormCard.setObjectName(u"layFormCard")
        self.layFormCard.setContentsMargins(18, 18, 18, 18)
        self.lblFormTitle = QLabel(self.fraFormCard)
        self.lblFormTitle.setObjectName(u"lblFormTitle")
        self.lblFormTitle.setStyleSheet(u"font-weight: 700; font-size: 11pt; background: transparent;")

        self.layFormCard.addWidget(self.lblFormTitle)

        self.layForm = QFormLayout()
        self.layForm.setObjectName(u"layForm")
        self.layForm.setLabelAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.layForm.setFormAlignment(Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.layForm.setHorizontalSpacing(16)
        self.layForm.setVerticalSpacing(12)
        self.lblServer = QLabel(self.fraFormCard)
        self.lblServer.setObjectName(u"lblServer")

        self.layForm.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblServer)

        self.ledServer = QLineEdit(self.fraFormCard)
        self.ledServer.setObjectName(u"ledServer")

        self.layForm.setWidget(0, QFormLayout.ItemRole.FieldRole, self.ledServer)

        self.lblUsername = QLabel(self.fraFormCard)
        self.lblUsername.setObjectName(u"lblUsername")

        self.layForm.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblUsername)

        self.ledUser = QLineEdit(self.fraFormCard)
        self.ledUser.setObjectName(u"ledUser")

        self.layForm.setWidget(1, QFormLayout.ItemRole.FieldRole, self.ledUser)

        self.lblPassword = QLabel(self.fraFormCard)
        self.lblPassword.setObjectName(u"lblPassword")

        self.layForm.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblPassword)

        self.ledPsw = QLineEdit(self.fraFormCard)
        self.ledPsw.setObjectName(u"ledPsw")
        self.ledPsw.setEchoMode(QLineEdit.EchoMode.Password)

        self.layForm.setWidget(2, QFormLayout.ItemRole.FieldRole, self.ledPsw)


        self.layFormCard.addLayout(self.layForm)

        self.layButtons = QHBoxLayout()
        self.layButtons.setObjectName(u"layButtons")
        self.spcButtons = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layButtons.addItem(self.spcButtons)

        self.pbnCancel = QPushButton(self.fraFormCard)
        self.pbnCancel.setObjectName(u"pbnCancel")

        self.layButtons.addWidget(self.pbnCancel)

        self.pbnSendMails = QPushButton(self.fraFormCard)
        self.pbnSendMails.setObjectName(u"pbnSendMails")

        self.layButtons.addWidget(self.pbnSendMails)


        self.layFormCard.addLayout(self.layButtons)


        self.layRoot.addWidget(self.fraFormCard)

        self.lblWindowHint = QLabel(Dialog)
        self.lblWindowHint.setObjectName(u"lblWindowHint")

        self.layRoot.addWidget(self.lblWindowHint)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Send mails", None))
        self.lblWindowTitle.setText(QCoreApplication.translate("Dialog", u"Confirm and send", None))
        self.lblWindowSubtitle.setText(QCoreApplication.translate("Dialog", u"Review the target server and enter your credentials to send the prepared reminder mail.", None))
        self.lblSummaryRecipients.setText(QCoreApplication.translate("Dialog", u"Recipients: 0", None))
        self.lblSubject.setText(QCoreApplication.translate("Dialog", u"Subject", None))
        self.ledSubject.setText(QCoreApplication.translate("Dialog", u"Kuchen reminder", None))
        self.lblFormTitle.setText(QCoreApplication.translate("Dialog", u"Mail account", None))
        self.lblServer.setText(QCoreApplication.translate("Dialog", u"Server", None))
        self.ledServer.setPlaceholderText(QCoreApplication.translate("Dialog", u"example.edu", None))
        self.lblUsername.setText(QCoreApplication.translate("Dialog", u"Username", None))
        self.ledUser.setPlaceholderText(QCoreApplication.translate("Dialog", u"your username", None))
        self.lblPassword.setText(QCoreApplication.translate("Dialog", u"Password", None))
        self.ledPsw.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022", None))
        self.pbnCancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.pbnSendMails.setText(QCoreApplication.translate("Dialog", u"Send mails", None))
        self.lblWindowHint.setText(QCoreApplication.translate("Dialog", u"The account details are only used for this send action and should stay easy to review.", None))
    # retranslateUi

