from PySide6.QtWidgets import QFileDialog, QDialog, QHeaderView
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

from ui.UIMailsDialog_ui import Ui_Dialog
from . import AppLogger as AL

class CKuchenDialog(QDialog, Ui_Dialog):
    
    def __init__(self, aDataManager):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("")
        
        self.mDM = aDataManager
        self.mLogger = AL.AppLogger()
        self.clearLabels()
        
        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnSaveRecipientList.clicked.connect(self.SaveFile)
        self.pbnAddRecipient.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)
        self.pbnAddColumn.clicked.connect(self.AddColumn)

        self.ledSearch.textChanged.connect(self.Search)
        self.cmbSortField.currentIndexChanged.connect(self.SortColumn)
        self.cmbSortDirection.currentIndexChanged.connect(self.SortColumn)

        self.model = QStandardItemModel()
        self.tbvMailList.setModel(self.model)
        self.tbvMailList.horizontalHeader().setStretchLastSection(True)
        self.tbvMailList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile(aForMainTable=False):
            self.mHeaders = self.mDM.mMailHeaders[:]
            self._createRadioButtons()
            self.SortColumn()
        else:
            self.mHeaders = []
            self.mLogger.warning("Load", "No standard mail list could be loaded.")
    
    def SaveFile(self):
        if self.mDM.SaveFile(aForMainTable=False):
            pass
        else:
            self.mLogger.error("Save", "Error saving mail list.")
            
            
    def ImportFile(self):
        lFileDialog = QFileDialog()
        lFileDialog.setNameFilter("CSV files (*.csv)")
        lFileDialog.setViewMode(QFileDialog.ViewMode.List)
        lFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if lFileDialog.exec():
            lSelectedFile = lFileDialog.selectedFiles()
            if lSelectedFile:
                lFilePath = lSelectedFile[0]
                if self.mDM.ImportFile(lFilePath, aForMainTable=False):
                    self.mHeaders = self.mDM.mMailHeaders[:]
                    self._createRadioButtons()
                    self.FillTable()
                else:
                    self.mLogger.error("Import", "Mail list import failed.")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedMailData()
        self.lblTableMeta.setText(f"{len(lSData)} recipients")
        if not lSData: 
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
        self.mDM.setSortedMailData(list(lData))
        self.FillTable()
    
    
    def DeleteSelected(self):
        lSelectedRows = sorted(set(index.row() for index in self.tbvMailList.selectionModel().selectedIndexes()), reverse=True)
        if lSelectedRows:
            lSData = self.mDM.getSortedMailData()
            lData = self.mDM.getMailData()
            for lRow in lSelectedRows:
                lDeletedRow = lSData[lRow]
                del lSData[lRow]
                try:
                    lData.remove(lDeletedRow)
                except ValueError:
                    pass
            self.mDM.setMailData(lData)
            self.mDM.setSortedMailData(lSData)
            self.FillTable()
        else:
            self.mLogger.warning("Delete", "No rows selected.")

    
    def clearLabels(self, aSearch=False):
        if not aSearch:
            self.ledSearch.setText("")

    
    def QuitButton(self):
        self.close()

    
    def _isDescending(self):
        return self.cmbSortDirection.currentText() == "Descending"

    def SortColumn(self):
        lSortColumn = self.cmbSortField.currentText()
        if lSortColumn and lSortColumn in self.mHeaders:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn), aForMain=False)
            self.mDM.sortData(self.mDM.getSortedColumnIndex(aForMain=False), aReverse=self._isDescending(), aForMain=False)
            lSearchText = self.ledSearch.text()
            if lSearchText.strip():
                self.Search(lSearchText)
            else:
                self.FillTable(True)

    def CellEdited(self, aItem):
        lRow = aItem.row()
        lCol = aItem.column()
        lValue = aItem.data(Qt.DisplayRole)  # type: ignore
        lSData = self.mDM.getSortedMailData()
        if 0 <= lRow < len(lSData) and 0 <= lCol < len(lSData[lRow]):
            lSData[lRow][lCol] = lValue
            self.mDM.setSortedMailData(lSData)


    def Search(self, aText):
        if self.checkforEnabledRBN():
            if aText.strip():
                lFiltered = [lRow for lRow in self.mDM.getMailData() if aText.lower() in str(lRow[self.mDM.getSortedMailColumnIndex()]).lower()]
                self.mDM.setSortedMailData(lFiltered)
            else:
                self.mDM.setSortedMailData(list(self.mDM.getMailData()))
            self.mDM.sortData(self.mDM.getSortedColumnIndex(aForMain=False), aReverse=self._isDescending(), aForMain=False)
        else:
            if aText.strip():  
               self.mDM.setSortedMailData([lRow for lRow in self.mDM.getMailData() if any(aText.lower() in str(lCell).lower() for lCell in lRow)])
            else:
                self.mDM.setSortedMailData(list(self.mDM.getMailData()))
    
        self.FillTable(True)

            
    def checkforEnabledRBN(self):
        return self.cmbSortField.currentText() in self.mHeaders

    def _createRadioButtons(self):
        lCurrentSelection = self.cmbSortField.currentText()
        self.cmbSortField.blockSignals(True)
        self.cmbSortField.clear()
        self.cmbSortField.addItems(self.mHeaders)
        if lCurrentSelection in self.mHeaders:
            self.cmbSortField.setCurrentText(lCurrentSelection)
        elif self.mHeaders:
            self.cmbSortField.setCurrentIndex(0)
        self.cmbSortField.blockSignals(False)

    def AddColumn(self):
        self.mLogger.info("Add Column", "Add column is not implemented yet.")
