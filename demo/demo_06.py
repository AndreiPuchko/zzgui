if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")


from zzgui.qt5.zzapp import ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess


class firstApp(ZzApp):
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
        form.add_control("", "First Label")
        form.add_control("field", "First Field")
        form.add_control("", "Close Form", control="button", valid=form.close)
        form.show_mdi_modal_form()


def demo():
    app = firstApp("zzgui - the first app")
    app.run()


if __name__ == "__main__":
    demo()
