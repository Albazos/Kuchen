import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QDialog
from PySide6.QtGui import QStandardItem, QStandardItemModel, QIcon
from PySide6.QtCore import Qt

import DataManager as DM
import KuchenMailManager as KMM
import LoginDialog as LD
from UIMainWindow_ui import Ui_MainWindow  


class CMainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.mHeaders = ["Name", "CakeCount","Hanuta","Waffel", "Date"]
        self.mDM = DM.DataManager()
        self.mKMM = None
        self.mISMM = None
        
        self.clearLabels()
        
        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnAdd.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)
        self.pbnOpenMailList.clicked.connect(self.ShowMailListDialog)
        self.pbnSendMail.clicked.connect(self.SendMails)
        #self.pbnSendMail.setDisabled(True)
        
        self.rbnName.toggled.connect(self.SortColumn)
        self.rbnCakeCount.toggled.connect(self.SortColumn)
        self.rbnHanuta.toggled.connect(self.SortColumn)
        self.rbnWaffel.toggled.connect(self.SortColumn)
        self.rbnDate.toggled.connect(self.SortColumn)

        self.leSearch.textChanged.connect(self.Search)

        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile():
            self.FillTable()
            self.labInfo.setText("File imported successfully")
        else:
            self.labInfo.setText("No file selected")
        self.SortColumn()
    
    def SaveFile(self):
        if self.mDM.SaveFile():
            self.labInfo.setText("File saved successfully")
        else:
            self.labInfo.setText("Error with File Save")
            
    def ShowMailListDialog(self):
        self.mKMM = KMM.CKuchenDialog(aDataManager=self.mDM)
        self.mKMM.exec()
        self.mDM.getData()
    
    def SendMails(self):
        lLD = LD.CLoginDialog(aMailData = self.mDM.createCompleteMailData())
        lLD.exec() # type: ignore
        if lLD.getSendState() == False:
            self.labInfo.setText("ERROR with Mail")
        else:
            self.labInfo.setText("Mails sent")
            
        
    def ImportFile(self):
        lFileDialog = QFileDialog()
        lFileDialog.setNameFilter("CSV files (*.csv)")
        lFileDialog.setViewMode(QFileDialog.ViewMode.List)
        lFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.rbnDate.setEnabled(True)
        self.rbnCakeCount.setEnabled(True)
        self.rbnHanuta.setEnabled(True)
        self.rbnWaffel.setEnabled(True)
        self.rbnName.setEnabled(True)
        if lFileDialog.exec():
            lSelectedFile = lFileDialog.selectedFiles()
            if lSelectedFile:
                lFilePath = lSelectedFile[0]
                self.mDM.ImportFile(lFilePath)
                self.FillTable()
                self.labInfo.setText("File imported successfully")
        else:
            self.labInfo.setText("No file selected")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedData()
        if lSData == None: 
            return
        for lRowID, lRowData in enumerate(lSData):  
            for lColID, lColData in enumerate(lRowData):
                lItem = QStandardItem(lColData)
                self.model.setItem(lRowID, lColID, lItem)
        self.clearLabels(aSearch)
        
    
    def AddRow(self):
        lData = self.mDM.getData()
        lData.append([""] * len(self.mHeaders))
        self.mDM.setData(lData)
        self.mDM.setSortedData(self.mDM.getData())
        self.FillTable()
    
    
    def DeleteSelected(self):
        lSelectedRows = sorted(set(index.row() for index in self.tableView.selectionModel().selectedIndexes()), reverse=True)
        if lSelectedRows:
            lSData = self.mDM.getSortedData()
            for lRow in lSelectedRows:
                del lSData[lRow]
            self.mDM.setSortedData(lSData)
            self.FillTable()
            self.labInfo.setText("Successfully removed selected row(s)")
        else:
            self.labInfo.setText("No rows selected")

    
    def clearLabels(self, aSearch=False):
        self.labInfo.setText("")
        if not aSearch:
            self.leSearch.setText("")

    
    def QuitButton(self):
        lReply = QMessageBox.question(
            self, "Beenden",
            "Möchtest du vor dem Beenden speichern?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if lReply == QMessageBox.StandardButton.Yes:
            self.SaveFile()
            self.close()
        elif lReply == QMessageBox.StandardButton.No:
            self.close()
        # Cancel: do nothing

    
    def SortColumn(self):
        lSortColumn = None
        if self.rbnName.isChecked():
            lSortColumn = "Name"
        elif self.rbnCakeCount.isChecked():
            lSortColumn = "CakeCount"
        elif self.rbnHanuta.isChecked():
            lSortColumn = "Hanuta"
        elif self.rbnWaffel.isChecked():
            lSortColumn = "Waffel"
        elif self.rbnDate.isChecked():
            lSortColumn = "Date"

        if lSortColumn:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn))
            self.mDM.sortData(self.mDM.getSortedColumnIndex())
            self.FillTable(True)

    def CellEdited(self, aItem):
        lRow = aItem.row()
        lCol = aItem.column()
        lValue = aItem.data(Qt.DisplayRole)  # type: ignore
        lSData = self.mDM.getSortedData()
        lSData[lRow][lCol] = lValue
        self.mDM.setSortedData(lSData)


    def Search(self, aText):
        if self.checkforEnabledRBN():
            if aText.strip():
                lFiltered = [lRow for lRow in self.mDM.getData() if aText.lower() in str(lRow[self.mDM.getSortedColumnIndex()]).lower()]
                self.mDM.setSortedData(lFiltered)
            else:
                self.mDM.setSortedData([row[:] for row in self.mDM.getData()])
        else:
            if aText.strip():  
               self.mDM.setSortedData([lRow for lRow in self.mDM.getData() if any(aText.lower() in str(lCell).lower() for lCell in lRow)])
            else:
                self.mDM.setSortedData([row[:] for row in self.mDM.getData()])
    
        self.FillTable(True)

            
    def checkforEnabledRBN(self):
        return (self.rbnCakeCount.isChecked() or
                self.rbnHanuta.isChecked() or
                self.rbnName.isChecked() or
                self.rbnWaffel.isChecked() or
                self.rbnDate.isChecked())
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kuchen_icon.svg")
    app.setWindowIcon(QIcon(icon_path))
    lCMainWindow = CMainWindow()
    lCMainWindow.setWindowIcon(QIcon(icon_path))
    lCMainWindow.show()
    lCMainWindow.activateWindow()
    sys.exit(app.exec())