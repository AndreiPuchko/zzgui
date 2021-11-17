if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from zzgui.zz_qt5 import widget, widgets
from zzgui.zz_qt5.widgets import toolbar
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
                print("close!")
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
        # Must to be copied into any child class
        form_widget = ZzFormWindow(self)
        form_widget.build_form()
        return form_widget

    def get_grid_widget(self):
        # Must to be copied into any child class
        grid_widget = ZzFormWindow(self)
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
            }
        )
        return True


class ZzFormWindow:
    def __init__(self, zz_form: ZzForm):
        super().__init__()
        self.shown = False
        self.zz_form = zz_form
        self.title = ""
        # self.meta = {}  # used when form_widget is a part of complex form
        self.widgets = {}
        self.tab_widget = None
        self._widgets_package = None
        self.escapeEnabled = True
        self.mode = "form"
        self.prev_form = None

    def build_grid(self):
        # populate model with columns metadata
        for meta in self.zz_form.controls:
            self.zz_form.model.add_column(meta)

        toolbar_widget = None
        if self.zz_form.actions.action_list:
            widget_class = self._get_widget("toolbar")
            toolbar_widget = widget_class({"actions": self.zz_form.actions, "control": "toolbar"})
            self.add_widget(toolbar_widget)
        widget_class = self._get_widget("grid")
        grid_widget = widget_class(self.zz_form)
        self.add_widget(grid_widget)

        if toolbar_widget:
            toolbar_widget.set_context_menu(grid_widget)

        # Make it work never more
        self.build_grid = lambda: None
        self.build_form = lambda: None

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
        self.build_grid = lambda: None
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
        """
        """
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
        # Special cases
        if name[:2] in ("/h", "/v", "/f"):  # frames
            control = "frames"
            class_name = "frame"
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
            widget2add = widget_class(meta)

        if hasattr(widget2add, "label"):
            widget2add.label = label2add

        self.widgets[name] = widget2add
        return label2add, widget2add

    def _get_widget(self, module_name, class_name=""):
        """For given name returns class from current GUI engine module"""
        if class_name == "":
            class_name = module_name
        # return getattr(getattr(self._widgets_package, module_name), class_name)
        try:
            return getattr(getattr(self._widgets_package, module_name), class_name)
        except Exception:
            return getattr(getattr(self._widgets_package, "label"), "label")


class ZzFormData:
    """Retrieving data from form"""

    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    # def __setattr__(self, name, value):
    #     if name != "form":
    #         w = self.form.dialogForm.widgets.get(name)
    #         if w:
    #             w.setText(value)
    #     else:
    #         self.__dict__[name] = value

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
        # else:
        #     return self.__dict__.get(name, "")
        # else:
        #     return self.form.lastDialogData.get(name, "")
