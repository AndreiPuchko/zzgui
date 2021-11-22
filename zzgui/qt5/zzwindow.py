if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QGridLayout

from PyQt5.QtCore import Qt

from zzgui import zzapp, zzwindow

zz_align = {
    "": Qt.AlignLeft | Qt.AlignTop,
    "1": Qt.AlignLeft | Qt.AlignBottom,
    "2": Qt.AlignHCenter | Qt.AlignBottom,
    "3": Qt.AlignRight | Qt.AlignBottom,
    "4": Qt.AlignLeft | Qt.AlignVCenter,
    "5": Qt.AlignHCenter | Qt.AlignVCenter,
    "6": Qt.AlignRight | Qt.AlignVCenter,
    "7": Qt.AlignLeft | Qt.AlignTop,
    "8": Qt.AlignHCenter | Qt.AlignTop,
    "9": Qt.AlignRight | Qt.AlignTop,
}


def layout(arg="h"):
    if arg.lower().startswith("v"):
        layout = QVBoxLayout()
        # layout = zzVBoxLayout()
        layout.setAlignment(zz_align["7"])
    elif arg.lower().startswith("f"):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight | Qt.AlignTop)
    elif arg.lower().startswith("g"):
        layout = QGridLayout()
    else:
        layout = QHBoxLayout()
        # layout = zzHBoxLayout()
        layout.setAlignment(zz_align["7"])
    layout.layout().setContentsMargins(0, 0, 0, 0)
    layout.layout().setSpacing(0)
    return layout


class ZzFrame(zzwindow.ZzFrame, QWidget):
    def set_mode(self, mode="v"):
        self.splitter = None
        super().set_mode(mode=mode)
        if self.layout() is not None:
            return
        self.setLayout(layout(mode))

    def insert_widget(self, pos=None, widget=None):
        # If toolbar - set context menu for parent widget
        if hasattr(widget, "meta"):
            if "toolbar" in widget.meta.get("name", ""):
                widget.set_context_menu(self)
        self.layout().addWidget(widget)

    def add_row(self, label=None, widget=None):
        self.layout().addRow(label, widget)


class ZzQtWindow(zzwindow.ZzWindow, ZzFrame):
    def __init__(self, title=""):
        super().__init__()
        self.set_title(title)

    def set_position(self, left, top):
        self.move(left, top)
        # self.move(100, 100)

    def set_size(self, width, height):
        self.resize(width, height)

    def get_position(self):
        return (self.pos().x(), self.pos().y())

    def get_size(self):
        if hasattr(self, "parent") and self.parent() is not None:
            return (self.parent().size().width(), self.parent().size().height())
        else:
            return (self.size().width(), self.size().height())

    def set_title(self, title):
        super().set_title(title)
        QWidget.setWindowTitle(self, title)

    def is_maximized(self):
        return 1 if QWidget.isMaximized(self) else 0

    def show_maximized(self):
        QWidget.showMaximized(self)