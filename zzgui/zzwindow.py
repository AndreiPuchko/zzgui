if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from zzgui.zzutils import num


class ZzFrame:
    def __init__(self, mode="v"):
        super().__init__()
        self.frame_mode = mode
        self.set_mode(self.frame_mode)
        self._widgets_list = []

    def set_mode(self, mode="v"):
        self.frame_mode = mode

    def add_widget(self, widget=None, label=None):
        if widget is None:
            return
        if self.frame_mode in ["v", "h"]:
            self.insert_widget(len(self._widgets_list), widget)

    def insert_widget(self, pos=None, widget=None):
        pass

    def add_row(self, label=None, widget=None):
        pass

    def swap_widgets(self, widget1, widget2):
        pass

    def move_widget(self, widget, direction="up"):
        pass


class ZzWindow(ZzFrame):
    def __init__(self, title=""):
        super().__init__()
        self.window_title = ""
        self.set_title(title)

    def set_title(self, title):
        self.window_title = title

    def set_position(self, left, top):
        pass

    def set_size(self, width, height):
        pass

    def get_position(self):
        pass

    def get_size(self):
        pass

    def is_maximized():
        pass

    def show_maximized():
        return 0

    def restore_geometry(self, settings):
        left = num(settings.get(self.window_title, "left", "0"))
        top = num(settings.get(self.window_title, "top", "0"))
        self.set_position(left, top)
        width = num(settings.get(self.window_title, "width", "800"))
        height = num(settings.get(self.window_title, "height", "600"))
        self.set_size(width, height)
        if num(settings.get(self.window_title, "is_max", "0")):
            self.show_maximized()

    def save_geometry(self, settings):
        settings.set(self.window_title, "is_max", f"{self.is_maximized()}")
        if not self.is_maximized():
            pos = self.get_position()
            if pos is not None:
                settings.set(self.window_title, "left", pos[0])
                settings.set(self.window_title, "top", pos[1])
            size = self.get_size()
            settings.set(self.window_title, "width", size[0])
            settings.set(self.window_title, "height", size[1])
        settings.write()
