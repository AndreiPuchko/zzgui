import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from configparser import ConfigParser
import zzgui.zzapp as zzapp
from zzgui.zzwindow import ZzWindow
import re

zz_app = None


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
            re.sub(r"\[.*\]", "", section)
            .strip()
            .split("\n")[0]
            .replace("\n", "")
            .strip()
        )

    def get(self, section="", key="", defaultValue=""):
        section = self.prepSection(section)
        try:
            return self.config.get(section, key)
        except Exception:
            return defaultValue

    def set(self, section="", key="", value=""):
        if section == "":
            return
        section = self.prepSection(section)
        value = "%(value)s" % locals()
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)


class ZzApp:
    def __init__(self, title=""):
        zzapp.zz_app = self
        self.window_title = title
        self.settings = ZzSettings()
        self.main_window = ZzMainWindow(title)
        self.menu_list = []
        self.on_init()
        self.main_window.show()

    def add_menu(self, text="", worker=None, before=None, toolbar=None):
        if text.endswith("|"):
            text = text[:-1]
        if text.startswith("|"):
            text = text[1:]
        self.menu_list.append(
            {"TEXT": text, "WORKER": worker, "BEFORE": before, "TOOLBAR": toolbar}
        )

    def build_menu(self):
        self.menu_list = self.reorder_menu(self.menu_list)

    def reorder_menu(self, menu):
        tmpList = [x["TEXT"] for x in menu]
        tmpDict = {x["TEXT"]: x for x in menu}
        reOrderedList = []
        for x in tmpList:
            # add node element for menu
            menu_node = "|".join(x.split("|")[:-1])
            if menu_node not in reOrderedList:
                reOrderedList.append(menu_node)
                tmpDict[menu_node] = {
                    "TEXT": menu_node,
                    "WORKER": None,
                    "BEFORE": None,
                    "TOOLBAR": None,
                }
            if tmpDict[x].get("BEFORE") in reOrderedList:
                reOrderedList.insert(reOrderedList.index(tmpDict[x].get("BEFORE")), x)
            else:
                reOrderedList.append(x)
        return [tmpDict[x] for x in reOrderedList]

    def close(self):
        self.main_window.close()

    def show_form(self, form=None, modal="modal"):
        pass

    def on_init(self):
        pass

    def on_start(self):
        pass

    def show_menubar(self, mode=True):
        pass

    def hide_menubar(self, mode=True):
        if mode:
            self.show_menubar(False)
        else:
            self.show_menubar(True)

    def is_menubar_visible(self):
        pass

    def show_toolbar(self, mode=True):
        pass

    def hide_toolbar(self, mode=True):
        if mode:
            self.show_toolbar(False)
        else:
            self.show_toolbar(True)

    def is_toolbar_visible(self):
        pass

    def show_tabbar(self, mode=True):
        pass

    def hide_tabbar(self, mode=True):
        if mode:
            self.show_tabbar(False)
        else:
            self.show_tabbar(True)

    def is_tabbar_visible(self):
        pass

    def show_statusbar(self, mode=True):
        pass

    def hide_statusbar(self, mode=True):
        if mode:
            self.show_statusbar(False)
        else:
            self.show_statusbar(True)

    def is_statusbar_visible(self):
        pass

    def run(self):
        self.main_window.restore_geometry(self.settings)
        self.on_start()
        self.build_menu()
        self.show_menubar(True)
        pass


class ZzMainWindow(ZzWindow):
    def __init__(self, title=""):
        super().__init__()
        self.window_title = title
        self.settings = ZzSettings()
        self.menu_list = []
        self._main_menu = {}
        # self.on_init()

        self.zz_toolbar = None
        self.zz_tabwidget = None

    def zz_layout(self):
        pass

    def _run(self):
        self.restore_geometry(self.settings)
        self.build_menu()
        self.show_menubar(True)
        self.on_start()
        return self

    def show(self):
        pass

    def _close(self):
        self.save_geometry(self.settings)

    def _on_init(self):
        pass

    def on_start(self):
        pass
