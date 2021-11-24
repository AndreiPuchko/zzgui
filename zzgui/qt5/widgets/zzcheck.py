import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QCheckBox

from zzgui.qt5.zzwidget import ZzWidget


class zzcheck(QCheckBox, ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setText(meta["label"])
        self.managed_widgets = []
        self.stateChanged.connect(self.state_changed)

    def state_changed(self):
        for x in self.managed_widgets:
            x.set_enabled(self.isChecked())
            if x.is_enabled():
                x.setFocus()
        self.valid()

    def add_managed_widget(self, widget):
        self.managed_widgets.append(widget)
        widget.check = self

    def remove_managed_widget(self, widget):
        if widget in self.managed_widgets:
            self.managed_widgets.pop(self.managed_widgets.index(widget))

    def set_text(self, text):
        self.setChecked(True if text else False)

    def get_text(self):
        return "*" if self.isChecked() else False

    def set_checked(self, mode=True):
        self.set_text(mode)

    def is_checked(self):
        return True if self.get_text() else False
