from click import launch
from zzgui.qt5.zzapp import ZzApp
from zzgui import zzapp
from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess
from zzgui.zzapp import ZzActions
from zzgui.zzdialogs import zzAskYN


class DemoApp(ZzApp):
    def on_start(self):
        self.hide_tabbar()
        self.hide_statusbar
        self.hide_menubar()
        self.define_launch_data()
        self.first_form()

    def first_form(self):
        self.form = ZzForm("Launch demo")
        self.form.add_control("/")
        if self.form.add_control("/v"):
            if self.form.add_control("/h"):
                self.form.add_control(
                    "app_list",
                    "",
                    control="list",
                    pic=";".join(self.launch_data.keys()),
                    valid=self.set_description,
                )
                if self.form.add_control("/v"):
                    self.form.add_control("descr", "Description", control="text", readonly=1)
                    self.form.add_control("/")
                self.form.add_control("/")
        self.form.add_control("/h")
        self.form.add_control("/s")
        self.form.add_control("run", "Run", control="button")
        self.form.add_control("/s")
        self.form.add_control("quit", "Quit", control="button", valid=self.close)
        self.form.add_control("/s")
        self.form.run()

    def define_launch_data(self):
        self.launch_data = {
            "Common widgets": {
                "text": "dlkgj sdl g;ksd",
                "py": "demo/demo_01.py",
            },
            "Main window management": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo/demo_01.py",
            },
        }

    def set_description(self):
        print(12)


def test():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    test()
