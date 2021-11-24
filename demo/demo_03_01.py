if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess


from demo.demo_03_00 import DemoApp as CoreDemoApp


class DemoApp(CoreDemoApp):
    def show_grid_form(self):
        form: ZzForm = self.describe_grid_form()

        def run_filter_data_form():
            filter_form = ZzForm("Filter Conditions")
            #Populate form with columns
            for x in form.controls.controls:
                filter_form.controls.add_control(
                    name=x["name"],
                    label=x["label"],
                    control=x["control"],
                    check=False if x["name"].startswith("/") else True,
                )

            def before_form_show():
                #put previous filter conditions to form
                for x in form.model.get_where().split(" and "):
                    if "' in " not in x:
                        continue
                    column_name = x.split("in")[1].strip()
                    column_value = x.split("in")[0].strip()[1:-1]
                    filter_form.w.__getattr__(column_name).set_text(column_value)
                    filter_form.w.__getattr__(column_name).check.set_checked()

            def valid():
                #apply new filter to grid
                filter_list = []
                for x in filter_form.widgets_list():
                    if x.check and x.check.is_checked():
                        filter_list.append(f"'{x.get_text()}' in {x.meta['name']}")
                filter_string = " and ".join(filter_list)
                form.model.set_where(filter_string)

            filter_form.before_form_show = before_form_show
            filter_form.valid = valid
            filter_form.add_ok_cancel_buttons()
            filter_form.show_mdi_modal_form()
        
        form.model.set_where()
        form.actions.add_action("Filter", worker=run_filter_data_form, hotkey="F9")
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
