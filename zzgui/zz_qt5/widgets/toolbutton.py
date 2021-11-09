import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet

from PyQt5.QtWidgets import QToolButton, QSizePolicy


class toolbutton(QToolButton, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__()
        self.meta = meta
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.set_text(meta.get('label'))
        if self.meta.get("valid"):
            self.clicked.connect(self.valid)
