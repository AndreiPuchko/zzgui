import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QComboBox

from zzgui.qt5.zzwidget import ZzWidget


class zzcombo(QComboBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.meta = meta
        for item in meta.get("pic", "").split(";"):
            self.addItem(item)

    def get_text(self):
        return self.currentText()
