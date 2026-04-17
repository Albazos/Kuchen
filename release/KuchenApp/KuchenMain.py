import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QRadioButton
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
        
        self.mDM = DM.DataManager()
        self.mKMM = None
        self.mRadioButtons = []
        
        self.mLogger = AL.AppLogger()
        self.mLogger.errorOccurred.connect(self._showError)
        self.mLogger.warningOccurred.connect(self._showWarning)
        self.mLogger.infoOccurred.connect(self._showInfo)
        
        self.clearLabels()
        
        self.pbnImport.clicked.connect(self.ImportFile)
        self.pbnSave.clicked.connect(self.SaveFile)
        self.pbnQuit.clicked.connect(self.QuitButton)
        self.pbnAdd.clicked.connect(self.AddRow)
        self.pbnDelete.clicked.connect(self.DeleteSelected)
        self.pbnOpenMailList.clicked.connect(self.ShowMailListDialog)
        self.pbnSendMail.clicked.connect(self.SendMails)
        #self.pbnSendMail.setDisabled(True)

        self.leSearch.textChanged.connect(self.Search)

        self.model = QStandardItemModel()
        self.tableView.setModel(self.model)

        self.model.dataChanged.connect(self.CellEdited)
        if self.mDM.LoadStandardFile():
            self.mHeaders = self.mDM.mMainHeaders[:]
            self._createRadioButtons()
            self.FillTable()
            self.labInfo.setText("File imported successfully")
        else:
            self.mHeaders = []
            self.labInfo.setText("No file selected")
        self.SortColumn()
    
    def SaveFile(self):
        if self.mDM.SaveFile():
            self.mLogger.info("Save", "File saved successfully.")
        else:
            self.mLogger.error("Save", "Error saving file.")
            
    def ShowMailListDialog(self):
        self.mKMM = KMM.CKuchenDialog(aDataManager=self.mDM)
        self.mKMM.exec()
    
    def SendMails(self):
        lLD = LD.CLoginDialog(aMailData = self.mDM.createCompleteMailData())
        lLD.exec() # type: ignore
        if not lLD.getSendState():
            self.mLogger.error("Mail", "Failed to send mails.")
        else:
            self.mLogger.info("Mail", "Mails sent successfully.")
            
        
    def ImportFile(self):
        lFileDialog = QFileDialog()
        lFileDialog.setNameFilter("CSV files (*.csv)")
        lFileDialog.setViewMode(QFileDialog.ViewMode.List)
        lFileDialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if lFileDialog.exec():
            lSelectedFile = lFileDialog.selectedFiles()
            if lSelectedFile:
                lFilePath = lSelectedFile[0]
                self.mDM.ImportFile(lFilePath)
                self.mHeaders = self.mDM.mMainHeaders[:]
                self._createRadioButtons()
                self.FillTable()
                self.labInfo.setText("File imported successfully")
        else:
            self.labInfo.setText("No file selected")



    
    def FillTable(self, aSearch=False):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(self.mHeaders)
        lSData = self.mDM.getSortedData()
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
        self.mDM.setSortedData([row[:] for row in lData])
        self.FillTable()
    
    
    def DeleteSelected(self):
        lSelectedRows = sorted(set(index.row() for index in self.tableView.selectionModel().selectedIndexes()), reverse=True)
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
        for lRbn in self.mRadioButtons:
            if lRbn.isChecked():
                lSortColumn = lRbn.property("headerKey")
                break

        if lSortColumn and lSortColumn in self.mHeaders:
            self.mDM.setSortedColumnIndex(self.mHeaders.index(lSortColumn))
            self.mDM.sortData(self.mDM.getSortedColumnIndex())
            self.FillTable(True)

    def CellEdited(self, aItem):
        lRow = aItem.row()
        lCol = aItem.column()
        lValue = aItem.data(Qt.DisplayRole)  # type: ignore
        lSData = self.mDM.getSortedData()
        lOldValue = lSData[lRow][lCol]
        lSData[lRow][lCol] = lValue
        self.mDM.setSortedData(lSData)
        lData = self.mDM.getData()
        for lDataRow in lData:
            if lDataRow[lCol] == lOldValue and all(lDataRow[i] == lSData[lRow][i] for i in range(len(lDataRow)) if i != lCol):
                lDataRow[lCol] = lValue
                break
        self.mDM.setData(lData)


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
        return any(lRbn.isChecked() for lRbn in self.mRadioButtons)

    def _createRadioButtons(self):
        for lRbn in self.mRadioButtons:
            self.verticalLayout.removeWidget(lRbn)
            lRbn.deleteLater()
        self.mRadioButtons.clear()
        for i, lHeader in enumerate(self.mHeaders):
            lRbn = QRadioButton(lHeader)
            lRbn.setProperty("headerKey", lHeader)
            if i == 0:
                lRbn.setChecked(True)
            lRbn.toggled.connect(self.SortColumn)
            self.verticalLayout.addWidget(lRbn)
            self.mRadioButtons.append(lRbn)

    def _showError(self, aTitle, aMessage):
        QMessageBox.critical(self, aTitle, aMessage)

    def _showWarning(self, aTitle, aMessage):
        QMessageBox.warning(self, aTitle, aMessage)

    def _showInfo(self, aTitle, aMessage):
        QMessageBox.information(self, aTitle, aMessage)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "kuchen_icon.svg")
    app.setWindowIcon(QIcon(icon_path))
    lCMainWindow = CMainWindow()
    lCMainWindow.setWindowIcon(QIcon(icon_path))
    lCMainWindow.show()
    lCMainWindow.activateWindow()
    sys.exit(app.exec())