import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QSizePolicy

from zzgui.qt5.zzwidget import ZzWidget


class zzspace(QFrame, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setLayout(QHBoxLayout())
        self.layout().addStretch()
