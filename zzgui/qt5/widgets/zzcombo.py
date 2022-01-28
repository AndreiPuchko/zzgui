import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QComboBox

from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import int_


class zzcombo(QComboBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        for item in meta.get("pic", "").split(";"):
            self.addItem(item)

    def set_text(self, text):
        if self.meta.get("num"):
            index = int_(text)
            index = index - 1 if index else 0
        else:
            index_list = [x for x in range(self.count()) if self.itemText(x) == text]
            if index_list:
                index = index_list[0]
            else:
                index = 0
        self.setCurrentIndex(index)

    def get_text(self):
        if self.currentText():
            if self.meta.get("num"):
                return self.currentIndex() + 1
            else:
                return self.currentText()
        else:
            return ""
