import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from zzgui.zzgui import ZzApp
from zzgui.zzgui import ZzWindow

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QToolButton
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QFormLayout
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt

# from PyQt5.Qsci import *

zzAlign = {
    "": Qt.AlignLeft | Qt.AlignTop,
    "1": Qt.AlignLeft | Qt.AlignBottom,
    "2": Qt.AlignHCenter | Qt.AlignBottom,
    "3": Qt.AlignRight | Qt.AlignBottom,
    "4": Qt.AlignLeft | Qt.AlignVCenter,
    "5": Qt.AlignHCenter | Qt.AlignVCenter,
    "6": Qt.AlignRight | Qt.AlignVCenter,
    "7": Qt.AlignLeft | Qt.AlignTop,
    "8": Qt.AlignHCenter | Qt.AlignTop,
    "9": Qt.AlignRight | Qt.AlignTop,
}


def layout(arg="h"):
    if arg.lower().startswith("v"):
        layout = QVBoxLayout()
        # layout = zzVBoxLayout()
        layout.setAlignment(zzAlign["7"])
    elif arg.lower().startswith("f"):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignTop)
    elif arg.lower().startswith("g"):
        layout = QGridLayout()
    else:
        layout = QHBoxLayout()
        # layout = zzHBoxLayout()
        layout.setAlignment(zzAlign["7"])
    layout.layout().setContentsMargins(0, 0, 0, 0)
    layout.layout().setSpacing(0)
    return layout


class ZzQtWindow(ZzWindow, QWidget):
    def __init__(self, title=""):
        super().__init__()
        self.set_title(title)

    def set_position(self, left, top):
        self.move(left, top)

    def set_size(self, width, height):
        self.resize(width, height)

    def get_position(self):
        return (self.pos().x(), self.pos().y())

    def get_size(self):
        return (self.size().width(), self.size().height())

    def set_title(self, title):
        super().set_title(title)
        QWidget.setWindowTitle(self, title)

    def is_maximized(self):
        return 1 if QWidget.isMaximized(self) else 0

    def show_maximized(self):
        QWidget.showMaximized(self)


class ZzQtApp(ZzApp, QMainWindow, ZzQtWindow):
    def __init__(self, title=""):
        self._core_app = QApplication([])
        super().__init__()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout("v"))
        self.statusBar().setVisible(True)
        self.toolbar = QToolBar()
        self.centralWidget().layout().addWidget(self.toolbar)
        self.set_title(title)

    def build_menu(self):
        self.menu_list = super().reorder_menu(self.menu_list)
        self._main_menu = {}
        QMainWindow.menuBar(self).clear()
        QMainWindow.menuBar(self).show()
        for x in self.menu_list:
            _path = x["TEXT"]
            if _path == "":
                continue
            prevNode = "|".join(_path.split("|")[:-1])
            topic = _path.split("|")[-1]
            if _path in self._main_menu:
                continue
            if _path.count("|") == 0:  # first in chain - menu bar
                node = QMainWindow.menuBar(self)
            else:
                node = self._main_menu[prevNode]
            if _path.endswith("-"):
                node.addSeparator()
            elif x["WORKER"]:
                self._main_menu[_path] = node.addAction(topic)
                self._main_menu[_path].triggered.connect(x["WORKER"])
                if x["TOOLBAR"]:
                    button = QToolButton()
                    button.setText(topic)
                    button.setDefaultAction(self._main_menu[_path])
                    self.toolbar.addAction(self._main_menu[_path])
            else:
                self._main_menu[_path] = node.addMenu(topic)

    def show_menubar(self, mode=True):
        ZzApp.show_menubar(self)
        if mode:
            QMainWindow.menuBar(self).show()
        else:
            QMainWindow.menuBar(self).hide()

    def is_menubar_visible(self):
        return QMainWindow.menuBar(self).isVisible()

    def show_toolbar(self, mode=True):
        ZzApp.show_toolbar(self)
        if mode:
            self.toolbar.show()
        else:
            self.toolbar.hide()

    def is_toolbar_visible(self):
        return self.toolbar.isVisible()

    def run(self):
        super().run()
        self.show()
        self._core_app.exec_()

    def closeEvent(self, e):
        self.close()
        e.accept()

    def close(self):
        super().close()
        QMainWindow.close(self)
