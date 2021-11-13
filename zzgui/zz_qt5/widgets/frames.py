if __name__ == "__main__":

    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QGroupBox
import zzgui.zz_qt5.widget as zzwiddet
import zzgui.zz_qt5.window as zzwindow


class frame(QGroupBox, zzwiddet.ZzWidget, zzwindow.ZzFrame):
    def __init__(self, meta):
        super().__init__(meta)
        zzwindow.ZzFrame.__init__(self, meta.get("name","/v")[1])
        if meta.get("label"):
            self.setTitle(meta.get("label"))
