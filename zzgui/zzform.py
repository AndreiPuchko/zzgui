if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zzapp as zzapp
from zzgui.zzmodel import ZzModel

VIEW = "VIEW"
NEW = "NEW"
COPY = "COPY"
EDIT = "EDIT"


class ZzForm:
    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.form_stack = []
        self.actions = zzapp.ZzActions()
        self.controls = zzapp.ZzControls()
        self.model = ZzModel()
        self.s = ZzFormData(self)
        self.w = ZzFormWidget(self)
        # Must be defined in any subclass
        self._ZzFormWindow_class = None

        self._in_close_flag = False
        self.last_closed_form = None

        self.crud_form = None
        self.grid_form = None
        self.current_row = 0
        self.current_column = 0

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
        self.get_form_widget(title).show_form(modal)

    def show_mdi_form(self, title=""):
        z = self.get_form_widget(title)
        z.show_form()

    def show_mdi_modal_form(self, title=""):
        form_widget = self.get_form_widget(title)
        form_widget.show_form("modal")

    def show_app_modal_form(self, title=""):
        self.get_form_widget(title).show_form(modal="super")

    def show_grid(self, title="", modal=""):
        self.get_grid_widget(title).show_form(modal)

    def show_mdi_grid(self, title=""):
        self.get_grid_widget(title).show_form(modal="")

    def show_mdi_modal_grid(self, title=""):
        self.get_grid_widget(title).show_form(modal="modal")

    def show_app_modal_grid(self, title=""):
        self.get_grid_widget(title).show_form(modal="superl")

    def get_form_widget(self, title=""):
        form_widget = self._ZzFormWindow_class(self, title)
        form_widget.build_form()
        return form_widget

    def get_grid_widget(self, title=""):
        self.grid_form = self._ZzFormWindow_class(self, title)
        self.grid_form.build_grid()
        return self.grid_form

    def prepare_crud_form_buttons(self, mode):
        crud_form_buttons = zzapp.ZzControls()
        crud_form_buttons.add_control("/")
        crud_form_buttons.add_control("/h", "")
        crud_form_buttons.add_control(
            "_prev_button",
            "<",
            control="button",
            mess="prev record",
            valid=lambda: self.move_crud_view(8),
            disabled=True if mode is not VIEW else False,
            hotkey="PgUp",
        )
        crud_form_buttons.add_control(
            "_next_button",
            ">",
            control="button",
            mess="prev record",
            valid=lambda: self.move_crud_view(2),
            disabled=True if mode is not VIEW else False,
            hotkey="PgDown",
        )
        crud_form_buttons.add_control("/s")
        crud_form_buttons.add_control(
            "_edit_button",
            "edit",
            control="button",
            mess="enable editing",
            valid=self.crud_view_to_edit,
            disabled=True if mode is not VIEW else False,
        )
        crud_form_buttons.add_control("/s")
        crud_form_buttons.add_control(
            "_ok_button",
            "Ok",
            control="button",
            mess="save data",
            disabled=True if mode is VIEW else False,
            hotkey="PgDown",
            valid=self.crud_save,
        )
        crud_form_buttons.add_control(
            "_cancel_button",
            "Cancel",
            control="button",
            mess="Do not save data",
            valid=self.crud_close,
        )
        return crud_form_buttons

    def crud_view_to_edit(self):
        self.crud_form.set_title(f"{self.title}.[EDIT]")
        self.w._ok_button.set_enabled(True)
        self.w._prev_button.set_enabled(False)
        self.w._next_button.set_enabled(False)
        self.w._edit_button.set_enabled(False)

    def move_crud_view(self, mode):
        self.grid_form.move_grid_index(mode)
        self.set_crud_form_data()

    def crud_save(self):
        print("save")
        pass

    def crud_close(self):
        self.crud_form.close()
        pass

    def show_crud_form(self, mode):
        crud_form_buttons = self.prepare_crud_form_buttons(mode)
        self.crud_form = self._ZzFormWindow_class(self, f"{self.title}.[{mode}]")
        self.crud_form.build_form(self.controls.controls, crud_form_buttons.controls)
        self.set_crud_form_data()
        self.crud_form.show_form()

    def set_crud_form_data(self):
        data = self.model.get_record(self.current_row)
        for x in data:
            if x not in self.crud_form.widgets:
                continue
            self.crud_form.widgets[x].set_text(data[x])

    def grid_index_changed(self, row, column):
        self.current_row = row
        self.current_column = column

    def set_grid_index(self, row_number=0):
        self.grid_form.self.grid_widget(row_number)

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
        self.controls.add_control(
            name,
            label,
            control,
            pic,
            data,
            actions,
            valid,
            readonly,
            when,
            widget,
            tag,
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
        # Must be defined in any subclass
        self._widgets_package = None
        self.escapeEnabled = True
        self.mode = "form"
        self.hotkey_widgets = {}

    def create_grid_navigation_actions(self):
        """returns standard actions for the grid"""
        actions = zzapp.ZzActions()
        actions.add_action(text="-")
        actions.add_action(text="<<", worker=lambda: self.move_grid_index(7))
        actions.add_action(text="🡸", worker=lambda: self.move_grid_index(8))
        actions.add_action(text="↺", worker=lambda: None, hotkey="F5")
        actions.add_action(text="🡺", worker=lambda: self.move_grid_index(2))
        actions.add_action(text=">>", worker=lambda: self.move_grid_index(1))
        return actions

    def create_grid_crud_actions(self):
        """returns standard actions for the grid"""
        actions = zzapp.ZzActions()
        actions.add_action(text="-")
        actions.add_action(
            text="View", worker=lambda: self.zz_form.show_crud_form(VIEW), hotkey="F12"
        )
        actions.add_action(
            text="New", worker=lambda: self.zz_form.show_crud_form(NEW), hotkey="Ins"
        )
        actions.add_action(
            text="Copy",
            worker=lambda: self.zz_form.show_crud_form(COPY),
            hotkey="Ctrl+Ins",
        )
        actions.add_action(
            text="Edit",
            worker=lambda: self.zz_form.show_crud_form(EDIT),
            hotkey="Spacebar",
        )
        actions.add_action(text="Remove", worker=lambda: None, hotkey="Delete")
        actions.add_action(text="-")
        return actions

    def move_grid_index(self, direction=None):
        if direction == 7:  # Top
            self.set_grid_index(0, self.get_grid_index()[1])
        elif direction == 8:  # Up
            self.set_grid_index(self.get_grid_index()[0] - 1, self.get_grid_index()[1])
        elif direction == 2:  # Down
            self.set_grid_index(self.get_grid_index()[0] + 1, self.get_grid_index()[1])
        elif direction == 1:  # Last
            self.set_grid_index(self.get_grid_row_count(), self.get_grid_index()[1])

    def set_grid_index(self, row=0, col=0):
        self.widgets["form__grid"].set_index(row, col)

    def get_grid_index(self):
        return self.widgets["form__grid"].current_index()

    def get_grid_row_count(self):
        return self.widgets["form__grid"].row_count()

    def build_grid(self):
        # populate model with columns metadata
        self.mode = "grid"
        for meta in self.zz_form.controls.controls:
            if meta.get("name", "").startswith("/"):
                continue
            self.zz_form.model.add_column(meta)

        actions = [
            self.create_grid_crud_actions(),
            self.zz_form.actions,
            self.create_grid_navigation_actions(),
        ]

        gridForm = ZzForm()
        gridForm.add_control("/vs", tag="gridsplitter")
        gridForm.add_control("toolbar", control="toolbar", actions=actions)
        gridForm.add_control("form__grid", control="grid")

        self.build_form(gridForm.controls.controls)
        # print (self.widgets.keys())
        self.move_grid_index(7)

        return

    def build_form(self, controls=[], extra_controls=[]):
        frame_stack = [self]
        tmp_frame = None

        if controls == []:
            controls = self.zz_form.controls.controls
        for meta in controls + extra_controls:
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
            # Hotkeys 
            if meta.get("hotkey") and meta.get("valid"):
                if meta.get("hotkey") not in self.hotkey_widgets:
                    self.hotkey_widgets[meta.get("hotkey")] = []
                self.hotkey_widgets[meta.get("hotkey")].append(widget2add)
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
            widget = self.zz_form.form_stack[-1].widgets.get(name)
            if widget:
                widget.set_text(value)
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


class ZzFormWidget:
    """Get widget object from form"""

    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    def __getattr__(self, name):
        widget = None
        if self.zz_form.form_stack == []:
            if self.zz_form.last_closed_form is None:
                return None
            else:
                widget = self.zz_form.last_closed_form.widgets.get(name)
        else:
            widget = self.zz_form.form_stack[-1].widgets.get(name)
        if widget is not None:
            return widget