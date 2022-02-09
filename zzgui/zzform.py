if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zzapp as zzapp
from zzgui.zzmodel import ZzModel
from zzgui.zzutils import int_

VIEW = "VIEW"
NEW = "NEW"
COPY = "COPY"
EDIT = "EDIT"
NO_DATA_WIDGETS = ("button", "toolbutton", "frame", "label")
NO_LABEL_WIDGETS = ("button", "toolbutton", "frame", "label", "check")


class ZzForm:
    def __init__(self, title=""):
        super().__init__()
        self.title = title
        self.form_stack = []
        self.heap = zzapp.ZzHeap()
        self.actions = zzapp.ZzActions()
        self.controls = zzapp.ZzControls()
        self.system_controls = zzapp.ZzControls()
        self.model = None
        self.db = zzapp.zz_app.db
        self._model_record = {}  # contains the data of the currently edited record

        # Shortcuts to elements
        self.s = ZzFormData(self)  # widgets data by name
        self.w = ZzFormWidget(self)  # widgets by name
        self.a = ZzFormAction(self)  # Actions by text
        self.r = ZzModelData(self)  # Grid data by name

        self.children_forms = []  # forms inside this form
        self.i_am_child = None
        self.max_child_level = 1  # max depth for child forms

        self.show_grid_action_top = True
        self.do_not_save_geometry = False

        # Must be redefined in any subclass
        self._ZzFormWindow_class = ZzFormWindow
        self._zzdialogs = None

        self._in_close_flag = False
        self.last_closed_form = None

        self.crud_form = None
        self.crud_mode = ""

        self.grid_form = None

        self.current_row = 0
        self.current_column = 0

    def run(self):
        if self.model:
            self.show_mdi_modal_grid()
        else:
            self.show_mdi_modal_form()

    def set_model(self, model):
        self.model: ZzModel = model
        self.model.zz_form = self
        return self.model

    def refresh(self):
        self.model.refresh()
        self.refresh_children()
        self.set_grid_index()

    def widgets(self):
        return self.form_stack[-1].widgets

    def widgets_list(self):
        return [self.form_stack[-1].widgets[x] for x in self.form_stack[-1].widgets]

    def focus_widget(self):
        return zzapp.zz_app.focus_widget()

    def close(self):
        if self._in_close_flag:
            return
        self._in_close_flag = True
        if self.form_stack:
            # if self.form_stack[-1].escapeEnabled:
            self.last_closed_form = self.form_stack.pop()
            self.last_closed_form.close()
        self._in_close_flag = False

    def show_form(self, title="", modal="modal"):
        self.get_form_widget(title).show_form(modal)

    def show_mdi_form(self, title=""):
        z = self.get_form_widget(title)
        z.show_form(modal="")

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
        self.model.build()
        self.get_grid_crud_actions()
        self.grid_form.build_grid()
        # self._after_grid_create()
        return self.grid_form

    def get_grid_crud_actions(self):
        # is_view = self.a.__getattr__("/view")
        is_view = True
        is_crud = self.a.__getattr__("/crud")

        tmp_actions = zzapp.ZzActions()
        if is_view or is_crud:
            tmp_actions.add_action(
                text=zzapp.ACTION_VIEW_TEXT,
                worker=lambda: self.show_crud_form(VIEW),
                icon=zzapp.ACTION_VIEW_ICON,
                hotkey=zzapp.ACTION_VIEW_HOTKEY,
                tag="view",
            )
        if is_crud and not self.model.readonly:
            tmp_actions.add_action(
                text=zzapp.ACTION_NEW_TEXT,
                worker=lambda: self.show_crud_form(NEW),
                icon=zzapp.ACTION_NEW_ICON,
                hotkey=zzapp.ACTION_NEW_HOTKEY,
            )
            tmp_actions.add_action(
                text=zzapp.ACTION_COPY_TEXT,
                worker=lambda: self.show_crud_form(COPY),
                icon=zzapp.ACTION_COPY_ICON,
                hotkey=zzapp.ACTION_COPY_HOTKEY,
            )
            tmp_actions.add_action(
                text="Edit",
                worker=lambda: self.show_crud_form(EDIT),
                icon=zzapp.ACTION_EDIT_ICON,
                hotkey=zzapp.ACTION_EDIT_HOTKEY,
                tag="edit",
            )
            tmp_actions.add_action(text="-")
            tmp_actions.add_action(
                text=zzapp.ACTION_REMOVE_TEXT,
                worker=self.crud_delete,
                icon=zzapp.ACTION_REMOVE_ICON,
                hotkey=zzapp.ACTION_REMOVE_HOTKEY,
            )
            tmp_actions.add_action(text="-")

        for x in self.actions:
            if x.get("text").startswith("/"):
                continue
            tmp_actions.append(x)
        self.actions = tmp_actions

    def build_grid_view_auto_form(self):
        # Define layout
        if self.model.records:
            self.add_control("/f", "Frame with form layout")
            # Populate it with the columns from csv
            for x in self.model.records[0]:
                self.add_control(x, x, control="line", datalen=100)
            # Assign data source
            self.model.readonly = True
            self.actions.add_action(text="/view")

            if self.model.filterable:

                def run_filter_data_form():
                    filter_form = self.__class__("Filter Conditions")
                    # Populate form with columns
                    for x in self.controls:
                        filter_form.controls.add_control(
                            name=x["name"],
                            label=x["label"],
                            control=x["control"],
                            check=False if x["name"].startswith("/") else True,
                            datalen=x["datalen"],
                        )

                    def before_form_show():
                        # put previous filter conditions to form
                        for x in self.model.get_where().split(" and "):
                            if "' in " not in x:
                                continue
                            column_name = x.split(" in ")[1].strip()
                            column_value = x.split(" in ")[0].strip()[1:-1]
                            filter_form.w.__getattr__(column_name).set_text(column_value)
                            filter_form.w.__getattr__(column_name).check.set_checked()

                    def valid():
                        # apply new filter to grid
                        filter_list = []
                        for x in filter_form.widgets_list():
                            if x.check and x.check.is_checked():
                                filter_list.append(f"'{x.get_text()}' in {x.meta['name']}")
                        filter_string = " and ".join(filter_list)
                        self.model.set_where(filter_string)

                    filter_form.before_form_show = before_form_show
                    filter_form.valid = lambda: self._zzdialogs.zzWait(valid, "Sorting...")
                    filter_form.add_ok_cancel_buttons()
                    filter_form.show_mdi_modal_form()

                self.actions.add_action("Filter", worker=run_filter_data_form, hotkey="F9")

    def get_table_schema(self):
        rez = []
        if self.model is not None:
            table_name = ""
            table_name = self.model.get_table_name()
            for x in self.controls:
                if x["name"].startswith("/"):
                    continue
                if x.get("control") in NO_DATA_WIDGETS:
                    continue
                column = {
                    "table": table_name,
                    "column": x["name"],
                    "datatype": x["datatype"],
                    "datalen": x["datalen"],
                    "datadec": x["datadec"],
                    "to_table": x["to_table"],
                    "to_column": x["to_column"],
                    "related": x["related"],
                    "pk": x["pk"],
                }
                rez.append(column)
        return rez

    def _valid(self):
        if self.valid() is False:
            return
        self.close()

    def _after_grid_create(self):
        pass

    def add_ok_cancel_buttons(self):
        buttons = zzapp.ZzControls()
        buttons.add_control("/")
        buttons.add_control("/h", "")
        buttons.add_control("/s")

        buttons.add_control(
            name="_ok_button",
            label="Ok",
            control="button",
            hotkey="PgDown",
            valid=self._valid,
        )
        buttons.add_control(
            name="_cancel_button",
            label="Cancel",
            control="button",
            mess="Do not save data",
            valid=self.close,
        )

        self.system_controls = buttons

    def add_crud_buttons(self, mode):
        buttons = zzapp.ZzControls()
        buttons.add_control("/")
        buttons.add_control("/h", "")
        buttons.add_control(
            name="_prev_button",
            label="<",
            control="button",
            mess="prev record",
            valid=lambda: self.move_crud_view(8),
            disabled=True if mode is not VIEW else False,
            hotkey="PgUp",
        )
        buttons.add_control(
            name="_next_button",
            label=">",
            control="button",
            mess="prev record",
            valid=lambda: self.move_crud_view(2),
            disabled=True if mode is not VIEW else False,
            hotkey="PgDown",
        )
        buttons.add_control("/s")

        if self.a.tag("edit"):
            buttons.add_control(
                name="_edit_button",
                label=zzapp.CRUD_BUTTON_EDIT_TEXT,
                control="button",
                mess=zzapp.CRUD_BUTTON_EDIT_MESSAGE,
                valid=self.crud_view_to_edit,
                disabled=True if mode is not VIEW else False,
            )
            buttons.add_control("/s")

            buttons.add_control(
                name="_ok_button",
                label=zzapp.CRUD_BUTTON_OK_TEXT,
                control="button",
                mess=zzapp.CRUD_BUTTON_OK_MESSAGE,
                disabled=True if mode is VIEW else False,
                hotkey="PgDown",
                valid=self.crud_save,
            )

        buttons.add_control(
            name="_cancel_button",
            label=zzapp.CRUD_BUTTON_CANCEL_TEXT,
            control="button",
            mess=zzapp.CRUD_BUTTON_CANCEL_MESSAGE,
            valid=self.crud_close,
        )
        self.system_controls = buttons

    def crud_view_to_edit(self):
        self.crud_form.set_title(f"{self.title}.[EDIT]")
        self.w._ok_button.set_enabled(True)
        self.w._prev_button.set_enabled(False)
        self.w._next_button.set_enabled(False)
        self.w._edit_button.set_enabled(False)

    def move_crud_view(self, mode):
        """move current grid record
        up (mode=8) or down (mode=2) - look at numpad to understand why
        and update values in crud_form
        """
        self.move_grid_index(mode)
        self.set_crud_form_data()

    def crud_delete(self):
        selected_rows = self.grid_form.get_grid_selected_rows()
        if len(selected_rows) == 1:
            ask_text = zzapp.ASK_REMOVE_RECORD_TEXT
        else:
            ask_text = zzapp.ASK_REMOVE_RECORDS_TEXT % len(selected_rows)
        if selected_rows and self._zzdialogs.zzAskYN(ask_text):
            show_error_messages = True
            for row in selected_rows:
                if self.model.delete(row) is not True and show_error_messages:
                    if selected_rows.index(row) == len(selected_rows) - 1:
                        self._zzdialogs.zzMess(self.model.get_data_error())
                    else:
                        if (
                            self._zzdialogs.zzAskYN(
                                zzapp.REMOVE_RECORD_ERROR_TEXT
                                + "<br>"
                                + self.model.get_data_error()
                                + "<br>"
                                + "Do not show next errors?"
                            )
                            == 2
                        ):
                            show_error_messages = False
            self.model.refresh()
            self.set_grid_index(row)

    def crud_save(self):
        crud_data = self.get_crud_form_data()
        if self.crud_mode in [EDIT, VIEW]:
            rez = self.model.update(crud_data, self.current_row)
            self.set_grid_index(self.current_row)
        else:
            rez = self.model.insert(crud_data, self.current_row)
            self.move_grid_index(1)
        if rez is False:
            self._zzdialogs.zzMess(self.model.get_data_error())
        else:
            self.close()

    def get_crud_form_data(self):
        crud_data = {}
        crud_data.update(self._model_record)
        for x in self.crud_form.widgets:
            if x.startswith("/"):
                continue
            widget = self.crud_form.widgets[x]
            if widget.meta.get("control") in NO_DATA_WIDGETS:
                continue
            crud_data[x] = self.s.__getattr__(x)

        return crud_data

    def crud_close(self):
        self.crud_form.close()
        pass

    def show_crud_form(self, mode):
        """mode - VIEW, NEW, COPY, EDIT"""
        self.crud_mode = mode
        self.add_crud_buttons(mode)
        self.crud_form = self._ZzFormWindow_class(self, f"{self.title}.[{mode}]")
        self.crud_form.build_form()
        self.set_crud_form_data(mode)
        self.crud_form.show_form()

    def set_crud_form_data(self, mode=EDIT):
        """set current record's value in crud_form"""
        where_string = self.model.get_where()
        if "=" in where_string:
            where_dict = {
                x.split("=")[0].strip(): x.split("=")[1].strip()
                for x in self.model.get_where().split(" and ")
            }
        else:
            where_dict = {}

        self._model_record = self.model.get_record(self.current_row)
        for x in self._model_record:
            if x not in self.crud_form.widgets:
                continue
            if mode == NEW:
                if x not in where_dict:
                    self.crud_form.widgets[x].set_text("")
                else:  # set where fields
                    if where_dict[x][0] == where_dict[x][-1] and where_dict[x][0] in (
                        '"',
                        "'",
                    ):
                        where_dict[x] = where_dict[x][1:-1]  # cut quotes
                    self.crud_form.widgets[x].set_text(where_dict[x])
                    self.crud_form.widgets[x].set_disabled()
            else:
                self.crud_form.widgets[x].set_text(self._model_record[x])

    def grid_index_changed(self, row, column):
        refresh_children_forms = row != self.current_row and row >= 0
        refresh_children_forms = True
        self.current_row = row
        self.current_column = column
        if refresh_children_forms:
            self.refresh_children()

    def refresh_children(self):
        for action in self.children_forms:
            filter = self.get_where_for_child(action)
            action["child_form_object"].model.set_where(filter)
            action["child_form_object"].model.refresh()
            action["child_form_object"].set_grid_index()
            action["child_form_object"].refresh_children()

    def show_child_form(self, action):
        child_form = action.get("child_form")()
        child_form.model.set_where(self.get_where_for_child(action))
        child_form.model.refresh()
        child_form.show_mdi_modal_grid()
        self.refresh()

    def get_where_for_child(self, action):
        if self.current_row >= 0:
            current_record = self.model.get_record(self.current_row)
            if action["child_form_object"].grid_form:
                action["child_form_object"].grid_form.set_enabled()
            return action["child_where"].format(**current_record)
        else:
            if action["child_form_object"].grid_form:
                action["child_form_object"].grid_form.set_disabled()
            return "1=2"

    def grid_header_clicked(self, column):
        if self.model is not None:
            self._zzdialogs.zzWait(lambda: self.model.set_order(column), "Sorting...")
            self.refresh()

    def grid_double_clicked(self):
        for tag in ("select", "view", "edit"):
            action = self.a.tag(tag)
            if action and action.get("worker"):
                action.get("worker")()
                break

    def set_grid_index(self, row=None, column=None):
        if row is None:
            row = self.current_row
        if column is None:
            column = self.current_column
        if self.grid_form:
            self.grid_form.set_grid_index(row, column)

    def move_grid_index(self, mode):
        self.grid_form.move_grid_index(mode)

    def get_controls(self):
        return self.controls + self.system_controls

    def when(self):
        pass

    def valid(self):
        pass

    def before_form_show(self):
        pass

    def after_form_show(self):
        pass

    def add_control(
        self,
        name="",
        label="",
        gridlabel="",
        control="",
        pic="",
        data="",
        datatype="char",
        datalen=0,
        datadec=0,
        pk="",
        actions=[],
        alignment=-1,
        to_table="",
        to_column="",
        to_form=None,
        related="",
        db=None,
        mask="",
        opts="",
        valid=None,
        readonly=None,
        disabled=None,
        check=None,
        noform=None,
        nogrid=None,
        when=None,
        widget=None,
        stretch=0,
        mess="",
        tag="",
        eat_enter=None,
        hotkey="",
    ):
        """
        to_form - form class or function(fabric) that returns form object
        """
        if isinstance(name, dict):
            self.controls.add_control(**name)
        else:
            d = locals().copy()
            del d["self"]
            self.controls.add_control(**d)
        return True  # Do not delete - it allows indentation in code

    def add_action(
        self,
        text,
        worker=None,
        icon="",
        mess="",
        hotkey="",
        tag="",
        child_form=None,
        child_where="",
    ):
        """
        child_form - form class or function(fabric) that returns form object
        """
        d = locals().copy()
        del d["self"]
        self.actions.add_action(**d)

    def validate_impexp_file_name(self, file, filetype):
        filetype = f".{filetype[:3].lower()}"
        file += "" if file.lower().endswith(filetype) else filetype
        return file

    def grid_data_export(self):
        file, filetype = zzapp.zz_app.get_save_file_dialoq("Export data", filter="CSV (*.csv);;JSON(*.json)")
        if not file:
            return
        file = self.validate_impexp_file_name(file, filetype)
        try:
            self.model.data_export(file)
        except Exception:
            self._zzdialogs.zzMess(f"Export error: {file}")

    def grid_data_import(self):
        file, filetype = zzapp.zz_app.get_open_file_dialoq("Export data", filter="CSV (*.csv);;JSON(*.json)")
        if not file:
            return
        file = self.validate_impexp_file_name(file, filetype)
        try:
            self.model.data_import(file)
        except Exception:
            self._zzdialogs.zzMess(f"Export error: {file}")


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
        self.grid_actions = zzapp.ZzActions()
        self._in_close_flag = None

    def create_grid_navigation_actions(self):
        """returns standard actions for the grid"""
        actions = zzapp.ZzActions()
        actions.add_action(text="-")
        actions.add_action(
            text=zzapp.ACTION_FIRST_ROW_TEXT,
            worker=lambda: self.move_grid_index(7),
            icon=zzapp.ACTION_FIRST_ROW_ICON,
            hotkey=zzapp.ACTION_FIRST_ROW_HOTKEY,
        )
        actions.add_action(
            text=zzapp.ACTION_PREVIOUS_ROW_TEXT,
            worker=lambda: self.move_grid_index(8),
            icon=zzapp.ACTION_PREVIOUS_ROW_ICON,
        )
        actions.add_action(
            text=zzapp.ACTION_REFRESH_TEXT,
            worker=lambda: self.zz_form.refresh(),
            icon=zzapp.ACTION_REFRESH_ICON,
            hotkey=zzapp.ACTION_REFRESH_HOTKEY,
        )
        actions.add_action(
            text=zzapp.ACTION_NEXT_ROW_TEXT,
            worker=lambda: self.move_grid_index(2),
            icon=zzapp.ACTION_NEXT_ROW_ICON,
        )
        actions.add_action(
            text=zzapp.ACTION_LAST_ROW_TEXT,
            worker=lambda: self.move_grid_index(1),
            icon=zzapp.ACTION_LAST_ROW_ICON,
            hotkey=zzapp.ACTION_LAST_ROW_HOTKEY,
        )
        actions.add_action(text="-")
        actions.add_action(text="Extra|Exp", worker=self.zz_form.grid_data_export)
        actions.add_action(text="Extra|Imp", worker=self.zz_form.grid_data_import)

        if not self.zz_form.i_am_child:
            actions.add_action(text="-")
            actions.add_action(
                text=zzapp.ACTION_CLOSE_TEXT,
                worker=self.close,
                icon=zzapp.ACTION_CLOSE_ICON,
            )

        return actions

    def move_grid_index(self, direction=None):
        """Directions - look at numpad to get the idea"""
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

    def get_grid_selected_rows(self):
        return self.widgets["form__grid"].get_selected_rows()

    def get_grid_row_count(self):
        return self.widgets["form__grid"].row_count()

    def build_grid(self):
        # populate model with columns metadata
        self.mode = "grid"
        tmp_grid_form = ZzForm()
        tmp_grid_form.add_control("/vs", tag="gridsplitter")

        tmp_grid_form.add_control(
            "form__grid",
            control="grid",
            actions=[self.zz_form.actions, self.create_grid_navigation_actions()],
            stretch=100,
        )
        # place child forms
        if self.zz_form.max_child_level:
            for action in self.zz_form.actions:
                if action.get("child_form"):
                    tmp_grid_form.add_control("/t", action.get("text", "="), stretch=100)
                    #  create child form!
                    action["child_form_object"] = action.get("child_form")()

                    action["child_form_object"].title = (
                        self.zz_form.title + "_" + action["child_form_object"].title
                    )
                    action["child_form_object"].i_am_child = True
                    action["child_form_object"].max_child_level = self.zz_form.max_child_level - 1
                    self.zz_form.children_forms.append(action)
                    tmp_grid_form.add_control(
                        f"child_grid__{action['text']}",
                        widget=action["child_form_object"],
                    )
        tmp_grid_form.add_control("/")

        if self.zz_form.show_app_modal_form is False:
            tmp_grid_form.controls[-1], tmp_grid_form.controls[-2] = (
                tmp_grid_form.controls[-2],
                tmp_grid_form.controls[-1],
            )
        self.build_form(tmp_grid_form.get_controls())
        self.zz_form.refresh_children()
        self.move_grid_index(1)

    def build_form(self, controls=[]):
        frame_stack = [self]
        tmp_frame = None

        if controls == []:
            controls = self.zz_form.get_controls()
        # set deafault layout to Form if first line not a layout def
        if controls and not controls[0].get("name", "").startswith("/"):
            controls.insert(0, {"name": "/f"})
        # Create widgets
        for meta in controls:
            meta["form"] = self.zz_form
            if meta.get("noform", ""):
                continue
            meta = zzapp.ZzControls.validate(meta)
            current_frame = frame_stack[-1]
            # do not add widget if it is not first tabpage on the form
            if not (meta.get("name", "") == ("/t") and self.tab_widget is not None):
                label2add, widget2add, action2add = self.widget(meta)
                if current_frame.frame_mode == "f":  # form layout
                    if label2add:
                        label2add.setContentsMargins(0, zzapp.zz_app.get_char_height() / 4, 0, 0)
                    if hasattr(widget2add, "frame_mode"):  # add any frame into form frame
                        label2add = self._get_widget("label")({"label": meta.get("label", "")})
                        widget2add.hide_border()
                        widget2add.label = label2add
                    current_frame.add_row(label2add, widget2add)
                else:  # v- h- box layout
                    if label2add is not None:
                        if (
                            current_frame != self
                            and current_frame.get_widget_count() == 0
                            and current_frame.label
                            and frame_stack[-2].frame_mode == "f"
                        ):
                            current_frame.label.set_text(label2add.get_text())
                            if widget2add:
                                widget2add.label = current_frame.label
                        else:
                            current_frame.add_widget(label2add)
                    if action2add is not None:
                        current_frame.add_widget(action2add)
                    if widget2add is not None:
                        current_frame.add_widget(widget2add)
                        if meta.get("control") == "toolbar":  # context menu for frame
                            widget2add.hide()
                            widget2add.set_context_menu(current_frame)
                        if action2add is not None:  # context menu for widget
                            action2add.set_context_menu(widget2add)
            # Hotkeys
            if meta.get("hotkey") and meta.get("valid"):
                if meta.get("hotkey") not in self.hotkey_widgets:
                    self.hotkey_widgets[meta.get("hotkey")] = []
                self.hotkey_widgets[meta.get("hotkey")].append(widget2add)
            # Special cases
            if meta.get("name", "") == ("/t"):  # If second and more tabpage widget
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
                continue  # do not touch - see elif +2
            elif meta.get("name", "") == "/":
                if len(frame_stack) > 1:
                    frame_stack.pop()
                    # Remove tab widget if it is at the end of stack
                    if "tab.tab" in f"{type(frame_stack[-1])}":
                        self.tab_widget = None
                        frame_stack.pop()
            elif meta.get("name", "").startswith("/"):
                frame_stack.append(widget2add)
        # Make it no more working
        self.build_grid = lambda: None
        self.build_form = lambda: None

    def widget(self, meta):
        """Widgets fabric"""
        if not meta.get("control"):
            if meta.get("widget"):
                control = "widget"
            else:
                control = "line" if meta.get("name") else "label"
        else:
            control = meta.get("control")

        if meta.get("to_table"):  # relation is here
            control = "relation"

        if control == "":
            control = "label"

        name = meta.get("name", "")
        label = meta.get("label", "")
        class_name = ""

        widget2add = None
        if label and control not in NO_LABEL_WIDGETS:
            label2add = self._get_widget("label")(meta)
        else:
            label2add = None

        # Form or widget
        if control == "widget":
            if isinstance(meta.get("widget"), ZzForm):
                if meta.get("widget").model is not None:
                    widget2add = meta.get("widget").get_grid_widget()
                else:
                    widget2add = meta.get("widget").get_form_widget()
            else:
                widget2add = meta.get("widget")
        else:  # Special cases
            if name[:2] in ("/h", "/v", "/f"):  # frame
                control = "frame"
                class_name = "frame"
                label2add = None
            elif "/" == name:
                return None, None, None
            elif "/t" in name:  # Tabpage
                label2add = None
                control = "tab"
            elif control.startswith("code"):
                control = "code"
            elif "radio" in control:
                control = "radio"
            elif "toolbar" in control:
                control = "toolbar"
            elif name == "/s":
                control = "space"

            widget_class = self._get_widget(control, class_name)
            widget2add = widget_class(meta)

            if hasattr(widget2add, "label"):
                widget2add.label = label2add
        if meta.get("check"):  # has checkbox
            label2add = self._get_widget("check", "check")({"label": meta["label"], "stretch": 0})
            label2add.add_managed_widget(widget2add)
            if not meta.get("data"):
                widget2add.set_disabled()
            else:
                label2add.set_checked()

        self.widgets[meta.get("tag", "") if meta.get("tag", "") else name] = widget2add

        actions2add = None
        if meta.get("actions") and meta.get("control") != "toolbar":
            actions2add = self._get_widget("toolbar", "toolbar")(
                {
                    "control": "toolbar",
                    "actions": meta["actions"],
                    "form": self.zz_form,
                    "stretch": 0,
                }
            )

        return label2add, widget2add, actions2add

    def _get_widget(self, module_name, class_name=""):
        """For given name returns class from current GUI engine module"""
        if class_name == "":
            class_name = module_name
        module_name = f"zz{module_name}"
        class_name = f"zz{class_name}"
        try:
            return getattr(getattr(self._widgets_package, module_name), class_name)
        except Exception:
            # print(self._widgets_package, module_name, class_name)
            return getattr(getattr(self._widgets_package, "zzlabel"), "zzlabel")

    def show_form(self, modal="modal", no_build=False):
        if no_build is False:
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
        self.restore_grid_columns()
        self.zz_form._after_grid_create()
        zzapp.zz_app.show_form(self, modal)

    def get_grid_list(self):
        return [self.widgets[x] for x in self.widgets if type(self.widgets[x]).__name__ == "zzgrid"]

    def get_sub_form_list(self):
        return [self.widgets[x] for x in self.widgets if type(self.widgets[x]).__name__ == "ZzFormWindow"]

    def restore_grid_columns(self):
        for grid in self.get_grid_list():
            col_settings = {}
            for count, x in enumerate(self.zz_form.model.headers):
                data = zzapp.zz_app.settings.get(self.window_title, f"grid_column__'{x}'")
                if data == "":
                    if self.zz_form.model.meta[count].get("relation"):
                        c_w = zzapp.GRID_COLUMN_WIDTH
                    else:
                        c_w = int_(self.zz_form.model.meta[count].get("datalen"))
                    c_w = zzapp.zz_app.get_char_width() * (min(c_w, zzapp.GRID_COLUMN_WIDTH))
                    data = f"{count}, {c_w}"
                col_settings[x] = data
            grid.set_column_settings(col_settings)
        for x in self.get_sub_form_list():
            x.restore_grid_columns()

    def save_grid_columns(self):
        for grid in self.get_grid_list():
            for x in grid.get_columns_settings():
                zzapp.zz_app.settings.set(
                    self.window_title,
                    f"grid_column__'{x['name']}'",
                    x["data"],
                )
        # for x in self.zz_form.children_forms:
        #     x["child_form_object"].close()
        for x in self.get_sub_form_list():
            x.close()

    def close(self):
        if self._in_close_flag:
            return
        self._in_close_flag = True
        # Splitters sizes
        for x in self.get_splitters():
            zzapp.zz_app.settings.set(
                self.window_title,
                f"splitter-{x}",
                self.widgets[x].splitter.get_sizes(),
            )
        # Grid columns
        self.save_grid_columns()
        self.save_geometry(zzapp.zz_app.settings)

    def get_splitters(self):
        return [
            x
            for x in self.widgets.keys()
            if hasattr(self.widgets[x], "splitter") and self.widgets[x].splitter is not None
        ]


