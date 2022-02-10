"""shows
defining the main menu and toolbar shortcuts
the possibilities for creating complex user interface forms
managing main window appearance
"""
from zzgui import zzapp
from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess
from zzgui.zzapp import ZzActions
from zzgui.zzdialogs import zzAskYN


class DemoApp(ZzApp):
    def on_start(self):
        self.first_form()

    def on_init(self):
        self.add_menu("File|First", self.first_form, toolbar="*")
        self.add_menu("File|-", None)
        self.add_menu("File|Toogle toolbar", self.show_hide_toolbar, toolbar="*")
        self.add_menu("File|Toogle menubar", self.show_hide_menubar, toolbar="*")
        self.add_menu("File|Toogle tabbar", self.show_hide_tabbar, toolbar="*")
        self.add_menu("File|Toogle statusbar", self.show_hide_statusbar, toolbar="*")
        self.add_menu("File|-", None)
        self.add_menu("Documents|Personal", None)
        self.add_menu("Documents|Business", None)
        self.add_menu("Help|About", lambda: zzMess("About zzgui"))
        self.add_menu("File|Quit", self.close, toolbar="*")

    def first_form(self):
        form = ZzForm("First form ever")
        form.add_control("/")
        actions = ZzActions()
        # actions.show_main_button = False
        # actions.show_actions = False
        actions.add_action(
            text="Action 1",
            worker=lambda: zzMess(
                "I am the Action 1.<br><br>"
                "<font color=red>You can reach me also with </font>"
                "<font size=+5 color=darkblue>mouse <b>left click</b>!</font>"
            ),
            mess="I am the Action! Click Me",
        )

        def action2():
            form.s.name = form.s.name + "+0"
            form.w.name.set_focus()
            zzapp.zz_app.show_statusbar_mess("Text in status bar")
            zzMess(
                "Ich bin <b>Action zwei</b><br><br>"
                "<font size=+2 color=green>Look,"
                "I have changed 'Enter your name' field</b></font><br>"
                "and set focus to it<br>"
                "And there is a text in the statusbar"
            )

        actions.add_action("Action 2", worker=action2)

        form.add_control("toolbar", "", actions=actions, control="toolbar", mess="Form's actions")
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
            data="FirstName LastName",
            mess="You can do it!",
        )

        if form.add_control("/t", "Tab1"):
            form.add_control("/hs")
            form.add_control(
                "",
                "Just a multiline label on tab1.<br>"
                "<b>Look</b>,"
                "This tab has a splitter! <b><br>"
                "The splitter has a <font color=red>memory!</b>",
            )
            form.add_control("spin1", "Spinbox", control="spin")
            form.add_control("/s")
            form.add_control(name="z1", label="Enter smths", control="line")

        if form.add_control("/t", "Tab2"):
            form.add_control("", "Just label on Tab2")
        form.add_control("/")

        if form.add_control("/t", "Tab3"):
            if form.add_control("/h"):
                form.add_control("", "Label on tab3")
                form.add_control("z1", "Decimal input", datatype="dec", datalen=15, datadec=2, pic="F")
                form.add_control("/s")
                form.add_control("/")

        if form.add_control("/t", "Tab4"):
            form.add_control("", "2222222222222222222")
        form.add_control("/")

        if form.add_control(name="/h", label="Horizontal frame"):

            if form.add_control(name="/vs", label="Vertical frame has a splitter too"):
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
                    "Radio buttons",
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

                form.add_control("f1", label="F1", control="line", data="f1 label content")
                form.add_control("f2", label="F2", control="line", data="f2 label content")
                form.add_control("bdate", label="Birthday", control="date", data="2011-01-15")
            form.add_control("/")
        form.add_control("/")

        form.add_control(
            name="text",
            label="Enter big text",
            control="text",
            data="simple <b>text<br>line2",
            mess="Input for big amount of text<br>"
            "Like <b><font color=red>War</font> and"
            " <font color=green>Peace</font></b>,"
            "<br> for example",
        )

        if form.add_control("/h", "ToolButtons"):
            form.add_control(
                label="toolbutton\nI can show value of focus widget",
                control="toolbutton",
                valid=lambda: zzMess(f"{self.focus_widget().get_text()}"),
            )

            def close_form():
                if zzAskYN("<b><font size=+3 color=darkred>Are you sure?") == 2:
                    form.close()

            form.add_control(
                label="I can close the form",
                control="toolbutton",
                valid=close_form,
            )
            form.add_control("/s")
            form.add_ok_cancel_buttons()
            form.system_controls.c._ok_button["label"] = "I am a system button,\ni have been renamed"

            form.valid = (
                lambda: zzAskYN("<font color=darkcyan size=+4>" "Are you really want to close ME?") == 2
            )
        form.add_control("/")

        form.show_mdi_modal_form()

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
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
