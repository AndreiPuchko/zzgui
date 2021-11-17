import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QCheckBox
import zzgui.zz_qt5.widget as zzwiddet


class check(QCheckBox, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setText(meta['label'])

    def set_text(self, text):
        self.setChecked(True if text else False)
