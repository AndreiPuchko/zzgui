import sys


if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zzform as zzform
from zzgui.zz_qt5.app import ZzQtWindow

from zzgui.zz_qt5.widgets import *

from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFormLayout
import zzgui.zzapp as zzapp
from zzgui.utils import num


class ZzForm(zzform.ZzForm, ZzQtWindow, QDialog):
    def __init__(self, title=""):
        super().__init__(title=title)
        self._widgets_package = __import__("zzgui.zz_qt5.widgets",None,None,[""])

    def show_form(self, modal="modal"):
        self.setLayout(zzapp.zz_app.zz_layout("v"))
        layoutList = [self.layout()]
        for meta in self.controls:
            currentLayout = layoutList[-1]
            label2add, widget2add = self.widget(meta)
            if isinstance(currentLayout, QFormLayout):
                currentLayout.addRow(label2add, widget2add)
            else:
                if label2add:
                    currentLayout.addWidget(label2add)
                if widget2add:
                    currentLayout.addWidget(widget2add)

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
        if self.shown:
            return
        self.restore_geometry(zzapp.zz_app.settings)
        self.shown = True
        if event:
            event.accept()

    def closeEvent(self, event=None):
        self.close()
        if event:
            event.accept()
