if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.zz_qt5.app import ZzApp as ZzApp
from zzgui.zz_qt5.form import ZzForm as ZzForm


def zzMess(mess="", title="Message", html=1):
    form = ZzForm(title)
    form.add_control("mess", control="text", data=f"{mess}")

    if form.add_control("/h"):
        form.add_control("/s")
        form.add_control(
            "close",
            "Ok",
            control="button",
            valid=form.close,
        )
        form.add_control("/s")
        form.add_control("/")
    form.show_form("super")


class Demo_app(ZzApp):

    def on_start(self):
        self.first_form()
        zzMess("122")

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
        if form.add_control("/h", "main window control"):
            form.add_control(
                label="Main menu on/off",
                control="toolbutton",
                valid=lambda: self.show_menubar(not self.is_menubar_visible()),
            )
            form.add_control(
                label="Toolbar on/off",
                control="toolbutton",
                valid=lambda: self.show_toolbar(not self.is_toolbar_visible()),
            )
            form.add_control(
                label="Tabbar on/off",
                control="toolbutton",
                valid=lambda: self.show_tabbar(not self.is_tabbar_visible()),
            )
            form.add_control(
                label="Statusbar on/off",
                control="toolbutton",
                valid=self.show_hide_statusbar,
            )
        form.add_control("/")

        form.add_control(name="p1", label="just label", control="label")
        form.add_control(
            name="name",
            label="Enter your name",
            control="line",
            data="simple data",
        )

        if form.add_control(name="/h", label="Horizontal frame"):

            if form.add_control(name="/v", label="Vertical frame"):
                form.add_control(label="just label 1")
                form.add_control(label="just label 2")
                form.add_control(
                    "combo",
                    label="combobox",
                    control="combo",
                    pic="item1;item2;item3",
                )
            form.add_control("/")

            form.add_control("list1", "", pic="item1;item2;item3", control="list")

            if form.add_control(name="/f", label="Form frame"):
                form.add_control(
                    "radio",
                    "Radio buttn",
                    pic="option 1;option 2;option 3",
                    control="radio",
                )
                form.add_control(
                    "check",
                    label="checkbox",
                    pic="checkbox text",
                    control="check",
                    data="*",
                )

                form.add_control("f1", label="F1", control="line")
                form.add_control("f2", label="F2", control="line")
            form.add_control("/")
        form.add_control("/")

        form.add_control(
            name="text",
            label="Enter big text",
            control="text",
            data="simple text<br>line2",
        )

        if form.add_control("/h", "buttons"):
            form.add_control(
                label="tool",
                control="toolbutton",
                valid=lambda: print(self.focusWidget().get_text()),
            )
            form.add_control("/s")
            form.add_control(
                label="Ok",
                control="button",
                valid=lambda: zzMess("3333333333333333"),
            )
            form.add_control(label="Cancel", control="button", valid=form.close)

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
