import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QDoubleSpinBox

from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import int_, float_


class zzdoublespin(QDoubleSpinBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        self.setDecimals(int_(meta.get("datadec", 1)))
        self.set_text(meta.get("data"))
        self.setSingleStep(0.05)
        if self.meta.get("valid"):
            self.valueChanged.connect(self.meta.get("valid"))

    def set_text(self, text):
        self.setValue(float_(text))

    def get_text(self):
        return self.text().replace(",", ".")

    def set_maximum_width(self, width, char="O"):
        return super().set_maximum_width(width, "W")
