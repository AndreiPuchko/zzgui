if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from zzgui import zzmodel

class ZzModel(zzmodel.ZzModel):
    def refresh(self):
        self.beginResetModel()
        self.endResetModel()
        return super().refresh()
