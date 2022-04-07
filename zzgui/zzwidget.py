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
        self.style_sheet = ""
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
        if not self.meta.get("form"):
            return
        if not self.meta.get("form").form_is_active is True:
            return
        valid = self.meta.get("valid")
        if valid is not None:
            return valid()
        else:
            return True

    def when(self):
        when = self.meta.get("when", lambda: True)
        if when:
            return self.meta.get("when", lambda: True)()
        else:
            return True

    def set_maximum_len(self, length):
        pass

    def set_maximum_width(self, width):
        pass

    def set_fixed_width(self, width):
        pass

    def set_alignment(self, alignment):
        pass

    def set_style_sheet(self, css: str):
        if css.strip().startswith("{"):
            css = type(self).__name__ + css
        self.style_sheet = css

    def get_default_height(self):
        pass

    def set_maximum_height(self, height):
        pass

    def get_default_width(self):
        pass

    def set_size_policy(self, horizontal, vertical):
        pass
