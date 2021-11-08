import sys


if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QWidget

# import zzgui.zzgui as zzgui
import zzgui.zzapp as zzgui


class ZzQtWindow(zzgui.ZzWindow, QWidget):
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
