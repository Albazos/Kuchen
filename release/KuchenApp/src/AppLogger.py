from PySide6.QtCore import QObject, Signal


class AppLogger(QObject):
    """Singleton Logger mit Qt-Signalen fuer GUI-Fehlermeldungen."""

    errorOccurred = Signal(str, str)
    warningOccurred = Signal(str, str)
    infoOccurred = Signal(str, str)

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            self._initialized = True

    def error(self, aTitle, aMessage):
        self.errorOccurred.emit(aTitle, aMessage)

    def warning(self, aTitle, aMessage):
        self.warningOccurred.emit(aTitle, aMessage)

    def info(self, aTitle, aMessage):
        self.infoOccurred.emit(aTitle, aMessage)
