if __name__ == "__main__":

    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QGroupBox, QSplitter, QSizePolicy
from PyQt5.QtCore import Qt

from zzgui.zzutils import num
import zzgui.zz_qt5.widget as zzwiddet
import zzgui.zz_qt5.window as zzwindow


class frame(QGroupBox, zzwiddet.ZzWidget, zzwindow.ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        zzwindow.ZzFrame.__init__(self, meta.get("name", "/v")[1])
        self.splitter = None
        if meta.get("name", "")[2:3] == "s":  # Splitter!
            self.splitter = splitter()
            if meta.get("name").startswith("/v"):
                self.splitter.setOrientation(Qt.Orientation.Vertical)
            self.layout().addWidget(self.splitter)
        if meta.get("label"):
            self.setTitle(meta.get("label"))

    def add_widget(self, widget=None, label=None):
        if self.splitter is not None:
            self.splitter.addWidget(widget)
            if hasattr(widget, "meta"):
                if "toolbar" in widget.meta.get("name", ""):
                    widget.set_context_menu(self.splitter)
        else:
            return super().add_widget(widget=widget, label=label)


class splitter(QSplitter):
    def __init__(self):
        super().__init__()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

    def get_sizes(self):
        return ",".join([f"{x}" for x in self.sizes()])

    def set_sizes(self, sizes):
        if sizes:
            sizes = [int(x) for x in sizes.split(",")]
            self.setSizes(sizes)
