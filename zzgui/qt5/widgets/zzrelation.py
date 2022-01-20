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
        self.to_form = None
        if self.meta.get("to_form"):
            self.to_form: ZzForm = self.meta.get("to_form")()

        self.add_widget(self.get)
        self.add_widget(self.button)
        self.add_widget(self.say)
        self.get_valid()

    def show_related_form(self):
        if isinstance(self.to_form, ZzForm):
            # if not self.formTo.isAction("Select"):
            #     self.formTo.addAction("Select",self.showRelatedFormResult,key="Enter",tag="select")
            self.to_form.add_action(
                "Select", self.show_related_form_result, hotkey="Enter", tag="select"
            )

            def seek():
                row = self.to_form.model.cursor.seek_row(
                    {self.meta["to_column"]: self.get_text()}
                )
                self.to_form.set_grid_index(row)

            self.to_form._after_grid_create = seek

            self.to_form.show_mdi_modal_grid()

    def show_related_form_result(self):
        if self.to_form:
            self.get.set_text(self.to_form.r.__getattr__(self.meta["to_column"]))
            self.to_form.close()
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
        # if self.to_form:
        #     rel = self.to_form.model.get_related(
        #         self.meta["to_table"],
        #         f"{self.meta['to_column']} = '{self.get.text()}'",
        #         self.meta["related"],
        #     )
        # else:
        #     rel = "...relation not defined..."
        rel = self.meta["form"].model._get_related(
            self.get.text(), self.meta, do_not_show_value=1, reset_cache=1
        )
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
