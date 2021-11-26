"""Shows the possibilities of combining several forms into one
"""
if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess

from zzgui.zzutils import num


class DemoApp(ZzApp):
    def on_start(self):
        self.show_complex_form()

    def on_init(self):
        self.add_menu("File|First", self.show_form1, toolbar="*")
        self.add_menu("File|Second", self.show_form2, toolbar="*")
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|Complex", self.show_complex_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("File|Options|Toogle toolbar", self.show_hide_toolbar)
        self.add_menu("File|Options|Toogle menubar", self.show_hide_menubar)
        self.add_menu("File|Options|Toogle tabbar", self.show_hide_tabbar)
        self.add_menu("File|Options|Toogle statusbar", self.show_hide_statusbar)
        self.add_menu("File|-")
        self.add_menu("Documents|Personal")
        self.add_menu("Documents|Business")
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")
        self.add_menu("File|Quit", self.close, toolbar="*")

    def describe_form1(self):
        form = ZzForm("First form")
        form.add_control("/f")
        form.add_control("uid", "Uid", control="line", data=1)
        if form.add_control("/h"):

            def add_id():
                form.s.uid = num(form.s.uid) + 1

            def sub_id():
                form.s.uid = num(form.s.uid) - 1

            form.add_control("", "+", control="toolbutton", valid=add_id)
            form.add_control("", "-", control="toolbutton", valid=sub_id)
            form.add_control("/")

        form.add_control("/s")
        form.add_control("name", "Name", control="line", data="First Name")
        form.add_control("birthdate", "", control="date", data="1990-05-01")
        form.add_control("/")
        form.add_control("/h")
        form.add_control("/s")

        form.add_control(
            "",
            "Greet me",
            control="button",
            valid=lambda: zzMess(f"{form.s.name}: {form.s.birthdate}"),
        )
        form.add_control("", "Close", control="button", valid=lambda: form.close())
        form.add_control("/")
        return form

    def show_form1(self):
        form = self.describe_form1()
        form.show_mdi_modal_form()
        print(form.s.name)

    def describe_form2(self):
        form = ZzForm("Second form")
        form.add_control("/f")
        form.add_control(
            "radio", "Color", pic="Red;White;Black", control="radio", data="2"
        )
        form.add_control(
            "check", "Transparency", pic="Transparency", control="check", data=""
        )
        form.add_control("combo", "Popup List", control="combo", pic="Oprion1;Option2")
        form.add_control("/")
        form.add_control("/h")
        form.add_control("/s")
        form.add_control(
            "",
            "Greet me",
            control="button",
            valid=lambda: zzMess(f"{form.s.name}-{form.s.birthdate}"),
        )

        def close_form():
            form.close()

        form.add_control("", "Close", control="button", valid=close_form)
        form.add_control("/")
        return form

    def show_form2(self):
        self.describe_form2().show_mdi_modal_form()

    def describe_complex_form(self):
        form = ZzForm("Complex form")
        form.add_control("/h")
        form.add_control("", "1", widget=self.describe_form1())
        form.add_control("/v")
        f1 = self.describe_form2()
        f2 = self.describe_form2()
        form.add_control("", "2", widget=f1)
        form.add_control("", "3", widget=f2)
        form.add_control("/")
        form.add_control("/")
        form.add_control("", "4", widget=self.describe_grid_form().get_grid_widget())

        return form

    def show_complex_form(self):
        self.describe_complex_form().show_mdi_modal_form()

    def describe_form4(self):
        form = ZzForm("Grid form")
        form.actions.add_action("New", lambda: zzMess("New"))
        form.actions.add_action("Edit|1", lambda: zzMess("Edit"))
        form.actions.add_action("Edit|2", lambda: zzMess("Edit"))
        form.actions.add_action("Nt", lambda: zzMess("Nt"))
        form.actions.add_action("Edit|3", lambda: zzMess("Edit"))
        form.add_control("uid", "Uid", control="line")
        form.add_control("name", "Name", control="line", data="First Name")
        form.add_control("date", "Date of bith", control="date", data="1990-05-01")
        return form

    def describe_grid_form(self):
        data = [
            {"uid": 1, "name": "Lorem Ipsum", "date": "2005-01-15"},
            {"uid": 2, "name": "Dolor Sit", "date": "2005-01-15"},
            {"uid": 3, "name": "Quis autem", "date": "2005-01-15"},
            {"uid": 4, "name": "Iron nagel", "date": "2005-01-15"},
        ]
        form = self.describe_form4()
        form.model.set_records(data)
        return form

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()

    def show_hide_menubar(self):
        self.show_menubar(not self.is_menubar_visible())

    def show_hide_toolbar(self):
        self.show_toolbar(not self.is_toolbar_visible())

    def show_hide_tabbar(self):
        self.show_tabbar(not self.is_tabbar_visible())

    def show_hide_statusbar(self):
        self.show_statusbar(not self.is_statusbar_visible())


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
