from PySide6.QtWidgets import QApplication, QFileDialog, QDialog
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

from UIMailsDialog_ui import Ui_Dialog
import DataManager as DM

class CKuchenDialog(QDialog, Ui_Dialog):
    
    def __init__(self, aDataManager):
        super().__init__()
        self.setupUi(self)
        
        self.mHeaders = ["Name", "Mail"]
        self.mDM = aDataManager
        self.mISMM = None
        self.clearLabels()
        
        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnAdd.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)

        self.rbnName.toggled.connect(self.SortColumn)
        self.rbnMail.toggled.connect(self.SortColumn)

        self.leSearch.textChanged.connect(self.Search)

        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile(aForMainTable=False):
            self.FillTable()
            self.labInfo.setText("File imported successfully")
        else:
            self.labInfo.setText("No file selected")
        self.SortColumn()
    
    def SaveFile(self):
        if self.mDM.SaveFile(aForMainTable=False):
            self.labInfo.setText("File saved successfully")
        else:
            self.labInfo.setText("Error with File Save")
            
            
    def ImportFile(self):
        lFileDialog = QFileDialog()
        lFileDialog.setNameFilter("CSV files (*.csv)")
        lFileDialog.setViewMode(QFileDialog.ViewMode.List)
        lFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.rbnMail.setEnabled(True)
        self.rbnName.setEnabled(True)
        if lFileDialog.exec():
            lSelectedFile = lFileDialog.selectedFiles()
            if lSelectedFile:
                lFilePath = lSelectedFile[0]
                self.mDM.ImportFile(lFilePath, aForMainTable=False)
                self.FillTable()
                self.labInfo.setText("File imported successfully")
        else:
            self.labInfo.setText("No file selected")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedMailData()
        if lSData == None: 
            return
        for lRowID, lRowData in enumerate(lSData):  
            for lColID, lColData in enumerate(lRowData):
                lItem = QStandardItem(lColData)
                self.model.setItem(lRowID, lColID, lItem)
        self.clearLabels(aSearch)
        
    
    def AddRow(self):
        lData = self.mDM.getMailData()
        lData.append([""] * len(self.mHeaders))
        self.mDM.setMailData(lData)
        self.mDM.setSortedMailData(self.mDM.getMailData())
        self.FillTable()
    
    
    def DeleteSelected(self):
        lSelectedRows = sorted(set(index.row() for index in self.tableView.selectionModel().selectedIndexes()), reverse=True)
        if lSelectedRows:
            lSData = self.mDM.getSortedMailData()
            for lRow in lSelectedRows:
                del lSData[lRow]
            self.mDM.setSortedMailData(lSData)
            self.FillTable()
            self.labInfo.setText("Successfully removed selected row(s)")
        else:
            self.labInfo.setText("No rows selected")

    
    def clearLabels(self, aSearch=False):
        self.labInfo.setText("")
        if not aSearch:
            self.leSearch.setText("")

    
    def QuitButton(self):
        self.close()

    
    def SortColumn(self):
        lSortColumn = None
        if self.rbnName.isChecked():
            lSortColumn = "Name"
        elif self.rbnMail.isChecked():
            lSortColumn = "Mail"

        if lSortColumn:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn), aForMain=False )
            self.mDM.sortData(self.mDM.getSortedColumnIndex(aForMain=False),aForMain=False)
            self.FillTable(True)

    def CellEdited(self, aItem):
        lRow = aItem.row()
        lCol = aItem.column()
        lValue = aItem.data(Qt.DisplayRole)  # type: ignore
        lSData = self.mDM.getSortedMailData()
        lSData[lRow][lCol] = lValue
        self.mDM.setSortedMailData(lSData)


    def Search(self, aText):
        if self.checkforEnabledRBN():
            if aText.strip():
                lFiltered = [lRow for lRow in self.mDM.getMailData() if aText.lower() in str(lRow[self.mDM.getSortedMailColumnIndex()]).lower()]
                self.mDM.setSortedMailData(lFiltered)
            else:
                self.mDM.setSortedMailData([row[:] for row in self.mDM.getMailData()])
        else:
            if aText.strip():  
               self.mDM.setSortedMailData([lRow for lRow in self.mDM.getMailData() if any(aText.lower() in str(lCell).lower() for lCell in lRow)])
            else:
                self.mDM.setSortedMailData([row[:] for row in self.mDM.getMailData()])
    
        self.FillTable(True)

            
    def checkforEnabledRBN(self):
        return (self.rbnName.isChecked() or
                self.rbnMail.isChecked())
