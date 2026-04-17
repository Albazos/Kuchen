from src.IServAPIEdited_standalone import IServAPI
from src import AppLogger as AL

class IservMailManager:
    
    def __init__(self, aUsername, aPassword, aURL):
        self.mUsername = aUsername
        self.mPassword = aPassword
        self.mURL = aURL
        self.mAPIconnection = IServAPI(self.mUsername,self.mPassword,self.mURL)
        self.mLogger = AL.AppLogger()
        

    def sendMail(self, aMailData):
        try:
            lFrom = self.mUsername + "@" + self.mURL
            #aMailData[0].remove(lFrom)
            lTo = aMailData[0]
            lHtmlBody = aMailData[1]

            self.mAPIconnection.send_email(lTo,"Kuchenreminder",body="", html_body=lHtmlBody) # type: ignore
            return True
        except Exception as e:
            self.mLogger.error("Send Mail", f"Error sending mail: {e}")
            return False
    