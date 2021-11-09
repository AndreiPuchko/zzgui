import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet
from PyQt5.QtWidgets import QComboBox


class combo(QComboBox, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__()
        self.meta = meta
        for item in meta.get("pic", "").split(";"):
            self.addItem(item)
