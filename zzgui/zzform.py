import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from zzgui.zzwindow import ZzWindow
import zzgui.zzapp as zzapp


class ZzForm(ZzWindow):
    def __init__(self, title=""):
        super().__init__(title=title)
        self.shown = False
        self.controls = []
        self.widgets = {}
        self._widgets_package = None

    def show_form(self, modal="modal"):
        zzapp.zz_app.show_form(self, modal)

    def close(self):
        self.save_geometry(zzapp.zz_app.settings)

    def widget(self, meta):
        control = meta.get("control", "line")
        name = meta.get("name", "")
        label = meta.get("label", "")
        widget2add = None
        if label:
            label2add = self.get_widget("label")(label)
        else:
            label2add = None

        widget_class = self.get_widget(control)
        if widget_class:
            widget2add = widget_class(label)

        if hasattr(widget2add, "label"):
            widget2add.label = label2add

        self.widgets[name] = widget2add
        if control == "label":
            label2add = None
        return label2add, widget2add

    def get_widget(self, name):
        try:
            return getattr(getattr(self._widgets_package, name), name)
        except Exception:
            return getattr(getattr(self._widgets_package, "label"), "label")

    def add_control(
        self,
        name="",
        label="",
        control="",
    ):
        self.controls.append(
            {
                "name": name,
                "label": label,
                "control": control,
            }
        )
