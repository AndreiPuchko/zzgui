if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from zzgui.zzwindow import ZzWindow
import zzgui.zzapp as zzapp

FRAMECONTROLS = {"/h": 1}


class ZzForm(ZzWindow):
    def __init__(self, title=""):
        super().__init__(title=title)
        self.shown = False
        self.controls = []
        self.widgets = {}
        self._widgets_package = None

    def show_form(self, modal="modal"):
        frame_list = [self]
        for meta in self.controls:
            if meta.get("noform", ""):
                continue

            current_frame = frame_list[-1]
            label2add, widget2add = self.widget(meta)

            if current_frame.frame_mode == "f":
                current_frame.addRow(label2add, widget2add)
            else:
                if label2add:
                    current_frame.add_widget(label2add)
                if widget2add:
                    current_frame.add_widget(widget2add)
            if meta.get("name", "").startswith("/"):
                if len(meta.get("name", "")) == 1:
                    frame_list.pop()
                else:
                    frame_list.append(widget2add)

        zzapp.zz_app.show_form(self, modal)

    def close(self):
        self.save_geometry(zzapp.zz_app.settings)

    def widget(self, meta):
        control = meta.get("control", "label")
        if control == "":
            control = "label"
        name = meta.get("name", "")
        label = meta.get("label", "")
        class_name = ""

        widget2add = None
        if label and control != "label":
            label2add = self._get_widget("label")(meta)
        else:
            label2add = None

        if name[:2] == "/h":
            control = "frames"
            class_name = "frame"

        widget_class = self._get_widget(control, class_name)

        if widget_class:
            widget2add = widget_class(meta)

        if hasattr(widget2add, "label"):
            widget2add.label = label2add

        self.widgets[name] = widget2add
        return label2add, widget2add

    def _get_widget(self, module_name, class_name=""):
        """
        for given name returns class from current GUI engine module
        """
        if class_name == "":
            class_name = module_name
        try:
            return getattr(getattr(self._widgets_package, module_name), class_name)
        except Exception:
            return getattr(getattr(self._widgets_package, "label"), "label")

    def add_control(
        self,
        name="",
        label="",
        control="",
        data="",
    ):
        self.controls.append(
            {
                "name": name,
                "label": label,
                "control": control,
                "data": data,
            }
        )
        return True
