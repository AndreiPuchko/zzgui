import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from zzgui.qt5.zzwindow import zz_align

from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QRadioButton, QSizePolicy

from zzgui.qt5.zzwidget import ZzWidget


class zzradio(QFrame, ZzWidget):
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
    def __init__(self, text, radio: zzradio):
        super().__init__(text)
        self.radio = radio

    def get_text(self):
        return f"{self.radio.button_list.index(self)}"
