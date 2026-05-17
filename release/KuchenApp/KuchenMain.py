import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QHeaderView
from PySide6.QtGui import QStandardItem, QStandardItemModel, QIcon
from PySide6.QtCore import Qt

from src import DataManager as DM
from src import KuchenMailManager as KMM
from src import LoginDialog as LD
from src import AppLogger as AL
from ui.UIMainWindow_ui import Ui_MainWindow  


class CMainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet("")
        
        self.mDM = DM.DataManager()
        self.mKMM = None
        
        self.mLogger = AL.AppLogger()
        self.mLogger.errorOccurred.connect(self._showError)
        self.mLogger.warningOccurred.connect(self._showWarning)
        self.mLogger.infoOccurred.connect(self._showInfo)
        
        self.clearLabels()

        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnImportToolbar.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnSaveToolbar.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnAddEntry.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)
        self.pbnOpenMailList.clicked.connect(self.ShowMailListDialog)
        self.pbnSendMail.clicked.connect(self.SendMails)
        self.pbnAddColumn.clicked.connect(self.AddColumn)
        self.pbnChangeClass.clicked.connect(self.ChangeClass)

        self.ledSearch.textChanged.connect(self.Search)
        self.cmbSortField.currentIndexChanged.connect(self.SortColumn)
        self.cmbSortDirection.currentIndexChanged.connect(self.SortColumn)

        self.model = QStandardItemModel()
        self.tbvCakeList.setModel(self.model)
        self.tbvCakeList.horizontalHeader().setStretchLastSection(True)
        self.tbvCakeList.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile():
            self.mHeaders = self.mDM.mMainHeaders[:]
            self._createRadioButtons()
            self.SortColumn()
        else:
            self.mHeaders = []
            self.mLogger.warning("Load", "No standard file could be loaded.")
        
        # Mail-Liste beim Start laden
        self.mDM.LoadStandardFile(aForMainTable=False)
    
    def SaveFile(self):
        if self.mDM.SaveFile():
            pass
        else:
            self.mLogger.error("Save", "Error saving file.")
            
    def ShowMailListDialog(self):
        self.mKMM = KMM.CKuchenDialog(aDataManager=self.mDM)
        self.mKMM.exec()
    
    def SendMails(self):
        lMailData = self.mDM.createCompleteMailData()
        lRecipients = lMailData[0]
        lCount = len(lRecipients)
        if lCount == 0:
            self.mLogger.warning("Mail", "No recipients found.")
            return
        lReply = QMessageBox.question(
            self, "Mail senden",
            f"Mail an {lCount} Empfänger senden?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if lReply != QMessageBox.StandardButton.Yes:
            return
        lLD = LD.CLoginDialog(aMailData=lMailData)
        lLD.exec() # type: ignore
        lState = lLD.getSendState()
        if lState is None:
            pass  # User cancelled, no message needed
        elif lState:
            self.mLogger.info("Mail", "Mails sent successfully.")
        else:
            self.mLogger.error("Mail", "Failed to send mails.")
            
        
    def ImportFile(self):
        lFileDialog = QFileDialog()
        lFileDialog.setNameFilter("CSV files (*.csv)")
        lFileDialog.setViewMode(QFileDialog.ViewMode.List)
        lFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if lFileDialog.exec():
            lSelectedFile = lFileDialog.selectedFiles()
            if lSelectedFile:
                lFilePath = lSelectedFile[0]
                if self.mDM.ImportFile(lFilePath):
                    self.mHeaders = self.mDM.mMainHeaders[:]
                    self._createRadioButtons()
                    self.FillTable()
                else:
                    self.mLogger.error("Import", "Import failed.")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedData()
        self.lblTableMeta.setText(f"{len(lSData)} entries")
        if not lSData: 
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
        self.mDM.setSortedData(list(lData))
        self.FillTable()
    
    
    def DeleteSelected(self):
        lSelectedRows = sorted(set(index.row() for index in self.tbvCakeList.selectionModel().selectedIndexes()), reverse=True)
        if lSelectedRows:
            lSData = self.mDM.getSortedData()
            lData = self.mDM.getData()
            for lRow in lSelectedRows:
                lDeletedRow = lSData[lRow]
                del lSData[lRow]
                try:
                    lData.remove(lDeletedRow)
                except ValueError:
                    pass
            self.mDM.setData(lData)
            self.mDM.setSortedData(lSData)
            self.FillTable()
        else:
            self.mLogger.warning("Delete", "No rows selected.")

    
    def clearLabels(self, aSearch=False):
        if not aSearch:
            self.ledSearch.setText("")

    
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

    
    def _isDescending(self):
        return self.cmbSortDirection.currentText() == "Descending"

    def SortColumn(self):
        lSortColumn = self.cmbSortField.currentText()
        if lSortColumn and lSortColumn in self.mHeaders:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn))
            self.mDM.sortData(self.mDM.getSortedColumnIndex(), aReverse=self._isDescending())
            lSearchText = self.ledSearch.text()
            if lSearchText.strip():
                self.Search(lSearchText)
            else:
                self.FillTable(True)

    def CellEdited(self, aItem):
        lRow = aItem.row()
        lCol = aItem.column()
        lValue = aItem.data(Qt.DisplayRole)  # type: ignore
        lSData = self.mDM.getSortedData()
        if 0 <= lRow < len(lSData) and 0 <= lCol < len(lSData[lRow]):
            lSData[lRow][lCol] = lValue
            self.mDM.setSortedData(lSData)


    def Search(self, aText):
        if self.checkforEnabledRBN():
            if aText.strip():
                lFiltered = [lRow for lRow in self.mDM.getData() if aText.lower() in str(lRow[self.mDM.getSortedColumnIndex()]).lower()]
                self.mDM.setSortedData(lFiltered)
            else:
                self.mDM.setSortedData(list(self.mDM.getData()))
            self.mDM.sortData(self.mDM.getSortedColumnIndex(), aReverse=self._isDescending())
        else:
            if aText.strip():  
               self.mDM.setSortedData([lRow for lRow in self.mDM.getData() if any(aText.lower() in str(lCell).lower() for lCell in lRow)])
            else:
                self.mDM.setSortedData(list(self.mDM.getData()))
    
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

    def ChangeClass(self):
        self.mLogger.info("Change Class", "Change class is not implemented yet.")

    def _showError(self, aTitle, aMessage):
        QMessageBox.critical(self, aTitle, aMessage)

    def _showWarning(self, aTitle, aMessage):
        QMessageBox.warning(self, aTitle, aMessage)

    def _showInfo(self, aTitle, aMessage):
        QMessageBox.information(self, aTitle, aMessage)


def _load_app_theme(aApplication):
    lBasePath = os.path.dirname(os.path.abspath(__file__))
    lThemePath = os.path.join(lBasePath, "assets", "theme_dark_blue.qss")
    lAssetDir = os.path.join(lBasePath, "assets").replace("\\", "/")
    with open(lThemePath, encoding="utf-8") as lThemeFile:
        lStylesheet = lThemeFile.read().replace("__ASSET_DIR__", lAssetDir)
    aApplication.setStyleSheet(lStylesheet)
        
if __name__ == "__main__":
    # Set AppUserModelID so Windows taskbar shows our icon instead of Python's
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("KuchenApp")

    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # type: ignore
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "assets", "kuchen_icon.svg")
    app.setWindowIcon(QIcon(icon_path))
    _load_app_theme(app)
    lCMainWindow = CMainWindow()
    lCMainWindow.setWindowIcon(QIcon(icon_path))
    lCMainWindow.show()
    lCMainWindow.activateWindow()
    sys.exit(app.exec())
