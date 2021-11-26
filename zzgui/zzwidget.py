if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


class ZzWidget:
    def __init__(self, meta={}):
        self.meta = meta
        self.form = None
        self.label = None
        self.check = None
        # print("ddd", meta)
        if self.meta.get("readonly"):
            self.set_readonly(True)
        if self.meta.get("disabled"):
            self.set_disabled(True)
        if self.meta.get("mess"):
            self.set_tooltip(self.meta.get("mess"))
        # if hasattr(self, "setToolTip") and self.meta.get("mess"):
        #     self.setToolTip(self.meta.get("mess"))
        # if self.meta.get("zzForm"):
        #     self.zzForm = meta["zzForm"]
        if hasattr(self, "set_text") and self.meta.get("data"):
            self.set_text(self.meta.get("data"))

    def set_readonly(self, arg):
        pass

    def set_disabled(self, arg=True):
        self.set_enabled(not arg)

    def set_enabled(self, arg=True):
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
