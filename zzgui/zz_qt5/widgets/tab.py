import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QTabWidget, QWidget
from zzgui.zz_qt5.window import ZzFrame
import zzgui.zz_qt5.widget as zzwiddet


class tab(QTabWidget, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta

    def add_tab(self, widget, text=""):
        self.addTab(widget, text)
