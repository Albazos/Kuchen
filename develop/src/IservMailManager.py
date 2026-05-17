from .IServAPI import IServAPI
import smtplib
from . import AppLogger as AL

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
            lSubject = aMailData[2] if len(aMailData) > 2 and aMailData[2] else "Kuchen reminder"

            self.mAPIconnection.send_email(lTo, lSubject, body="", html_body=lHtmlBody) # type: ignore
            return True
        except (OSError, smtplib.SMTPException, ValueError, ConnectionError) as e:
            self.mLogger.error("Send Mail", f"Error sending mail: {e}")
            return False
        finally:
            self.mPassword = None
    
