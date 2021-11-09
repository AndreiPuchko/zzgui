import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QTextEdit
import zzgui.zz_qt5.widget as zzwiddet


class text(QTextEdit, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__()
        self.meta = meta
        self.set_text(meta.get('data'))

    def set_text(self, text):
        self.setHtml(text)

    def get_text(self):
        return f"{self.toPlainText()}"
