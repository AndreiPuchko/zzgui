import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics

from zzgui.qt5.zzwidget import ZzWidget
from zzgui.zzutils import num

class zzbutton(QPushButton, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        # self.meta = meta
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.set_text(meta.get("label"))
        if self.meta.get("valid"):
            self.clicked.connect(self.valid)
        ml = num(self.meta.get("datalen"))
        if ml:
            self.setMinimumWidth(QFontMetrics(self.font()).width("W") * ml)

    def keyPressEvent(self, ev):
        if ev.key() in [Qt.Key_Enter, Qt.Key_Return] and not self.meta.get("eat_enter"):
            ev.accept()
            self.focusNextChild()
        else:
            super().keyPressEvent(ev)
