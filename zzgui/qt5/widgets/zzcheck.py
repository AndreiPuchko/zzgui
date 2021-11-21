import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QCheckBox

from zzgui.qt5.zzwidget import ZzWidget

class zzcheck(QCheckBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setText(meta['label'])

    def set_text(self, text):
        self.setChecked(True if text else False)
