if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zzapp as zzapp


class ZzForm:
    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.controls = []
        self.actions = zzapp.ZzAction()
        self.form_stack = []

    def close(self):
        if self.form_stack:
            form_window = self.form_stack.pop()
            form_window.close()
            print("close")

    def show_dialog(self, title="", modal=""):
        self.get_form_widget().show_form(title, modal)
        # ZzFormWindow(self).show_form(modal=modal)

    def show_mdi_modal_dialog(self, title=""):
        self.get_form_widget().show_form(title, "modal")
        # ZzFormWindow(self).show_form("modal")

    def show_app_modal_dialog(self, title=""):
        self.get_form_widget().show_form(title, modal="super")
        # ZzFormWindow(self).show_form(title, modal="super")

    def get_form_widget(self):
        # Must to be copied into any child class
        form_widget = ZzFormWindow(self)
        form_widget.build_form()
        return form_widget

    def add_control(
        self,
        name="",
        label="",
        control="",
        pic="",
        data="",
        actions=[],
        valid=None,
        readonly=None,
        when=None,
    ):
        self.controls.append(
            {
                "name": name,
                "label": label,
                "control": control,
                "pic": pic,
                "data": data,
                "actions": actions,
                "readonly": readonly,
                "valid": valid,
                "when": when,
            }
        )
        return True


class ZzFormWindow:
    def __init__(self, zz_form: ZzForm):
        super().__init__()
        self.shown = False
        self.zz_form = zz_form
        self.zz_form.form_stack.append(self)
        self.title = ""
        # self.controls = []
        self.widgets = {}
        self.tab_widget = None
        self._widgets_package = None
        self.escapeEnabled = True
        self.mode = "form"
        self.prev_form = None

    def build_form(self):
        frame_stack = [self]
        tmp_frame = None
        for meta in self.zz_form.controls:
            # print(frame_list)
            if meta.get("noform", ""):
                continue

            current_frame = frame_stack[-1]

            # do not add widget if it is not first tabpage on the form
            if not (meta.get("name", "") == ("/t") and self.tab_widget is not None):
                label2add, widget2add = self.widget(meta)
                if current_frame.frame_mode == "f":
                    current_frame.add_row(label2add, widget2add)
                else:
                    if label2add is not None:
                        current_frame.add_widget(label2add)
                    if widget2add is not None:
                        current_frame.add_widget(widget2add)
            # If tabpage widget
            if meta.get("name", "") == ("/t"):
                if self.tab_widget is None:
                    self.tab_widget = widget2add
                    frame_stack.append(widget2add)
                else:
                    if tmp_frame in frame_stack:
                        frame_stack = frame_stack[: frame_stack.index(tmp_frame)]
                tmp_frame = self.widget({"name": "/v"})[1]
                self.tab_widget.addTab(tmp_frame, meta.get("label", ""))
                frame_stack.append(tmp_frame)
            elif meta.get("name", "") == ("/s"):
                continue
            elif meta.get("name", "") == "/":
                if len(frame_stack) > 1:
                    frame_stack.pop()
                    # Remove tab widget if it is at the end of stack
                    if "tab.tab" in f"{type(frame_stack[-1])}":
                        self.tab_widget = None
                        frame_stack.pop()
            elif meta.get("name", "").startswith("/"):
                frame_stack.append(widget2add)
        # Make it work never more 
        self.build_form = lambda: None

    def show_form(self, title="", modal="modal"):
        self.build_form()
        self.title = title if title else self.zz_form.title
        zzapp.zz_app.set_tabbar_text(self.zz_form.title)
        zzapp.zz_app.show_form(self, modal)

    def close(self):
        # print (self.prev_form)
        if self.prev_form:
            zzapp.zz_app.set_tabbar_text(self.prev_form.title)
        else:
            zzapp.zz_app.set_tabbar_text("=")
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
        elif "/t" in name:
            control = "tab"
        elif "radio" in control:
            control = "radio"
        elif "toolbar" in control:
            control = "toolbar"
        elif name == "/s":
            control = "space"

        widget_class = self._get_widget(control, class_name)

        if widget_class:
            widget2add = widget_class(meta)

        if hasattr(widget2add, "label"):
            widget2add.label = label2add

        # self.widgets[name] = widget2add
        return label2add, widget2add

    def _get_widget(self, module_name, class_name=""):
        """
        for given name returns class from current GUI engine module
        """
        if class_name == "":
            class_name = module_name
        # return getattr(getattr(self._widgets_package, module_name), class_name)
        try:
            return getattr(getattr(self._widgets_package, module_name), class_name)
        except Exception:
            return getattr(getattr(self._widgets_package, "label"), "label")
