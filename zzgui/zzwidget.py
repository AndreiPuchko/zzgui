if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


class ZzWidget:
    def __init__(self, meta={}):
        self.meta = meta
        self.form = None
        self.label = None
        self.check = None
        self.parentLayout = None
        if self.meta.get("readonly"):
            self.set_readonly(True)
        if self.meta.get("disabled"):
            self.set_disabled(True)
        # if hasattr(self, "setToolTip") and self.meta.get("mess"):
        #     self.setToolTip(self.meta.get("mess"))
        # if self.meta.get("zzForm"):
        #     self.zzForm = meta["zzForm"]
        if hasattr(self, "setText") and self.meta.get("data"):
            self.setText(self.meta.get("data"))

    def set_readonly(self, arg):
        pass

    def set_disabled(self, arg=True):
        self.set_enabled(not arg)

    def set_enabled(self, arg=True):
        pass

    def set_text(self):
        pass

    def get_text(self):
        pass
