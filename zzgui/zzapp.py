import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from configparser import ConfigParser
import zzgui.zzapp as zzapp
from zzgui.zzwindow import ZzWindow
import re

zz_app = None


class ZzHeap:
    pass


class ZzActions:
    def __init__(self, action=None):
        self.show_main_button = True
        self.show_actions = True
        if isinstance(action, list):
            self.action_list = action[:]
        else:
            self.action_list = []

    def add_action(self, text, worker=None, icon="", mess="", hotkey="", tag=""):
        """ "/view", "/crud" """
        action = {}
        action["text"] = text
        action["worker"] = worker
        action["icon"] = icon
        action["mess"] = mess
        action["hotkey"] = hotkey
        action["tag"] = tag
        self.action_list.append(action)
        return True

    # def insertAction(
    #     self, before, text, worker=None, icon="", mess="", key="", **kvargs
    # ):
    #     for x in self.addAction.__code__.co_varnames:
    #         if x not in ["kvargs", "self"]:
    #             kvargs[x] = locals()[x]
    #     self.action_list.insert(before, kvargs)

    # def removeAction(self, text):
    #     actionIndex = safe_index([x["text"] for x in self.action_list], text)
    #     if actionIndex is not None:
    #         self.action_list.pop(actionIndex)


class ZzControls:
    class _C:
        def __init__(self, controls):
            self.controls = controls

        def __getattr__(self, name):
            for line in self.controls.controls:
                if line.get("name") == name or line.get("tag") == name:
                    return line
            return [line["name"] for line in self.controls.controls]

    def __init__(self):
        self.controls = []
        self.c = self._C(self)

    def add_control(
        self,
        name="",
        label="",
        gridlabel="",
        control="",
        pic="",
        data="",
        actions=[],
        valid=None,
        readonly=None,
        disabled=None,
        check=None,
        form_only=None,
        grid_only=None,
        when=None,
        widget=None,
        mess="",
        tag="",
        eat_enter=None,
        hotkey="",
    ):
        self.controls.append(
            {
                "name": name,
                "label": label,
                "gridlabel": gridlabel,
                "control": control,
                "pic": pic,
                "data": data,
                "actions": actions,
                "readonly": readonly,
                "disabled": disabled,
                "check": check,
                "form_only": form_only,
                "grid_only": grid_only,
                "valid": valid,
                "when": when,
                "widget": widget,
                "mess": mess,
                "eat_enter": eat_enter,
                "tag": tag,
                "hotkey": hotkey,
            }
        )
        return True


class ZzSettings:
    def __init__(self, filename=""):
        self.filename = filename if filename else "zzGui.ini"
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
        self.heap = ZzHeap()
        self.style_file = ""
        self.settings_file = ""

        self.style_file = self.get_argv("style")
        if self.style_file == "":
            self.style_file = "zzGui.css"
        self.settings_file = self.get_argv("ini")

        self.set_style()

        self.settings = ZzSettings(self.settings_file)
        self.main_window = ZzMainWindow(title)
        self.menu_list = []
        self.main_window.restore_geometry(self.settings)
        self.on_init()

        self.main_window.show()

    def set_style(self):
        pass

    def get_argv(self, argtext: str):
        for x in sys.argv:
            if x.startswith(f"/{argtext}:") or x.startswith(f"-{argtext}:"):
                file_name = x[(len(argtext) + 2):]
                print(file_name)
                return file_name
        return ""

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
        tmp_list = [x["TEXT"] for x in menu]
        tmp_dict = {x["TEXT"]: x for x in menu}
        re_ordered_list = []
        for x in tmp_list:
            # add node element for menu
            menu_node = "|".join(x.split("|")[:-1])
            if menu_node not in re_ordered_list:
                re_ordered_list.append(menu_node)
                tmp_dict[menu_node] = {
                    "TEXT": menu_node,
                    "WORKER": None,
                    "BEFORE": None,
                    "TOOLBAR": None,
                }
            if tmp_dict[x].get("BEFORE") in re_ordered_list:
                re_ordered_list.insert(
                    re_ordered_list.index(tmp_dict[x].get("BEFORE")), x
                )
            else:
                re_ordered_list.append(x)
        return [tmp_dict[x] for x in re_ordered_list]

    def close(self):
        self.main_window.save_geometry(self.settings)
        self.main_window.close()
        sys.exit(0)

    def show_statusbar_mess(self, text=""):
        pass

    def show_form(self, form=None, modal="modal"):
        pass

    def focus_widget(self):
        pass

    def lock(self):
        pass

    def unlock(self):
        pass

    def process_events(self):
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

    def disable_toolbar(self, mode=True):
        pass

    def disable_menubar(self, mode=True):
        pass

    def disable_tabbar(self, mode=True):
        pass

    def show_tabbar(self, mode=True):
        pass

    def get_tabbar_text(self):
        pass

    def set_tabbar_text(self, text=""):
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
        self.build_menu()
        self.on_start()


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

    # def zz_layout(self):
    #     pass

    # def _run(self):
    #     self.restore_geometry(self.settings)
    #     self.build_menu()
    #     self.show_menubar(True)
    #     self.on_start()
    #     return self

    def show(self):
        pass

    # def _close(self):
    #     self.save_geometry(self.settings)

    # def _on_init(self):
    #     pass

    def on_start(self):
        pass
