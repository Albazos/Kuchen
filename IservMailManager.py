from IServAPIEdited import IServAPI

class IservMailManager:
    mUsername = None
    mPassword = None
    mURL = None
    mAPIconnection = None
    
    def __init__(self, aUsername, aPassword, aURL):
        self.mUsername = aUsername
        self.mPassword = aPassword
        self.mURL = aURL
        self.mAPIconnection = IServAPI(self.mUsername,self.mPassword,self.mURL)
        

    def sendMail(self, aMailData):
        
        lFrom = self.mUsername + "@wvss.de" # type: ignore #to remove from list
        #aMailData[0].remove(lFrom)
        lTo = aMailData[0]
        lHtmlBody = aMailData[1]

        self.mAPIconnection.send_email(lTo,"Kuchenreminder",body="", html_body=lHtmlBody) # type: ignore
        return True
    