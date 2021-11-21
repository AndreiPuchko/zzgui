import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QLabel


from zzgui.qt5.zzwidget import ZzWidget


class zzlabel(QLabel, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        # self.meta = meta
        self.set_text(meta["label"])
