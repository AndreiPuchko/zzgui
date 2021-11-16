import pkgutil

from zzgui.zz_qt5.widgets import (
    label,
    line,
    frames,
    check,
    toolbar,
    tab,
    text,
    button,
    radio,
    toolbutton,
    combo,
    date,
    space,
    list,
    spin,
    
)


# Import forgotten widgets
for x in pkgutil.iter_modules(["zzgui/zz_qt5/widgets"]):
    if x.name not in locals():
        zz = f"zzgui/zz_qt5/widgets/{x.name}".replace("/", ".")
        locals()[f"{x.name}"] = __import__(zz, None, None, [""])
