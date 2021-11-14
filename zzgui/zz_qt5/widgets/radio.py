import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet
from zzgui.zz_qt5.window import zz_align

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QRadioButton, QSizePolicy


class radio(QFrame, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setLayout(QVBoxLayout() if "v" in meta.get("control") else QHBoxLayout())
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.layout().setAlignment(zz_align["7"])
        self.button_list = []
        # self.meta = meta
        for item in meta.get("pic", "").split(";"):
            self.button_list.append(zzRadioButton(item, self))
            self.layout().addWidget(self.button_list[-1])
        self.button_list[0].setChecked(True)


class zzRadioButton(QRadioButton):
    def __init__(self, text, radio: radio):
        super().__init__(text)
        self.radio = radio

    def get_text(self):
        return f"{self.radio.button_list.index(self)}"
       
