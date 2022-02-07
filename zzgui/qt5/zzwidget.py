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
    def __init__(self, meta):
        super().__init__()
        zzwidget.ZzWidget.__init__(self, meta)
        # self.setContentsMargins(0, 0, 0, 0)

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

    def is_readonly(self):
        if hasattr(self, "isReadOnly"):
            return self.isReadOnly()

    def set_focus(self):
        self.setFocus()

    def set_maximum_width(self, width):
        if self.meta.get("control", "") not in ("radio", "check"):
            self.setMaximumWidth(QFontMetrics(self.font()).width("W") * width)

    def set_maximum_len(self, length):
        if hasattr(self, "setMaxLength"):
            return self.setMaxLength(length)

    def set_alignment(self, alignment):
        if hasattr(self, "setAlignment"):
            self.setAlignment(zz_align[f"{alignment}"])

    def valid(self):
        if self.meta.get("valid"):
            return self.meta.get("valid", lambda: True)()
        else:
            return True

    def when(self):
        if self.meta.get("when"):
            return self.meta.get("when", lambda: True)()
        else:
            return True
