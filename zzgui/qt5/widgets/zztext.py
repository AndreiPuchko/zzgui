import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTextEdit, QSizePolicy

from zzgui.qt5.zzwidget import ZzWidget


class zztext(QTextEdit, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.set_text(meta.get('data'))

    def set_text(self, text):
        self.setHtml(text)

    def get_text(self):
        return f"{self.toPlainText()}"
