import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from configparser import ConfigParser
from zzgui.utils import num

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


class ZzWindow:
    def __init__(self, title=""):
        super().__init__()
        self.window_title = ""
        self.set_title(title)

    def set_title(self, title):
        self.window_title = title

    def set_position(self, left, top):
        pass

    def set_size(self, width, height):
        pass

    def get_position(self):
        pass

    def get_size(self):
        pass

    def is_maximized():
        pass

    def show_maximized():
        return 0

    def restore_geometry(self, settings):
        left = num(settings.get(self.window_title, "left", "0"))
        top = num(settings.get(self.window_title, "top", "0"))
        self.set_position(left, top)
        width = num(settings.get(self.window_title, "width", "800"))
        height = num(settings.get(self.window_title, "height", "600"))
        self.set_size(width, height)
        if num(settings.get(self.window_title, "is_max", "0")):
            self.show_maximized()

    def save_geometry(self, settings):
        settings.set(self.window_title, "is_max", f"{self.is_maximized()}")
        if not self.is_maximized():
            pos = self.get_position()
            settings.set(self.window_title, "left", pos[0])
            settings.set(self.window_title, "top", pos[1])
            size = self.get_size()
            settings.set(self.window_title, "width", size[0])
            settings.set(self.window_title, "height", size[1])
        settings.write()


class ZzApp(ZzWindow):
    def __init__(self, title=""):
        super().__init__()
        self.window_title = title
        self.settings = ZzSettings()
        self.menu_list = []
        self._main_menu = {}
        self.on_init()

        # self.toolbar = None
        # self.tab_widget = None

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

    def show_menubar(self, mode=True):
        pass

    def hide_menubar(self, mode=True):
        if mode:
            self.show_menubar(False)
        else:
            self.show_menubar(True)

    def is_menubar_visible(self):
        pass

    def reorder_menu(self, menu):
        tmpList = [x["TEXT"] for x in menu]
        print(tmpList)
        tmpDict = {x["TEXT"]: x for x in menu}
        reOrderedList = []
        for x in tmpList:
            # add node element for menu
            # if "|" in x:
            menu_node = "|".join(x.split("|")[:-1])
            # else:
            #     menu_node = x
            # print (f"{x}! {menu_node} !")
            # if menu_node == "":
            #     continue
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

    def show_toolbar(self, mode=True):
        pass

    def hide_toolbar(self, mode=True):
        if mode:
            self.show_toolbar(False)
        else:
            self.show_toolbar(True)

    def is_toolbar_visible(self):
        pass

    def run(self):
        self.restore_geometry(self.settings)
        self.build_menu()
        self.show_menubar(True)
        self.on_start()
        return self

    def close(self):
        self.save_geometry(self.settings)

    def on_init(self):
        pass

    def on_start(self):
        pass
