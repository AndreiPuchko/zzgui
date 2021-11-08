if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

# from zzgui.zzapp import *
from zzgui.zz_qt5.app import ZzApp as ZzApp
from zzgui.zz_qt5.form import ZzForm as ZzForm


class Demo_app(ZzApp):
    def on_start(self):
        pass
        # self.hide_toolbar()
        # self.hide_menubar()
        self.first_form()

    def on_init(self):
        self.add_menu("File|First", self.first_form, toolbar="First")
        self.add_menu("File|Second", self.worker)
        self.add_menu("File|Grid", self.worker)
        self.add_menu("File|Complex", self.worker)
        self.add_menu("File|-", None)
        self.add_menu("File|Toogle toolbar", self.show_hide_toolbar, toolbar="spr_cln")
        self.add_menu("File|Toogle menubar", self.show_hide_menubar, toolbar="spr_cln")
        self.add_menu("File|Toogle tabbar", self.show_hide_tabbar, toolbar="spr_cln")
        self.add_menu(
            "File|Toogle statusbar", self.show_hide_statusbar, toolbar="spr_cln"
        )
        self.add_menu("File|-", None)
        self.add_menu("File|Quit", self.close, toolbar="*")
        self.add_menu("File|-", None)
        self.add_menu("Documents|Personal", None)
        self.add_menu("Documents|Business", None)
        self.add_menu("Help|About", None)

    def first_form(self):
        form = ZzForm("First form ever")
        form.add_control("p1", "just label", "label")
        form.add_control("name", "Enter your name", "line")
        form.show_form()

    def show_hide_menubar(self):
        self.show_menubar(not self.is_menubar_visible())

    def show_hide_toolbar(self):
        self.show_toolbar(not self.is_toolbar_visible())

    def show_hide_tabbar(self):
        self.show_tabbar(not self.is_tabbar_visible())

    def show_hide_statusbar(self):
        self.show_statusbar(not self.is_statusbar_visible())

    def worker(self):
        print(123)


def demo():
    app = Demo_app("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
