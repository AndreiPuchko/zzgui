import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTabWidget

from zzgui.qt5.zzwindow import ZzFrame
from zzgui.qt5.zzwidget import ZzWidget


class zztab(QTabWidget, ZzWidget, ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta

    def add_tab(self, widget, text=""):
        self.addTab(widget, text)
