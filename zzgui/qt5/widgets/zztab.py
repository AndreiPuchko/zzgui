import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTabBar, QTabWidget

from zzgui.qt5.zzwindow import ZzFrame
from zzgui.qt5.zzwidget import ZzWidget


class ZzTabBar(QTabBar):
    def get_text(self):
        return self.tabText(self.currentIndex())


class zztab(QTabWidget, ZzWidget, ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        self.setTabBar(ZzTabBar())
        self.meta = meta

    def add_tab(self, widget, text=""):
        self.addTab(widget, text)

    def get_text(self):
        return self.tabBar().tabText(self.currentIndex())
