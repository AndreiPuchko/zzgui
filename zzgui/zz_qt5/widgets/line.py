import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QLineEdit
import zzgui.zz_qt5.widget as zzwiddet


class line(QLineEdit, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__()
        self.set_text(meta.get('data'))
