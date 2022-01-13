import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QFrame

from zzgui.zzform import ZzForm
from zzgui.zzutils import num
from zzgui.qt5.zzwidget import ZzWidget
from zzgui.qt5.zzwindow import ZzFrame
from zzgui.qt5.widgets.zzline import zzline
from zzgui.qt5.widgets.zzbutton import zzbutton


class zzrelation(QFrame, ZzWidget, ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        ZzFrame.__init__(self, "h")
        self.meta = meta
        meta["valid"] = self.get_valid

        self.get = zzline(meta)
        self.button = zzbutton(
            {"label": "?", "datalen": 3, "valid": self.show_related_form}
        )
        self.say = zzline({"disabled": "*"})
        self.add_widget(self.get)
        self.add_widget(self.button)
        self.add_widget(self.say)
        self.get_valid()

    def show_related_form(self):
        self.form_to: ZzForm = self.meta.get("to_form")
        if isinstance(self.form_to, ZzForm):
            # if not self.formTo.isAction("Select"):
            #     self.formTo.addAction("Select",self.showRelatedFormResult,key="Enter",tag="select")
            self.form_to.add_action(
                "Select", self.show_related_form_result, hotkey="Enter", tag="select"
            )

            # self.form_to.addSelectGridAction(self.showRelatedFormResult)

            # def beforeStart():
            #     row = self.form_to.model.cursor.getPkRow(
            #         {self.meta["to_field"]: self.get.text()}
            #     )
            #     if row:
            #         self.form_to.setGridIndex(row)

            # self.form_to.beforeStart = beforeStart

            self.form_to.show_mdi_modal_grid()

    def show_related_form_result(self):
        self.get.setText(self.form_to.r.__getattr__(self.meta["to_column"]))
        self.form_to.close()
        self.get.set_focus()
        self.get_valid()

    def get_valid(self):
        value = self.get.get_text()
        if self.meta.get("num") and num(value) == 0:
            return True
        elif value == "":
            return True
        return self.set_related()

    def set_related(self):
        if self.meta.get("to_form"):
            rel = self.meta.get("to_form").model.get_related(
                self.meta["to_table"],
                f"{self.meta['to_column']} = '{self.get.text()}'",
                self.meta["related"],
            )
        else:
            rel = "...relation not defined..."
        if rel is None:
            self.say.set_text(" wrong key ")
            return False
        else:
            self.say.set_text(rel)
            return True

    def set_text(self, text):
        self.get.set_text(text)
        self.get_valid()

    def get_text(self):
        return self.get.get_text()
