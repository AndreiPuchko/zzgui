if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QFontMetrics

from zzgui import zzwidget
from zzgui.qt5.zzwindow import zz_align


class ZzWidget(QWidget, zzwidget.ZzWidget):
    def __init__(self, meta={}):
        super().__init__()
        zzwidget.ZzWidget.__init__(self, meta)
        # self.setContentsMargins(0, 0, 0, 0)

    def mouseDoubleClickEvent(self, event):
        if self.meta.get("dblclick"):
            self.meta.get("dblclick")()
        return super().mouseDoubleClickEvent(event)

    def set_tooltip(self, mess):
        self.setToolTip(mess)

    def set_disabled(self, arg=True):
        self.setEnabled(True if not arg else False)

    def set_enabled(self, arg=True):
        self.setEnabled(True if arg else False)

    def set_text(self, text):
        if hasattr(self, "setText"):
            self.setText(f"{text}")

    def get_text(self):
        if hasattr(self, "text"):
            return self.text()
        return ""

    def set_readonly(self, arg):
        if hasattr(self, "setReadOnly"):
            self.setReadOnly(True if arg else False)

    def is_enabled(self):
        return self.isEnabled()

    def set_visible(self, arg=True):
        self.setVisible(arg)

    def is_visible(self):
        if hasattr(self, "isVisible"):
            return self.isVisible()

    def is_readonly(self):
        if hasattr(self, "isReadOnly"):
            return self.isReadOnly()

    def set_focus(self):
        self.setFocus()

    def set_maximum_width(self, width, char="O"):
        if self.meta.get("control", "") not in ("radio", "check"):
            if char != "":
                self.setMaximumWidth(QFontMetrics(self.font()).width(char) * width)
            else:
                self.setMaximumWidth(width)

    def set_fixed_width(self, width, char="O"):
        if self.meta.get("control", "") not in ("radio", "check"):
            if char != "":
                self.setFixedWidth(QFontMetrics(self.font()).width(char) * width)
            else:
                self.setFixedWidth(width)

    def set_fixed_height(self, width, char="O"):
        if self.meta.get("control", "") not in ("radio", "check"):
            if char != "":
                self.setFixedHeight(QFontMetrics(self.font()).height() * width)
            else:
                self.setFixedHeight(width)

    def set_maximum_len(self, length):
        if hasattr(self, "setMaxLength"):
            return self.setMaxLength(length)

    def set_alignment(self, alignment):
        if hasattr(self, "setAlignment"):
            self.setAlignment(zz_align[f"{alignment}"])

    # def valid(self):
    #     if self.meta.get("valid"):
    #         return self.meta.get("valid", lambda: True)()
    #     else:
    #         return True

    # def when(self):
    #     if self.meta.get("when"):
    #         return self.meta.get("when", lambda: True)()
    #     else:
    #         return True

    def set_style_sheet(self, css: str):
        super().set_style_sheet(css)
        self.setStyleSheet(self.style_sheet)

    def add_style_sheet(self, css: str):
        last_style = self.styleSheet() + f"; {css}"
        super().set_style_sheet(last_style)
        self.setStyleSheet(last_style)

    def get_style_sheet(self):
        return self.styleSheet()

    # def fix_default_height(self):
    #     self.set_maximum_height(self.get_default_height())

    def get_default_height(self):
        return self.sizeHint().height()

    def set_maximum_height(self, height):
        self.setMaximumHeight(height)

    # def fix_default_width(self):
    #     self.set_maximum_width(self.get_default_width())

    def get_default_width(self):
        return self.sizeHint().width()

    def set_size_policy(self, horizontal, vertical):
        self.setSizePolicy(horizontal, vertical)

    def get_next_focus_widget(self, pos=1):
        return self.nextInFocusChain()

    def get_next_widget(self, pos=1):
        return self.layout().widget()

    def add_widget_above(self, widget, pos=0):
        my_pos = self.parentWidget().layout().indexOf(self)
        self.parent().layout().insertWidget(my_pos - pos, widget)

    def add_widget_below(self, widget, pos=0):
        my_pos = self.parentWidget().layout().indexOf(self)
        self.parent().layout().insertWidget(my_pos + pos + 1, widget)

    def remove(self):
        self.parentWidget().layout().removeWidget(self)
        self.setParent(None)

    def get_layout_position(self):
        return self.parentWidget().layout().indexOf(self)

    def get_layout_count(self):
        return self.parentWidget().layout().count()

    def get_layout_widget(self, pos):
        return self.parentWidget().layout().itemAt(pos).widget()

    def get_layout_widgets(self):
        return [self.get_layout_widget(x) for x in range(self.get_layout_count())]

    def move_up(self):
        pos = self.get_layout_position()
        if pos > 0:
            w = self.parentWidget().layout().takeAt(pos).widget()
            self.parentWidget().layout().insertWidget(pos - 1, w)

    def move_down(self):
        pos = self.get_layout_position()
        if pos < self.get_layout_count()-1:
            w = self.parentWidget().layout().takeAt(pos+1).widget()
            self.parentWidget().layout().insertWidget(pos, w)

    def action_set_visible(self, text, mode=True):
        for action in self.actions():
            if action.text().strip() == text:
                action.setVisible(mode)

    def action_set_enabled(self, text, mode=True):
        for action in self.actions():
            if action.text().strip() == text:
                action.setVisible(mode)
