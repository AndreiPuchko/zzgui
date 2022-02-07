if __name__ == "__main__":

    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QGroupBox, QSplitter, QSizePolicy
from PyQt5.QtCore import Qt


from zzgui.qt5.zzwindow import ZzFrame
from zzgui.qt5.zzwidget import ZzWidget


class zzframe(QGroupBox, ZzWidget, ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        ZzFrame.__init__(self, meta.get("name", "/v")[1])
        self.splitter = None
        if meta.get("name", "")[2:3] == "s":  # Splitter!
            self.splitter = zzsplitter()
            if meta.get("name").startswith("/v"):
                self.splitter.setOrientation(Qt.Orientation.Vertical)
            self.layout().addWidget(self.splitter)
        if meta.get("label"):
            self.set_title(meta.get("label"))

    def hide_border(self):
        self.setObjectName("grb")
        self.setStyleSheet("QGroupBox#grb {border:0}")
        self.set_title("")

    def set_title(self, title):
        self.setTitle(title)

    def get_widget_count(self):
        return self.layout().count()

    def add_widget(self, widget=None, label=None):
        if self.splitter is not None:
            self.splitter.addWidget(widget)
            if hasattr(widget, "meta"):
                # print(widget.meta.get("stretch"), widget)
                self.splitter.setStretchFactor(self.splitter.count()-1, widget.meta.get("stretch", 0))
            # if hasattr(widget, "meta"):
            #     if "toolbar" in widget.meta.get("name", ""):
            #         widget.set_context_menu(self.splitter)
        else:
            return super().add_widget(widget=widget, label=label)


class zzsplitter(QSplitter):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    def get_sizes(self):
        return ",".join([f"{x}" for x in self.sizes()])

    def set_sizes(self, sizes):
        if sizes:
            sizes = [int(x) for x in sizes.split(",")]
            self.setSizes(sizes)
