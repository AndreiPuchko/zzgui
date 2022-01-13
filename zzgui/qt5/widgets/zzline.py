import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QLineEdit


from zzgui.qt5.zzwidget import ZzWidget


class zzline(QLineEdit, ZzWidget):
    pass
