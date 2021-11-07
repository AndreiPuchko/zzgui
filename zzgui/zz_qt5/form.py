import sys


if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


import zzgui.zzform as zzform
from zzgui.zz_qt5.app import ZzQtWindow
from PyQt5.QtWidgets import QDialog, QLabel
import zzgui.zzapp as zzapp
from zzgui.utils import num


class ZzForm(zzform.ZzForm, ZzQtWindow, QDialog):
    def __init__(self, title=""):
        super().__init__(title=title)

    def show_form(self, modal="modal"):
        self.setLayout(zzapp.zz_app.zz_layout())
        for meta in self.controls:
            self.layout().addWidget(QLabel(meta['label']))
        return super().show_form(modal=modal)

    def restore_geometry(self, settings):
        paw = self.parent()
        left = num(settings.get(self.window_title, "left", "0"))
        top = num(settings.get(self.window_title, "top", "0"))
        paw.move(left, top)
        width = num(settings.get(self.window_title, "width", "800"))
        height = num(settings.get(self.window_title, "height", "600"))
        paw.resize(width, height)
        # if num(settings.get(self.window_title, "is_max", "0")):
        #     paw.showMaximized()

    def get_position(self):
        paw = self.parent()
        return (paw.pos().x(), paw.pos().y())

    def showEvent(self, event=None):
        self.restore_geometry(zzapp.zz_app.settings)
        if event:
            event.accept()

    def closeEvent(self, event=None):
        self.close()
        if event:
            event.accept()
