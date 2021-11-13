if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from PyQt5.QtWidgets import QWidget

from zzgui import zzwidget


class ZzWidget(QWidget, zzwidget.ZzWidget):
    def __init__(self, meta):
        super().__init__()
        zzwidget.ZzWidget.__init__(self, meta)

    def set_enabled(self, arg=True):
        self.setEnabled(True if arg else False)

    def set_text(self, text):
        if hasattr(self, "setText"):
            self.setText(text)

    def get_text(self):
        if hasattr(self, "text"):
            return self.text()
        return ""

    def set_readonly(self, arg):
        if hasattr(self, "setReadOnly"):
            self.setReadOnly(True if arg else False)
