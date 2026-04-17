from PySide6.QtWidgets import QDialog

import IservMailManager as ISM
import SettingsManager as SM
from UILoginDialog_ui import Ui_Dialog

class CLoginDialog(QDialog, Ui_Dialog):
    
    def __init__(self,aMailData):
       super().__init__()
       self.setupUi(self)
       self.mSendState = None  # None=cancelled, True=sent, False=failed
       self.mMailData = aMailData
       
       self.pbnCancel.clicked.connect(self.CancelButton)
       self.pbnLogin.clicked.connect(self.SendMails)
    
    def SendMails(self):
        lLoginData = []
        lLoginData.append(self.ledUser.text())
        lLoginData.append(self.ledPsw.text())
       
        lSettings = SM.SettingsManager()
        self.mISMM = ISM.IservMailManager(lLoginData[0],lLoginData[1],lSettings.getIServDomain())
        if self.mISMM.sendMail(self.mMailData):
            self.mSendState = True
            self.close()
        else:
            self.mSendState = False
            
    def CancelButton(self):
        self.close()
    
    def getSendState(self):
        return self.mSendState
    
