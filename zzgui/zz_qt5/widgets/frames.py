if __name__ == "__main__":

    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()

from PyQt5.QtWidgets import QGroupBox
import zzgui.zz_qt5.widget as zzwiddet
import zzgui.zz_qt5.window as zzwindow


class frame(QGroupBox, zzwiddet.ZzWidget, zzwindow.ZzFrame):
    def __init__(self, meta):
        if meta.get("name")[:2] == "/h":
            mode = "h"
        elif meta.get("name")[:2] == "/v":
            mode = "v"
        elif meta.get("name")[:2] == "/f":
            mode = "f"
        super().__init__(mode=mode)
        if meta.get("label"):
            self.setTitle(meta.get("label"))
