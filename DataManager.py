#works with the Data and holds it
import csv

class DataManger():
    mData = []
    mMailData = []
    mCompleteMailData = []
    
    mSortedMailData = []
    mSortedData = []  
    
    mSortedMailColumnIndex = None
    mSortedColumnIndex = None 
    
    def setSortedData(self, aData):
        self.mSortedData = aData
    
    def getSortedData(self):
        return self.mSortedData

    def setData(self, aData):
        self.mData = aData
    
    def getData(self):
        return self.mData
    
    def setSortedColumnIndex(self, aData, aForMain=True):
        if aForMain:
            self.mSortedColumnIndex = aData
        else:
            self.mSortedMailColumnIndex = aData
            
    def getSortedColumnIndex(self, aForMain=True ):
        if aForMain:
            return self.mSortedColumnIndex
        else:
            return self.mSortedMailColumnIndex 
        
    
    def setSortedMailData(self, aData):
        self.mSortedMailData = aData
    
    def getSortedMailData(self):
        return self.mSortedMailData

    def setMailData(self, aData):
        self.mMailData = aData
    
    def getMailData(self):
        return self.mMailData
    
    def getCompleteMailData(self):
        return self.mCompleteMailData
    
    def setCompleteMailData(self, aData):
        self.mCompleteMailData = aData
    
    def setSortedMailColumnIndex(self, aData):
        self.mSortedMailColumnIndex = aData
    
    def getSortedMailColumnIndex(self):
        return self.mSortedMailColumnIndex
    
    def LoadStandartFile(self, aForMainTable = True):
        if aForMainTable:
            lFilePath = "./Kuchen/Data/CakeData.csv"
        else: 
            lFilePath = "./Kuchen/Data/Klassen/EITB23A.csv"
        if lFilePath:
            with open(lFilePath, newline='') as csvfile:
                lDialect = csv.Sniffer().sniff(csvfile.readline())
                csvfile.seek(0)
                lReader = csv.reader(csvfile, dialect=lDialect)
                if aForMainTable:
                    self.setData(list(lReader))              
                    self.mHeaders = self.getData()[0]
                    del self.getData()[0]
                else:
                    self.setMailData(list(lReader))              
                    self.mHeaders = self.getMailData()[0]
                    del self.getMailData()[0]
            if aForMainTable:            
                self.setSortedData(self.getData())
            else:
                self.setSortedMailData(self.getMailData())
            csvfile.close()
            return True  
        else:
            return False
    
    def sortData(self, aSortColumnIndex, aForMain = True):
            if aForMain:
                lSData = self.getSortedData()
            else:
                lSData = self.getSortedMailData()
            if len(lSData) > 1:
                lSData.sort(key=lambda x: x[aSortColumnIndex])
            if aForMain:
                self.setSortedData(lSData) 
            else:
                self.setSortedMailData(lSData)
    
    def SaveFile(self, aForMainTable = True):
        if aForMainTable:
            lFilePath = "./Kuchen/Data/CakeData.csv"
        else: 
            lFilePath = "./Kuchen/Data/Klassen/EITB23A.csv"
        if lFilePath:
            with open(lFilePath, 'w', newline='') as csvfile:
                lWriter = csv.writer(csvfile, delimiter=',')
                lWriter.writerow(self.mHeaders)
                if aForMainTable:
                    lWriter.writerows(self.getData())
                else:
                    lWriter.writerows(self.getSortedMailData())
                csvfile.close()
            return True       
        else:
            return False
        
    def ImportFile(self, aPath, aForMainTable = True):
         with open(aPath, newline='') as csvfile:
                    lDialect = csv.Sniffer().sniff(csvfile.readline())
                    csvfile.seek(0)
                    lReader = csv.reader(csvfile, dialect=lDialect)
                    if aForMainTable:
                        self.setData(list(lReader))          
                        self.mHeaders = self.getData()[0]
                        del self.getData()[0]
                        self.setSortedData(self.getData())
                    else:
                        self.setMailData(list(lReader))          
                        self.mHeaders = self.getMailData()[0]
                        del self.getMailData()[0]
                        self.setSortedMailData(self.getMailData())
                    csvfile.close() 
    
    
    def createCompleteMailData(self):
        lCompleteMailData = []
        lMails = []
        for lMail in self.mMailData:
            lMails.append(lMail[1])
        lCompleteMailData.append(lMails)
        lHeaders = ["Name", "CakeCount","Hanuta","Waffel", "Date"]
        lHtmlBody = self.createHtmlDataString(aHeaders=lHeaders)
        lCompleteMailData.append(lHtmlBody)
        self.setCompleteMailData(lCompleteMailData)
        return lCompleteMailData
    
    def createHtmlDataString(self, aHeaders = None):
        table_style = "width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;"
        th_style = "background-color: #f2f2f2; color: #333; font-weight: bold; padding: 12px; border: 1px solid #dddddd; text-align: left;"
        td_style = "padding: 8px; border: 1px solid #dddddd; text-align: left;"
        tr_even_style = "background-color: #f9f9f9;"

        html = f'<table style="{table_style}">\n'

        if aHeaders:
            html += "  <thead>\n    <tr>\n"
            for header in aHeaders:
                html += f'      <th style="{th_style}">{header}</th>\n'
            html += "    </tr>\n  </thead>\n"

        html += "  <tbody>\n"
        for i, row in enumerate(self.mData):
            style = tr_even_style if i % 2 == 0 else ""
            html += f'    <tr style="{style}">\n'
            for item in row:
                html += f'      <td style="{td_style}">{item}</td>\n'
            html += "    </tr>\n"

        html += "  </tbody>\n</table>"

        return html