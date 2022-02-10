if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.qt5.zzapp import ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
import imp


class DemoApp(ZzApp):
    def on_init(self):
        self.hide_tabbar()
        self.hide_statusbar()
        self.hide_menubar()
        self.define_launch_data()

    def on_new_tab(self):
        self.first_form()
        self.close()

    def first_form(self):
        self.form = ZzForm("Launch demo")
        self.form.maximized = True
        self.form.hide_title = True
        self.form.set_style_sheet(
            "QWidget{font:20px;} zzbutton {font:30px; padding: 10 100px} zzlist::item {margin: 10px;}"
        )
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
                    self.form.add_control(
                        "description", "Description", control="text", readonly=1, disabled=1
                    )
                    self.form.add_control("/")
                self.form.add_control("/")
        self.form.add_control("/h")
        self.form.add_control("/s")
        self.form.add_control("run", "Run", control="button", valid=self.launcher)
        self.form.add_control("/s")
        self.form.add_control("quit", "Quit", control="button", valid=self.close)
        self.form.add_control("/s")
        self.form.after_form_show = self.after_form_show
        self.form.run()

    def launcher(self):
        py = self.launch_data[self.form.s.app_list]["py"]
        f, filename, description = imp.find_module(py, ["demo"])
        mo = imp.load_module("demo", f, filename, description)
        mo.DemoApp().run()
        mo = None

    def after_form_show(self):
        self.form.w.run.set_style_sheet("{background-color:lightblue}")
        self.form.w.quit.set_style_sheet("{background-color:pink}")

        self.form.w.app_list.set_text(list(self.launch_data.keys())[0])
        # self.form.w.app_list.set_focus()

    def define_launch_data(self):
        self.launch_data = {
            "Common widgets": {
                "text": """
                """,
                "py": "demo_01",
            },
            "Main window management": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_02",
            },
            "Grid (CSV)": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_03",
            },
            "progressbar": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_04",
            },
            "non modal form": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_05",
            },
            "Code editor": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_06",
            },
            "Database App 1": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_07",
            },
            "Database App 2": {
                "text": "dslkg ;skld g;ksd ;kgs",
                "py": "demo_08",
            },
        }

    def set_description(self):
        self.form.s.description = self.launch_data[self.form.s.app_list]["text"]


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
