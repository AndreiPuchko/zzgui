if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.zz_qt5.widgets import ZzQtApp as ZzApp


class Demo_app(ZzApp):

    def on_start(self):
        pass
        # self.hide_toolbar()
        # self.hide_menubar()

    def on_init(self):
        self.add_menu("File|First", self.worker, toolbar="First")
        self.add_menu("File|Second", self.worker, toolbar="First")
        self.add_menu("File|Grid", self.worker, toolbar="Grid")
        self.add_menu("File|Complex", self.worker, toolbar="Complex")
        self.add_menu("File|Show/Hide toolbar", self.show_hide_toolbar, toolbar="spr_cln")
        self.add_menu("File|Hide/Show menubar", self.show_hide_menubar, toolbar="spr_cln")
        self.add_menu("File|MOVE", self.worker, toolbar="M o v e!")
        self.add_menu("File|-", None)
        self.add_menu("Documents|Personal", None)
        self.add_menu("Documents|Business", None)
        self.add_menu("Quit", self.close, toolbar="*")

    def show_hide_menubar(self):
        self.show_menubar(not self.is_menubar_visible())

    def show_hide_toolbar(self):
        self.show_toolbar(not self.is_toolbar_visible())

    def worker(self):
        print(123)


def demo():
    app = Demo_app("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
