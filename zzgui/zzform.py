if __name__ == "__main__":
    import sys

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
        frame_list = [self]
        for meta in self.controls:
            if meta.get("noform", ""):
                continue

            current_frame = frame_list[-1]
            label2add, widget2add = self.widget(meta)

            if current_frame.frame_mode == "f":
                current_frame.add_row(label2add, widget2add)
            else:
                if label2add:
                    current_frame.add_widget(label2add)
                if widget2add:
                    current_frame.add_widget(widget2add)
            if meta.get("name", "") == ("/s"):
                continue
            if meta.get("name", "").startswith("/"):
                if len(meta.get("name", "")) == 1:
                    frame_list.pop()
                else:
                    frame_list.append(widget2add)

        zzapp.zz_app.show_form(self, modal)

    def close(self):
        self.save_geometry(zzapp.zz_app.settings)

    def widget(self, meta):
        control = meta.get("control", "line" if meta.get("name") else "label")
        if control == "":
            control = "label"
        name = meta.get("name", "")
        label = meta.get("label", "")
        class_name = ""

        widget2add = None
        if label and control not in ("button", "toolbutton", "frame", "label"):
            label2add = self._get_widget("label")(meta)
        else:
            label2add = None

        if name[:2] in ("/h", "/v", "/f"):
            control = "frames"
            class_name = "frame"
        elif "radio" in name:
            control = "radio"
        elif name == "/s":
            control = "space"

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
        return getattr(getattr(self._widgets_package, module_name), class_name)
        # try:
        #     return getattr(getattr(self._widgets_package, module_name), class_name)
        # except Exception:
        #     return getattr(getattr(self._widgets_package, "label"), "label")

    def add_control(
        self,
        name="",
        label="",
        control="",
        pic="",
        data="",
        valid=None,
        when=None,
    ):
        self.controls.append(
            {
                "name": name,
                "label": label,
                "control": control,
                "pic": pic,
                "data": data,
                "valid": valid,
                "when": when,
            }
        )
        return True
