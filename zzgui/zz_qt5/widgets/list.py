import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet
from PyQt5.QtWidgets import QListWidget, QListWidgetItem


class list(QListWidget, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        for item in meta.get("pic", "").split(";"):
            self.addItem(QListWidgetItem(item))
    def get_text(self):
        return self.currentItem().text()
