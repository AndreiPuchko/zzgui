# The light Python GUI builder (currently based on PyQT5)

# Less than 200 lines GUI app:
 ---
```python
from zzgui.zz_qt5.app import ZzApp as ZzApp
from zzgui.zz_qt5.form import ZzForm as ZzForm

import zzgui.zzdialog
from zzgui.zzdialog import zzMess

zzgui.zzdialog.ZzForm = ZzForm


class DemoApp(ZzApp):
    def on_start(self):
        self.show_form3()

    def on_init(self):
        self.add_menu("File|First", self.show_form1, toolbar="First")
        self.add_menu("File|Second", self.show_form2, toolbar="First")
        self.add_menu("File|Complex", self.show_form3, toolbar="First")
        self.add_menu("File|Grid", self.worker)
        self.add_menu("File|-")
        self.add_menu(
            "File|Options|Toogle toolbar", self.show_hide_toolbar, toolbar="tb"
        )
        self.add_menu(
            "File|Options|Toogle menubar", self.show_hide_menubar, toolbar="tb"
        )
        self.add_menu("File|Options|Toogle tabbar", self.show_hide_tabbar, toolbar="tb")
        self.add_menu(
            "File|Options|Toogle statusbar", self.show_hide_statusbar, toolbar="tb"
        )
        self.add_menu("File|-")
        self.add_menu("File|Quit", self.close, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("Documents|Personal")
        self.add_menu("Documents|Business")
        self.add_menu("Help|About", lambda: zzMess("About zzgui"))

    def describe_form1(self):
        form = ZzForm("First form")
        form.add_control("/f")
        form.add_control("uid", "Uid", control="line")
        form.add_control("name", "Name", control="line", data="First Name")
        form.add_control("birthdate", "", control="date", data="1990-05-01")
        form.add_control("/")
        form.add_control("/h")
        form.add_control("/s")
        form.add_control(
            "",
            "Greet me",
            control="button",
            valid=lambda: zzMess(f"{form.s.name}-{form.s.birthdate}"),
        )
        form.add_control("", "Close", control="button", valid=lambda: form.close())
        form.add_control("/")
        return form

    def show_form1(self):
        form = self.describe_form1()
        form.get_form_widget().show_form()
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
        form = self.describe_form2()
        form.get_form_widget().show_form()
        print(form.s.name)

    def describe_form3(self):
        form = ZzForm("Complex form")
        form.add_control("/h")
        form.add_control("", "1", control="form", widget=self.describe_form1())
        form.add_control("/v")
        f1 = self.describe_form2()
        f2 = self.describe_form2()
        form.add_control("", "2", control="form", widget=f1)
        form.add_control("", "3", control="form", widget=f2)
        return form

    def show_form3(self):
        form = self.describe_form3()
        form.get_form_widget().show_form()

    def show_hide_menubar(self):
        self.show_menubar(not self.is_menubar_visible())

    def show_hide_toolbar(self):
        self.show_toolbar(not self.is_toolbar_visible())

    def show_hide_tabbar(self):
        self.show_tabbar(not self.is_tabbar_visible())

    def show_hide_statusbar(self):
        self.show_statusbar(not self.is_statusbar_visible())

    def worker(self):
        print(self.main_window.menuBar().actions())
        print(123)


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()

```