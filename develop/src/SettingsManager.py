import configparser
import os
import sys


def _get_base_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SettingsManager:
    """Liest und schreibt Einstellungen aus Data/Settings/settings.ini."""

    _DEFAULTS = {
        "Klassen": {
            "Dateiname": "StandardKlasse.csv",
        },
        "CakeData": {
            "Dateiname": "StandardCakeData.csv",
        },
        "IServ": {
            "Domain": "wvss.de",
        },
    }

    def __init__(self):
        self._base_dir = _get_base_dir()
        self._settings_dir = os.path.join(self._base_dir, "Data", "Settings")
        self._settings_path = os.path.join(self._settings_dir, "settings.ini")
        self._config = configparser.ConfigParser()

        # Defaults setzen, dann INI laden (falls vorhanden)
        self._config.read_dict(self._DEFAULTS)
        if os.path.isfile(self._settings_path):
            self._config.read(self._settings_path, encoding="utf-8")

    def get(self, aSection, aKey):
        return self._config.get(aSection, aKey)

    def set(self, aSection, aKey, aValue):
        if not self._config.has_section(aSection):
            self._config.add_section(aSection)
        self._config.set(aSection, aKey, aValue)

    def save(self):
        os.makedirs(self._settings_dir, exist_ok=True)
        with open(self._settings_path, "w", encoding="utf-8") as f:
            self._config.write(f)

    def getKlassenDateiname(self):
        return self.get("Klassen", "Dateiname")

    def setKlassenDateiname(self, aDateiname):
        self.set("Klassen", "Dateiname", aDateiname)

    def getCakeDataDateiname(self):
        return self.get("CakeData", "Dateiname")

    def setCakeDataDateiname(self, aDateiname):
        self.set("CakeData", "Dateiname", aDateiname)

    def getIServDomain(self):
        return self.get("IServ", "Domain")

    def setIServDomain(self, aDomain):
        self.set("IServ", "Domain", aDomain)
