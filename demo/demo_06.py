if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.qt5.zzapp import ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess


class DemoApp(ZzApp):
    def on_start(self):
        self.first_form()

    def on_init(self):
        self.add_menu("File|About", lambda: zzMess("First application!"), toolbar=1)
        self.add_menu("File|First Form", self.first_form, toolbar=1)
        self.add_menu("File|-")
        self.add_menu("File|Exit", self.close, toolbar=1)
        return super().on_init()

    def first_form(self):
        form = ZzForm("FirstForm")
        form.init_size = [95, 95]
        form.add_control("", "First Label")
        form.add_control("field", "First Field")
        form.add_control("/")
        form.add_control("code", "Text Field", control="codepython")
        form.add_control("/h")

        def open_file():
            file_name = ZzApp.get_open_file_dialoq(filter="Python file(*.py);; Toml file(*.toml *.ini)")[0]
            if file_name:
                form.s.code = open(file_name).read()

        form.add_control("open", "Open file", control="button", valid=open_file)

        form.add_control("/s")
        form.add_control("", "Close Form", control="button", valid=form.close)

        def after_form_show():
            form.s.code = open("zzgui/zzapp.py").read()

        form.after_form_show = after_form_show
        form.run()


def demo():
    app = DemoApp("zzgui - the first app")
    app.run()


if __name__ == "__main__":
    demo()
