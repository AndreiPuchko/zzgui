import pkgutil

for x in pkgutil.iter_modules(["zzgui/zz_qt5/widgets"]):
    zz = f"zzgui/zz_qt5/widgets/{x.name}".replace("/", ".")
    locals()[f"{x.name}"] = __import__(zz, None, None, [""])
