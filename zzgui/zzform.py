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
        self.controls = []

    def show_form(self, modal="modal"):
        zzapp.zz_app.show_form(self, modal)
        # self.restore_geometry(zzapp.zz_app.settings)

    def close(self):
        print("close")
        self.save_geometry(zzapp.zz_app.settings)

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
