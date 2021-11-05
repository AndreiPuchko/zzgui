from configparser import ConfigParser
from utils import num
import re


class ZzSettings:
    def __init__(self, filename="zzGui.ini"):
        self.filename = filename
        self.config = ConfigParser()
        self.read()

    def read(self):
        self.config.read(self.filename)

    def write(self):
        with open(self.filename, "w") as configfile:
            self.config.write(configfile)

    def prepSection(self, section):
        return (
            re.sub("\[.*\]", "", section)
            .strip()
            .split("\n")[0]
            .replace("\n", "")
            .strip()
        )

    def get(self, section="", key="", defaultValue=""):
        # section=re.sub("\[.*\]","",section).strip().split("\n")[0].replace("\n","")
        section = self.prepSection(section)
        try:
            return self.config.get(section, key)
        except Exception:
            return defaultValue

    def set(self, section="", key="", value=""):
        # section=re.sub("\[.*\]","",section).strip().split("\n")[0].replace("\n","")
        section = self.prepSection(section)
        value = "%(value)s" % locals()
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)


class ZzWindow:
    def set_title(self):
        pass

    def set_position(self, left, top):
        pass

    def set_size(self, width, height):
        pass

    def get_position(self):
        pass

    def get_size(self):
        pass

    def restore_geometry(self, settings):
        left = num(settings.get("MainWindow", "left", "0"))
        top = num(settings.get("MainWindow", "top", "0"))
        self.set_position(left, top)
        width = num(settings.get("MainWindow", "width", "800"))
        height = num(settings.get("MainWindow", "height", "600"))
        self.set_size(width, height)

    def save_geometry(self, settings):
        pos = self.get_position()
        settings.set("MainWindow", "left", pos[0])
        settings.set("MainWindow", "top", pos[1])
        size = self.get_size()
        settings.set("MainWindow", "width", size[0])
        settings.set("MainWindow", "height", size[1])
        settings.write()


class ZzApp:
    def __init__(self):
        super().__init__()
        # self.setStyle("Fusion")
        # print(QStyleFactory.keys())
        # if zzApp.zzApp.cssfile:
        #     try:
        #         self.setStyleSheet(open(zzApp.zzApp.cssfile).read())
        #     except:
        #         print("css file loading error")

        # self._margins = [10, 10, 10, 10]
        # self._spacing = 10
        self.settings = ZzSettings()
        self.main_widget = None
        self.mainMenu = {}
        # self.justClosed = None
        # qApp.zzApp=self
        # self.focusChanged.connect(self._focusChanged)

    @staticmethod
    def app(engine="PyQt5"):
        if engine == "PyQt5":
            from zz_qt5.widgets import ZzQtApp

            return ZzQtApp()

    def close(self):
        self.main_widget.save_geometry(self.settings)

    def run(self):
        self.main_widget.restore_geometry(self.settings)
        self.on_start()

    def on_start(self):
        pass


if __name__ == "__main__":
    app = ZzApp.app()
    app.run()
