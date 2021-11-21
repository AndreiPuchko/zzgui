if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zzapp as zzapp
from zzgui.zzmodel import ZzModel


class ZzForm:
    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.controls = []
        self.form_stack = []
        self.actions = zzapp.ZzAction()
        self.model = ZzModel()
        self.s = ZzFormData(self)
        # Must be defined in any subclass
        self._ZzFormWindow_class = None

        self._in_close_flag = False
        self.last_closed_form = None

    def close(self):
        if self._in_close_flag:
            return
        self._in_close_flag = True
        if self.form_stack:
            if self.form_stack[-1].escapeEnabled:
                self.last_closed_form = self.form_stack.pop()
                self.last_closed_form.close()
        self._in_close_flag = False

    def show_form(self, title="", modal="modal"):
        self.get_form_widget().show_form(title, modal)

    def show_mdi_form(self, title=""):
        self.get_form_widget().show_form(title, "")

    def show_mdi_modal_form(self, title=""):
        self.get_form_widget().show_form(title, "modal")

    def show_app_modal_form(self, title=""):
        self.get_form_widget().show_form(title, modal="super")

    def show_grid(self, title="", modal=""):
        self.get_grid_widget().show_form(title, modal)

    def show_mdi_grid(self, title=""):
        self.get_grid_widget().show_form(title, modal="")

    def show_mdi_modal_grid(self, title=""):
        self.get_grid_widget().show_form(title, modal="modal")

    def show_app_modal_grid(self, title=""):
        self.get_grid_widget().show_form(title, modal="superl")

    def get_form_widget(self):
        form_widget = self._ZzFormWindow_class(self)
        form_widget.build_form()
        return form_widget

    def get_grid_widget(self):
        grid_widget = self._ZzFormWindow_class(self)
        grid_widget.build_grid()
        return grid_widget

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
        widget=None,
        tag="",
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
                "widget": widget,
                "tag": tag,
            }
        )
        return True


class ZzFormWindow:
    def __init__(self, zz_form: ZzForm):
        super().__init__()
        self.shown = False
        self.zz_form = zz_form
        self.title = ""
        self.widgets = {}
        self.tab_widget = None
        self._widgets_package = None
        self.escapeEnabled = True
        self.mode = "form"

    def build_grid(self):
        # populate model with columns metadata
        for meta in self.zz_form.controls:
            self.zz_form.model.add_column(meta)

        gridForm = ZzForm()
        gridForm.add_control("/vs", actions=self.zz_form.actions, tag="gridsplitter")
        gridForm.add_control("toolbar", control="toolbar", actions=self.zz_form.actions)
        gridForm.add_control("form__grid", control="grid")

        self.build_form(gridForm.controls)

        return

    def build_form(self, controls=[]):
        frame_stack = [self]
        tmp_frame = None
        if controls == []:
            controls = self.zz_form.controls
        for meta in controls:
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
            # If second and more tabpage widget
            if meta.get("name", "") == ("/t"):
                if self.tab_widget is None:
                    self.tab_widget = widget2add
                    frame_stack.append(widget2add)
                else:
                    if tmp_frame in frame_stack:
                        frame_stack = frame_stack[: frame_stack.index(tmp_frame)]
                tmp_frame = self.widget({"name": "/v"})[1]
                self.tab_widget.add_tab(tmp_frame, meta.get("label", ""))
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
        self.build_grid = lambda: None
        self.build_form = lambda: None

    def get_splitters(self):
        return [
            x
            for x in self.widgets.keys()
            if hasattr(self.widgets[x], "splitter")
            and self.widgets[x].splitter is not None
        ]

    def show_form(self, title="", modal="modal"):
        self.build_form()
        self.title = title if title else self.zz_form.title
        # Restore splitters sizes
        for x in self.get_splitters():
            sizes = zzapp.zz_app.settings.get(
                self.window_title,
                f"splitter-{x}",
                "",
            )
            self.widgets[x].splitter.set_sizes(sizes)
        # Restore grid columns sizes
        if "form__grid" in self.widgets:
            col_settings = {}
            for x in self.zz_form.model.headers:
                data = zzapp.zz_app.settings.get(
                    self.window_title, f"grid_column-'{x}'"
                )
                col_settings[x] = data
            self.widgets["form__grid"].set_column_settings(col_settings)

        zzapp.zz_app.show_form(self, modal)

    def close(self):
        # Splitters sizes
        for x in self.get_splitters():
            zzapp.zz_app.settings.set(
                self.window_title,
                f"splitter-{x}",
                self.widgets[x].splitter.get_sizes(),
            )
        # Grid columns
        if "form__grid" in self.widgets:
            for x in self.widgets["form__grid"].get_columns_settings():
                zzapp.zz_app.settings.set(
                    self.window_title,
                    f"grid_column-'{x['name']}'",
                    x["data"],
                )
        self.save_geometry(zzapp.zz_app.settings)

    def widget(self, meta):
        """Widgets fabric"""
        if not meta.get("control"):
            if meta.get("widget"):
                control = "widget"
            else:
                control = "line" if meta.get("name") else "label"
        else:
            control = meta.get("control")
        if control == "":
            control = "label"
        name = meta.get("name", "")
        label = meta.get("label", "")
        class_name = ""

        widget2add = None
        if label and control not in ("button", "toolbutton", "frame", "label", "check"):
            label2add = self._get_widget("label")(meta)
        else:
            label2add = None
        # Forms and widgets
        if control == "widget":
            if isinstance(meta.get("widget"), ZzForm):
                widget2add = meta.get("widget").get_form_widget()
            else:
                widget2add = meta.get("widget")
            return label2add, widget2add
        else:
            # Special cases
            if name[:2] in ("/h", "/v", "/f"):  # frame
                control = "frame"
                class_name = "frame"
                label2add = None
            elif "/" == name:
                return None, None
            elif "/t" in name:  # Tabpage
                control = "tab"
            elif "radio" in control:
                control = "radio"
            elif "toolbar" in control:
                control = "toolbar"
            elif name == "/s":
                control = "space"

            widget_class = self._get_widget(control, class_name)

            if widget_class:
                if control == "grid":
                    widget2add = widget_class(self.zz_form)
                else:
                    widget2add = widget_class(meta)

            if hasattr(widget2add, "label"):
                widget2add.label = label2add

        self.widgets[meta.get("tag", "") if meta.get("tag", "") else name] = widget2add
        return label2add, widget2add

    def _get_widget(self, module_name, class_name=""):
        """For given name returns class from current GUI engine module"""
        if class_name == "":
            class_name = module_name
        # return getattr(getattr(self._widgets_package, module_name), class_name)
        module_name = f"zz{module_name}"
        class_name = f"zz{class_name}"
        try:
            return getattr(getattr(self._widgets_package, module_name), class_name)
        except Exception:
            return getattr(getattr(self._widgets_package, "zzlabel"), "zzlabel")


class ZzFormData:
    """Get and put data from/to form"""

    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    def __setattr__(self, name, value):
        if name != "zz_form":
            w = self.zz_form.form_stack[-1].widgets.get(name)
            if w:
                w.set_text(value)
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if self.zz_form.form_stack == []:
            if self.zz_form.last_closed_form is None:
                return None
            else:
                widget = self.zz_form.last_closed_form.widgets.get(name)
        else:
            widget = self.zz_form.form_stack[-1].widgets.get(name)
        if widget is not None:
            return widget.get_text()
