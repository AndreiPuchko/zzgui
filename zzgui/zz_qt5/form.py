if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zzapp as zzapp
import zzgui.zzform as zzform

from zzgui.zz_qt5.app import ZzQtWindow
from zzgui.utils import num

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtGui import QKeySequence

from PyQt5.QtCore import Qt

# from PyQt5.QtWidgets import QFormLayout


# class zzDialog(QDialog):
#     def __init__(self, zz_form=""):
#         super().__init__(zz_form)
#     def closeEvent(self, event=None):
#         print("close event")
#         if self.prev_form:
#             self.prev_form.setEnabled(True)
#         self.close()
#         if event:
#             event.accept()


class ZzForm(zzform.ZzForm):
    # def __init__(self, title=""):
    #     super().__init__(title=title)
    def show_dialog(self, modal="modal"):
        dialog = ZzFormWindow(self)
        dialog.show_form(modal)

    def show_mdi_modal_dialog(self):
        ZzFormWindow(self).show_form("modal")

    def show_app_modal_dialog(self):
        ZzFormWindow(self).show_form(modal="super")


class ZzFormWindow(QDialog, zzform.ZzFormWindow, ZzQtWindow):
    def __init__(self, zz_form: ZzForm):
        super().__init__(zz_form)
        ZzQtWindow.__init__(self, zz_form.title)
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

    def keyPressEvent(self, event):
        key = event.key()
        keyText = QKeySequence(event.modifiers() | event.key()).toString()
        # print (f"{keyText}")
        # if key==Qt.Key_Escape:
        #     print (self,self.escapeEnabled)
        if key == Qt.Key_Escape and self.escapeEnabled:
            self.close()
        # elif self.mode == "form" and key in (Qt.Key_Up,):
        #     QApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.ShiftModifier))
        # elif self.mode == "form" and key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Down):
        #     QApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, event.modifiers()))
        # elif self.mode == "grid" and key in (Qt.Key_Return,):
        #     QApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Enter, event.modifiers()))
        # elif self.mode == "form" and keyText in self.hotKeyWidgets:  # is it form hotkey
        #     for wi in self.hotKeyWidgets[keyText]:
        #         if wi.isEnabled():
        #             # validate only not hotkeyed widget
        #             if wi != qApp.focusWidget() and \
        #                     hasattr(qApp.focusWidget(), "meta") and \
        #                     qApp.focusWidget().meta.get("key"):
        #                 if qApp.focusWidget().valid() is False:
        #                     return
        #             return wi.valid()
        # else:
        event.accept()
        super().keyPressEvent(event)

    def close(self):
        super().close()
        if self.parent() is not None:
            self.parent().close()
        else:
            QDialog.close(self)

    def closeEvent(self, event=None):
        print("close event")
        if self.prev_form:
            self.prev_form.setEnabled(True)
        self.close()
        if event:
            event.accept()
