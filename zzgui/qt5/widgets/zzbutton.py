import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QPushButton, QSizePolicy

from zzgui.qt5.zzwidget import ZzWidget


class zzbutton(QPushButton, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        # self.meta = meta
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.set_text(meta.get("label"))
        if self.meta.get("valid"):
            self.clicked.connect(self.valid)
