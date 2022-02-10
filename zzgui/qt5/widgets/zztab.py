import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTabBar, QTabWidget, QShortcut
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

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

        self.next_tab_hotkey = QShortcut(QKeySequence("Ctrl+PgDown"), self)
        self.next_tab_hotkey.activated.connect(lambda tab=self: self.setCurrentIndex(self.currentIndex()+1))

        self.prev_tab_hotkey = QShortcut(QKeySequence("Ctrl+PgUp"), self)
        self.prev_tab_hotkey.activated.connect(lambda tab=self: tab.setCurrentIndex(tab.currentIndex() - 1))

    def set_shortcuts_local(self):
        self.next_tab_hotkey.setContext(Qt.WidgetWithChildrenShortcut)
        self.prev_tab_hotkey.setContext(Qt.WidgetWithChildrenShortcut)

    def add_tab(self, widget, text=""):
        self.addTab(widget, text)

    def get_text(self):
        return self.tabBar().tabText(self.currentIndex())
