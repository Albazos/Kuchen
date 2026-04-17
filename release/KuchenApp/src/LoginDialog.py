from PySide6.QtWidgets import QDialog

from src import IservMailManager as ISM
from src import SettingsManager as SM
from ui.UILoginDialog_ui import Ui_Dialog

class CLoginDialog(QDialog, Ui_Dialog):
    
    def __init__(self,aMailData):
       super().__init__()
       self.setupUi(self)
       self.mSendState = False
       self.mMailData = aMailData
       
       self.pbnCancel.clicked.connect(self.CancelButton)
       self.pbnLogin.clicked.connect(self.SendMails)
    
    def SendMails(self):
        lLoginData = []
        lLoginData.append(self.ledUser.text())
        lLoginData.append(self.ledPsw.text())
       
        lSettings = SM.SettingsManager()
        self.mISMM = ISM.IservMailManager(lLoginData[0],lLoginData[1],lSettings.getIServDomain())
        if self.mISMM.sendMail(self.mMailData) == True:
            self.mSendState = True
            self.close()
            
    def CancelButton(self):
        self.close()
    
    def getSendState(self):
        return self.mSendState
    
