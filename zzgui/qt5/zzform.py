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

            width = num(settings.get(self.window_title, "width", "-1"))
            height = num(settings.get(self.window_title, "height", "-1"))
            if -1 in [width, height]:  # bad settings or first run
                width = paw.parent().size().width()*0.9 if self.mode == "grid" else 0.5
                height = paw.parent().size().height()*0.9 if self.mode == "grid" else 0.5
            paw.resize(width, height)

            sizeAfter = paw.size()
            self.expand_size(paw, sizeBefore, sizeAfter)

            left = num(settings.get(self.window_title, "left", "-1"))
            top = num(settings.get(self.window_title, "top", "-1"))
            if -1 in [left, top]:  # bad settings or first run
                left, top = self.center_pos()

            paw.move(left, top)

            self.fit_size_and_pos(paw)

            if num(settings.get(self.window_title, "is_max", "0")):
                self.showMaximized()
                paw.move(0, 0)

    def center_pos(self):
        left = (self.parent().parent().size().width() - self.parent().size().width()) / 2
        top = (self.parent().parent().size().height() - self.parent().size().height()) / 2
        return left, top

    def expand_size(self, paw, sizeBefore, sizeAfter):
        wDelta = 0 if sizeBefore.width() < sizeAfter.width() else sizeBefore.width() - sizeAfter.width()
        hDelta = (
                0 if sizeBefore.height() < sizeAfter.height() else sizeBefore.height() - sizeAfter.height()
            )
        if wDelta or hDelta:
            paw.resize(paw.size().width() + wDelta, paw.size().height() + hDelta)

    def fit_size_and_pos(self, paw):
        """ ensure form fits outside window
        """
        parent_size = paw.parent().size()

        size = paw.size()
        original_size = paw.size()

        pos = paw.pos()
        orginal_pos = paw.pos()
        # width
        if parent_size.width() - (size.width()) < 0:
            size.setWidth(parent_size.width())
        if pos.x() + size.width() > parent_size.width():
            pos.setX(parent_size.width() - size.width())
        if pos.x() < 0:
            pos.setX(0)
        # height
        if parent_size.height() - (size.height()) < 0:
            size.setHeight(parent_size.height())

        if pos.y() + size.height() > parent_size.height():
            pos.setY(parent_size.height() - size.height())
        if pos.y() < 0:
            pos.setY(0)
        if orginal_pos != pos:
            paw.move(pos)
        if size != original_size:
            paw.resize(size)

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
            return

        if not isinstance(self.parent(), QMdiSubWindow):
            self.escapeEnabled = False

        # first_widget = self.widgets[list(self.widgets.keys())[0]]
        # while (
        #     not first_widget.isEnabled()
        #     or (hasattr(first_widget, "isReadOnly") and first_widget.isReadOnly())
        #     or first_widget.focusPolicy() == Qt.NoFocus
        # ):
        #     # print(first_widget)
        #     first_widget = first_widget.nextInFocusChain()

        # first_widget.setFocus()
        # print(first_widget)
        # set focus into first enabled widget
        for widget_name in self.widgets:
            widget = self.widgets[widget_name]
            if widget.focusPolicy() == Qt.NoFocus:
                continue
            if hasattr(widget, "isReadOnly") and widget.isReadOnly():
                continue
            if widget.isEnabled():
                widget.setFocus()
                break

        if self.zz_form.do_not_save_geometry is False:
            self.restore_geometry(zzapp.zz_app.settings)

        self.shown = True
        if event:
            event.accept()
        self.zz_form.after_form_show()

    def keyPressEvent(self, event: QEvent):
        key = event.key()
        keyText = QKeySequence(event.modifiers() | event.key()).toString()
        if key == Qt.Key_Escape and self.escapeEnabled:
            self.close()
        elif key == Qt.Key_Escape and not self.escapeEnabled:
            event.ignore()
            # return
        elif self.mode == "form" and key in (Qt.Key_Up,):
            QApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, Qt.ShiftModifier))
        elif self.mode == "form" and key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Down):
            QApplication.sendEvent(self, QKeyEvent(QEvent.KeyPress, Qt.Key_Tab, event.modifiers()))
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
        # event.acc5ept()

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
zzWait
zzAskYN
