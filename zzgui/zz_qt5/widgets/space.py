import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
import zzgui.zz_qt5.widget as zzwiddet


class space(QFrame, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        # zzwiddet.ZzWidget.__init__(self, meta)
        # self.meta = meta
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setLayout(QHBoxLayout())
        self.layout().addStretch()
        
