#works with the Data and holds it
import csv
import os
import html
import SettingsManager as SM
import AppLogger as AL

class DataManager():
    
    def __init__(self):
        self.mData = []
        self.mMailData = []
        self.mCompleteMailData = []
        self.mSortedMailData = []
        self.mSortedData = []
        self.mSortedMailColumnIndex = None
        self.mSortedColumnIndex = None
        self.mMainHeaders = []
        self.mMailHeaders = []
        self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self.mSettings = SM.SettingsManager()
        self.mLogger = AL.AppLogger()
    
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
    
    def LoadStandardFile(self, aForMainTable=True):
        if aForMainTable:
            lCakeDatei = self.mSettings.getCakeDataDateiname()
            lFilePath = os.path.join(self._base_dir, "Data", lCakeDatei)
        else: 
            lKlassenDatei = self.mSettings.getKlassenDateiname()
            lFilePath = os.path.join(self._base_dir, "Data", "Klassen", lKlassenDatei)
        try:
            with open(lFilePath, newline='') as csvfile:
                lSample = csvfile.read(4096)
                csvfile.seek(0)
                lDialect = csv.Sniffer().sniff(lSample)
                lReader = csv.reader(csvfile, dialect=lDialect)
                if aForMainTable:
                    self.setData(list(lReader))              
                    self.mMainHeaders = self.getData()[0]
                    del self.getData()[0]
                    self._padRows(self.getData(), len(self.mMainHeaders))
                else:
                    self.setMailData(list(lReader))              
                    self.mMailHeaders = self.getMailData()[0]
                    del self.getMailData()[0]
                    self._padRows(self.getMailData(), len(self.mMailHeaders))
            if aForMainTable:            
                self.setSortedData([row[:] for row in self.getData()])
            else:
                self.setSortedMailData([row[:] for row in self.getMailData()])
            return True  
        except (OSError, csv.Error) as e:
            self.mLogger.error("Load File", f"Error loading file: {e}")
            return False
    
    def _padRows(self, aData, aHeaderLen):
        for lRow in aData:
            while len(lRow) < aHeaderLen:
                lRow.append("")
    
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
            lCakeDatei = self.mSettings.getCakeDataDateiname()
            lFilePath = os.path.join(self._base_dir, "Data", lCakeDatei)
        else: 
            lKlassenDatei = self.mSettings.getKlassenDateiname()
            lFilePath = os.path.join(self._base_dir, "Data", "Klassen", lKlassenDatei)
        try:
            with open(lFilePath, 'w', newline='') as csvfile:
                lWriter = csv.writer(csvfile, delimiter=',')
                if aForMainTable:
                    lWriter.writerow(self.mMainHeaders)
                    lWriter.writerows(self.getData())
                else:
                    lWriter.writerow(self.mMailHeaders)
                    lWriter.writerows(self.getMailData())
            return True       
        except OSError as e:
            self.mLogger.error("Save File", f"Error saving file: {e}")
            return False
        
    def ImportFile(self, aPath, aForMainTable = True):
        try:
            with open(aPath, newline='') as csvfile:
                lSample = csvfile.read(4096)
                csvfile.seek(0)
                lDialect = csv.Sniffer().sniff(lSample)
                lReader = csv.reader(csvfile, dialect=lDialect)
                if aForMainTable:
                    self.setData(list(lReader))          
                    self.mMainHeaders = self.getData()[0]
                    del self.getData()[0]
                    self._padRows(self.getData(), len(self.mMainHeaders))
                    self.setSortedData([row[:] for row in self.getData()])
                else:
                    self.setMailData(list(lReader))          
                    self.mMailHeaders = self.getMailData()[0]
                    del self.getMailData()[0]
                    self._padRows(self.getMailData(), len(self.mMailHeaders))
                    self.setSortedMailData([row[:] for row in self.getMailData()])
        except (OSError, csv.Error) as e:
            self.mLogger.error("Import File", f"Error importing file: {e}")
    
    
    def createCompleteMailData(self):
        lCompleteMailData = []
        lMails = []
        for lMail in self.mMailData:
            lMails.append(lMail[1])
        lCompleteMailData.append(lMails)
        lHtmlBody = self.createHtmlDataString(aHeaders=self.mMainHeaders)
        lCompleteMailData.append(lHtmlBody)
        self.setCompleteMailData(lCompleteMailData)
        return lCompleteMailData
    
    def createHtmlDataString(self, aHeaders = None):
        table_style = "width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;"
        th_style = "background-color: #f2f2f2; color: #333; font-weight: bold; padding: 12px; border: 1px solid #dddddd; text-align: left;"
        td_style = "padding: 8px; border: 1px solid #dddddd; text-align: left;"
        tr_even_style = "background-color: #f9f9f9;"

        lHtml = f'<table style="{table_style}">\n'

        if aHeaders:
            lHtml += "  <thead>\n    <tr>\n"
            for header in aHeaders:
                lHtml += f'      <th style="{th_style}">{html.escape(str(header))}</th>\n'
            lHtml += "    </tr>\n  </thead>\n"

        lHtml += "  <tbody>\n"
        for i, row in enumerate(self.mData):
            style = tr_even_style if i % 2 == 0 else ""
            lHtml += f'    <tr style="{style}">\n'
            for item in row:
                lHtml += f'      <td style="{td_style}">{html.escape(str(item))}</td>\n'
            lHtml += "    </tr>\n"

        lHtml += "  </tbody>\n</table>"
        return lHtml