class ZzFormData:
    """Get and put data from/to form"""

    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    def __setattr__(self, name, value):
        if name != "zz_form":
            widget = self.zz_form.form_stack[-1].widgets.get(name)
            if widget:
                widget.set_text(value)
            else:  # no widget - put data to model's record
                self.zz_form._model_record[name] = value
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
        else:  # no widget here? get data from model
            return self.zz_form._model_record.get(name, None)


class ZzFormWidget:
    """Get widget object from form"""

    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    def __getattr__(self, attrname):
        widget = None
        if self.zz_form.form_stack == []:
            if self.zz_form.last_closed_form is None:
                return None
            else:
                widgets = self.zz_form.last_closed_form.widgets
        else:
            widgets = self.zz_form.form_stack[-1].widgets
        # print(widgets)
        if attrname.startswith("_") and attrname.endswith("_"):
            pos = int_(attrname.replace("_", ""))
            if pos < len(widgets):
                widget = widgets.get(list(widgets)[pos])
        else:
            widget = widgets.get(attrname)
        if widget is not None:
            return widget


class ZzFormAction:
    def __init__(self, zz_form):
        self.zz_form: ZzForm = zz_form

    def tag(self, tag=""):
        if tag:
            for act in self.zz_form.actions:
                if act.get("tag") == tag:
                    return act
        return {}

    def __getattr__(self, name):
        for act in self.zz_form.actions:
            if act.get("text") == name:
                return act
        return {}


class ZzModelData:
    def __init__(self, zz_form: ZzForm):
        self.zz_form = zz_form

    def __getattr__(self, name):
        datadic = self.zz_form.model.get_record(self.zz_form.current_row)
        return datadic.get(name, "")
