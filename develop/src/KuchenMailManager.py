from PySide6.QtWidgets import QFileDialog, QDialog, QRadioButton, QButtonGroup, QHBoxLayout
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtCore import Qt

from ui.UIMailsDialog_ui import Ui_Dialog
from . import AppLogger as AL

class CKuchenDialog(QDialog, Ui_Dialog):
    
    def __init__(self, aDataManager):
        super().__init__()
        self.setupUi(self)
        
        self.mDM = aDataManager
        self.mLogger = AL.AppLogger()
        self.mRadioButtons = []
        self.mRbnAscending = None
        self.mRbnDescending = None
        self.clearLabels()
        
        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnAdd.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)

        self.leSearch.textChanged.connect(self.Search)

        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile(aForMainTable=False):
            self.mHeaders = self.mDM.mMailHeaders[:]
            self._createRadioButtons()
            self.SortColumn()
            self.mLogger.info("Load", "Standard mail list loaded successfully.")
        else:
            self.mHeaders = []
            self.mLogger.warning("Load", "No standard mail list could be loaded.")
    
    def SaveFile(self):
        if self.mDM.SaveFile(aForMainTable=False):
            self.mLogger.info("Save", "Mail list saved successfully.")
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
                    self.mLogger.info("Import", "Mail list imported successfully.")
                else:
                    self.mLogger.error("Import", "Mail list import failed.")
        else:
            self.mLogger.info("Import", "No file selected.")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedMailData()
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
        lSelectedRows = sorted(set(index.row() for index in self.tableView.selectionModel().selectedIndexes()), reverse=True)
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
            self.mLogger.info("Delete", "Successfully removed selected row(s).")
        else:
            self.mLogger.warning("Delete", "No rows selected.")

    
    def clearLabels(self, aSearch=False):
        if not aSearch:
            self.leSearch.setText("")

    
    def QuitButton(self):
        self.close()

    
    def _isDescending(self):
        return self.mRbnDescending is not None and self.mRbnDescending.isChecked()

    def SortColumn(self):
        lSortColumn = None
        for lRbn in self.mRadioButtons:
            if lRbn.isChecked():
                lSortColumn = lRbn.property("headerKey")
                break

        if lSortColumn and lSortColumn in self.mHeaders:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn), aForMain=False)
            self.mDM.sortData(self.mDM.getSortedColumnIndex(aForMain=False), aReverse=self._isDescending(), aForMain=False)
            lSearchText = self.leSearch.text()
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
        return any(lRbn.isChecked() for lRbn in self.mRadioButtons)

    def _createRadioButtons(self):
        for lRbn in self.mRadioButtons:
            self.verticalLayout.removeWidget(lRbn)
            lRbn.deleteLater()
        self.mRadioButtons.clear()

        if self.mRbnAscending is not None:
            self.mRbnAscending.deleteLater()
            self.mRbnAscending = None
        if self.mRbnDescending is not None:
            self.mRbnDescending.deleteLater()
            self.mRbnDescending = None

        for i, lHeader in enumerate(self.mHeaders):
            lRbn = QRadioButton(lHeader)
            lRbn.setProperty("headerKey", lHeader)
            if i == 0:
                lRbn.setChecked(True)
            self.verticalLayout.addWidget(lRbn)
            self.mRadioButtons.append(lRbn)

        lOrderLayout = QHBoxLayout()
        self.mRbnAscending = QRadioButton("Ascending")
        self.mRbnDescending = QRadioButton("Descending")
        self.mRbnAscending.setChecked(True)
        lOrderGroup = QButtonGroup(self)
        lOrderGroup.addButton(self.mRbnAscending)
        lOrderGroup.addButton(self.mRbnDescending)
        lOrderLayout.addWidget(self.mRbnAscending)
        lOrderLayout.addWidget(self.mRbnDescending)
        self.verticalLayout.addLayout(lOrderLayout)

        for lRbn in self.mRadioButtons:
            lRbn.toggled.connect(self.SortColumn)
        self.mRbnAscending.toggled.connect(self.SortColumn)
        self.mRbnDescending.toggled.connect(self.SortColumn)
