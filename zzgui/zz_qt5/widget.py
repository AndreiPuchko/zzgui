if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from PyQt5.QtWidgets import QWidget
from zzgui.zzwidget import ZzWidget


class ZzWidget(QWidget, ZzWidget):
    def set_readonly(self, arg):
        if arg:
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    def set_enabled(self, arg=True):
        if arg:
            self.setEnabled(True)
        else:
            self.setEnabled(True)

    def set_text(self, text):
        if hasattr(self, "setText"):
            self.setText(text)

    def get_text(self, text):
        if hasattr(self, "text"):
            return self.text()
        return ""
