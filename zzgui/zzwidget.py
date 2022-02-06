if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from zzgui.zzutils import num


class ZzWidget:
    def __init__(self, meta={}):
        self.meta = meta
        self.form = None
        self.label = None
        self.check = None
        if self.meta.get("readonly"):
            self.set_readonly(True)
        if self.meta.get("disabled"):
            self.set_disabled(True)
        if self.meta.get("mess"):
            self.set_tooltip(self.meta.get("mess"))
        if hasattr(self, "set_text") and self.meta.get("data"):
            self.set_text(self.meta.get("data"))

        max_width = max(num(self.meta.get("datalen", 0)), len(self.meta.get("pic", "")))
        if max_width:
            self.set_maximum_width(max_width)
        if max_width:
            self.set_maximum_len(max_width)

        self.set_alignment(self.meta.get("alignment", 7))

    def set_readonly(self, arg):
        pass

    def set_disabled(self, arg=True):
        self.set_enabled(not arg)

    def set_enabled(self, arg=True):
        pass

    def set_visible(self, arg=True):
        pass

    def set_tooltip(self, mess):
        pass

    def set_focus(self):
        pass

    def is_enabled(self):
        pass

    def set_text(self, text):
        pass

    def get_text(self):
        pass

    def valid(self):
        if self.meta.get("valid") is not None:
            return self.meta.get("valid")()
        else:
            return True

    def when(self):
        return self.meta.get("when", lambda: True)()

    def set_maximum_len(self, length):
        pass

    def set_maximum_width(self, width):
        pass

    def set_alignment(self, alignment):
        pass
