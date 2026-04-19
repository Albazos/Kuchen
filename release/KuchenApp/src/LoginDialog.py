from PySide6.QtWidgets import QDialog

from . import IservMailManager as ISM
from . import SettingsManager as SM
from ui.UILoginDialog_ui import Ui_Dialog

class CLoginDialog(QDialog, Ui_Dialog):
    
    def __init__(self,aMailData):
       super().__init__()
       self.setupUi(self)
       self.mSendState = None  # None=cancelled, True=sent, False=failed
       self.mMailData = aMailData
       self.mSettings = SM.SettingsManager()
       
       self.ledServer.setText(self.mSettings.getIServDomain())
       
       self.pbnCancel.clicked.connect(self.CancelButton)
       self.pbnLogin.clicked.connect(self.SendMails)
    
    def SendMails(self):
        lUser = self.ledUser.text()
        lPsw = self.ledPsw.text()
        lServer = self.ledServer.text().strip()
        
        if lServer:
            self.mSettings.setIServDomain(lServer)
            self.mSettings.save()
       
        self.mISMM = ISM.IservMailManager(lUser, lPsw, lServer)
        if self.mISMM.sendMail(self.mMailData):
            self.mSendState = True
            self.close()
        else:
            self.mSendState = False
            
    def CancelButton(self):
        self.close()
    
    def getSendState(self):
        return self.mSendState
    
