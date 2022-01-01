if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QDialog, QMdiSubWindow, QApplication
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeySequence, QKeyEvent


import zzgui.zzapp as zzapp
import zzgui.zzform as zzform
import zzgui.qt5.widgets

from zzgui.qt5.zzapp import ZzQtWindow
from zzgui.zzutils import num

import zzgui.zzdialogs
from zzgui.zzdialogs import zzMess, zzWait, zzAskYN


class ZzForm(zzform.ZzForm):
    def __init__(self, title=""):
        super().__init__(title=title)
        self._ZzFormWindow_class = ZzFormWindow
        self._zzdialogs = zzgui.zzdialogs


class ZzFormWindow(QDialog, zzform.ZzFormWindow, ZzQtWindow):
    def __init__(self, zz_form: ZzForm, title=""):
        super().__init__(zz_form)
        title = title if title else zz_form.title
        ZzQtWindow.__init__(self, title)
        self._widgets_package = zzgui.qt5.widgets

    def restore_geometry(self, settings):
        paw = self.parent()
        if paw is not None:
            # save default == minimal size
            sizeBefore = paw.size()
            left = num(settings.get(self.window_title, "left", "0"))
            top = num(settings.get(self.window_title, "top", "0"))

            paw.move(left, top)
            width = num(settings.get(self.window_title, "width", "0"))
            height = num(settings.get(self.window_title, "height", "0"))
            if width > 0 and height > 0:
                paw.resize(width, height)

            # in case the minimal size is begger than last saved in the settings - correction
            sizeAfter = paw.size()
            wDelta = (
                0
                if sizeBefore.width() < sizeAfter.width()
                else sizeBefore.width() - sizeAfter.width()
            )
            hDelta = (
                0
                if sizeBefore.height() < sizeAfter.height()
                else sizeBefore.height() - sizeAfter.height()
            )
            if wDelta or hDelta:
                paw.resize(paw.size().width() + wDelta, paw.size().height() + hDelta)

        # if num(settings.get(self.window_title, "is_max", "0")):
        #     paw.showMaximized()

    def set_position(self, left, top):
        paw = self.parent()
        if paw is not None:
            paw.move(left, top)

    def set_size(self, w, h):
        paw = self.parent()
        if paw is not None:
            paw.resize(w, h)

    def get_position(self):
        parent_mdi_sub_window = self.parent()
        if parent_mdi_sub_window is not None:
            return (parent_mdi_sub_window.pos().x(), parent_mdi_sub_window.pos().y())

    def showEvent(self, event=None):
        if self.shown:
            return

        self.zz_form.form_stack.append(self)

        if self.zz_form.before_form_show() is False:
            self.zz_form.close()

        if not isinstance(self.parent(), QMdiSubWindow):
            self.escapeEnabled = False

        first_widget = self.widgets[list(self.widgets.keys())[0]]
        while (
            not first_widget.isEnabled()
            or (hasattr(first_widget, "isReadOnly") and first_widget.isReadOnly())
            or first_widget.focusPolicy() == Qt.NoFocus
        ):
            first_widget = first_widget.nextInFocusChain()
        first_widget.setFocus()

        # mdi_height = (
        #     self.parent().parent().parent().viewport().height()
        #     - zzapp.zz_app.main_window.zz_tabwidget.tabBar().height()
        # )
        # mdi_width = self.parent().parent().parent().viewport().width()

        # size_before = self.size()
        if self.zz_form.do_not_save_geometry is False:
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

    def keyPressEvent(self, event: QEvent):
        key = event.key()
        keyText = QKeySequence(event.modifiers() | event.key()).toString()
        if key == Qt.Key_Escape and self.escapeEnabled:
            self.close()
        elif self.mode == "form" and key in (Qt.Key_Up,):
            QApplication.sendEvent(
                self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.ShiftModifier)
            )
        elif self.mode == "form" and key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Down):
            QApplication.sendEvent(
                self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, event.modifiers())
            )
        elif self.mode == "grid" and key in (Qt.Key_Return,):
            self.zz_form.grid_double_clicked()
        elif keyText in self.hotkey_widgets:  # is it form hotkey
            for widget in self.hotkey_widgets[keyText]:
                if widget.is_enabled() and hasattr(widget, "valid"):
                    widget.valid()
                    return
                    # validate only not hotkeyed widget
                    # if wi != qApp.focusWidget() and \
                    #         hasattr(qApp.focusWidget(), "meta") and \
                    #         qApp.focusWidget().meta.get("key"):
                    #     if qApp.focusWidget().valid() is False:
                    #         return
                    # return wi.valid()

        #     for wi in self.hotKeyWidgets[keyText]:
        #         if wi.isEnabled():
        # else:
        event.accept()

    def close(self):
        super().close()
        if self.parent() is not None:
            if isinstance(self.parent(), QMdiSubWindow):
                self.parent().close()
        else:
            QDialog.close(self)

    def closeEvent(self, event=None):
        self.zz_form.close()
        if event:
            event.accept()


# Tells the module which engine to use
zzgui.zzdialogs.ZzForm = ZzForm
zzMess
