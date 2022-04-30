import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QDoubleSpinBox

from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import int_


class zzdoublespin(QDoubleSpinBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        self.setDecimals(int_(meta.get("datadec", 1)))
        self.set_text(meta.get("data"))

    def set_text(self, text):
        self.setValue(int_(text))

    def set_maximum_width(self, width, char="O"):
        return super().set_maximum_width(width, "W")
