if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zzapp as zzapp
import zzgui.zzform as zzform

from zzgui.zz_qt5.app import ZzQtWindow
from zzgui.utils import num

from PyQt5.QtWidgets import QDialog

# from PyQt5.QtWidgets import QFormLayout


class zzDialog(QDialog):
    def __init__(self, title=""):
        super().__init__()
        # self.setWindowTitle(title)
        # self.exec_()
        # print (123, [f"{x}" for x in dir(self) if x.startswith("e")])


# class ZzForm(zzform.ZzForm, ZzQtWindow, QDialog):
class ZzForm(zzDialog, zzform.ZzForm, ZzQtWindow):
    def __init__(self, title=""):
        super().__init__()
        zzform.ZzForm.__init__(self, title)
        self._widgets_package = __import__("zzgui.zz_qt5.widgets", None, None, [""])

    def restore_geometry(self, settings):
        paw = self.parent()
        if paw is not None:
            left = num(settings.get(self.window_title, "left", "0"))
            top = num(settings.get(self.window_title, "top", "0"))

            paw.move(left, top)
            width = num(settings.get(self.window_title, "width", "800"))
            height = num(settings.get(self.window_title, "height", "600"))
            paw.resize(width, height)
        # if num(settings.get(self.window_title, "is_max", "0")):
        #     paw.showMaximized()

    def get_position(self):
        paw = self.parent()
        if paw is not None:
            return (paw.pos().x(), paw.pos().y())

    def showEvent(self, event=None):
        if self.shown:
            return
        self.restore_geometry(zzapp.zz_app.settings)
        self.shown = True
        if event:
            event.accept()

    def close(self):
        super().close()
        if self.parent() is not None:
            self.parent().close()
        else:
            QDialog.close(self)

    def closeEvent(self, event=None):
        if self.prev_form:
            self.prev_form.setEnabled(True)
        self.close()
        if event:
            event.accept()
