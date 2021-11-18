if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QDialog, QMdiSubWindow
from PyQt5.QtCore import Qt

import zzgui.zzapp as zzapp
import zzgui.zzform as zzform

from zzgui.zz_qt5.app import ZzQtWindow
from zzgui.zzutils import num


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

    # def show_dialog(self, title="", modal="modal"):
    #     self.get_form_widget().show_form(title, modal)

    # def show_mdi_modal_dialog(self, title=""):
    #     self.get_form_widget().show_form(title, "modal")

    # def show_app_modal_dialog(self, title=""):
    #     self.get_form_widget().show_form(title, modal="super")

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
        self.zz_form.form_stack.append(self)
        if not isinstance(self.parent(), QMdiSubWindow):
            self.escapeEnabled = False
        # mdi_height = (
        #     self.parent().parent().parent().viewport().height()
        #     - zzapp.zz_app.main_window.zz_tabwidget.tabBar().height()
        # )
        # mdi_width = self.parent().parent().parent().viewport().width()

        # size_before = self.size()
        self.restore_geometry(zzapp.zz_app.settings)
        # size_after = self.size()
        # width_delta = (
        #     0
        #     if size_before.width() < size_after.width()
        #     else size_before.width() - size_after.width()
        # )
        # height_delta = (
        #     0
        #     if size_before.height() < size_after.height()
        #     else size_before.height() - size_after.height()
        # )

        # paw = self.parent()
        # if width_delta or height_delta:
        #     paw.resize(size_after.width() + width_delta, size_after.height() + height_delta)
        # if self.parent().height() +self.parent().y() > mdi_height:
        #     self.parent().move(self.parent().x(),  0)
        self.shown = True
        if event:
            event.accept()

    def keyPressEvent(self, event):
        key = event.key()
        # keyText = QKeySequence(event.modifiers() | event.key()).toString()
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
        # super().keyPressEvent(event)

    def close(self):
        super().close()
        if self.parent() is not None:
            if isinstance(self.parent(), QMdiSubWindow):
                self.parent().close()
        else:
            QDialog.close(self)

    def closeEvent(self, event=None):
        # if self.prev_form:
        #     self.prev_form.parent().setEnabled(True)
        self.zz_form.close()
        if event:
            event.accept()
