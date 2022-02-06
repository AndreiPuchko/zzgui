import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QProgressBar


from zzgui.qt5.zzwidget import ZzWidget


class zzprogressbar(QProgressBar, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.set_text(meta["label"])
        self.setMaximum(0)
        self.setMinimum(0)

    def set_max(self, value):
        self.setMaximum(value)

    def set_min(self, value):
        self.setMinimum(value)

    def set_value(self, value):
        self.setValue(value)
