import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QRadioButton, QSizePolicy

from zzgui.qt5.zzwindow import zz_align
from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import int_


class zzradio(QFrame, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setLayout(QVBoxLayout() if "v" in meta.get("control") else QHBoxLayout())
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.layout().setAlignment(zz_align["7"])
        self.layout().setSpacing(0)
        self.button_list = []
        for item in meta.get("pic", "").split(";"):
            button = zzRadioButton(item, self)
            # button.toggled.connect(lambda: print(self.get_text(), button))
            self.button_list.append(button)
            self.layout().addWidget(button)

        self.button_list[0].setChecked(True)

    def set_text(self, text):
        if hasattr(self, "button_list"):
            if self.meta.get("num"):
                index = int_(text)
                index = index - 1 if index else 0
            else:
                index_list = [
                    x for x in range(len(self.button_list)) if self.button_list[x].get_text() == text
                ]
                if index_list:
                    index = index_list[0]
                else:
                    index = 0
            self.button_list[index].setChecked(True)

    def get_text(self):
        index_list = [x for x in range(len(self.button_list)) if self.button_list[x].isChecked()]
        if index_list:
            index = index_list[0]
            if self.meta.get("num"):
                return str(index + 1)
            else:
                return self.button_list[index].get_text()
        else:
            return ""


class zzRadioButton(QRadioButton):
    def __init__(self, text, radio: zzradio):
        super().__init__(text)
        self.radio = radio
        self.toggled.connect(self.value_changed)

    def value_changed(self, value):
        if value:
            if self.radio.meta.get("valid"):
                self.radio.meta.get("valid")()
        else:
            if self.radio.meta.get("when"):
                self.radio.meta.get("when")()

    def get_text(self):
        return self.text()
