import sys
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog, QMessageBox
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

import IservMailManager as ISM
from UILoginDialog_ui import Ui_Dialog

class CLoginDialog(QDialog, Ui_Dialog):
    
    mSendState = False
    mMailData = None
    
    def __init__(self,aMailData):
       super().__init__()
       self.setupUi(self)
       self.mMailData = aMailData
       
       self.pbnCancel.clicked.connect(self.CancelButton)
       self.pbnLogin.clicked.connect(self.SendMails)
    
    def SendMails(self):
        lLoginData = []
        lLoginData.append(self.ledUser.text())
        lLoginData.append(self.ledPsw.text())
       
        self.mISMM = ISM.IservMailManager(lLoginData[0],lLoginData[1],"wvss.de")
        if self.mISMM.sendMail(self.mMailData) == True:
            self.mSendState = True
            self.close()
            
    def CancelButton(self):
        self.close()
    
    def getSendState(self):
        return self.mSendState
    
