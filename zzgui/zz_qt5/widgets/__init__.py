import pkgutil

from zzgui.zz_qt5.widgets import label
from zzgui.zz_qt5.widgets import line
from zzgui.zz_qt5.widgets import frames
from zzgui.zz_qt5.widgets import check

# Import forgotten widgets
for x in pkgutil.iter_modules(["zzgui/zz_qt5/widgets"]):
    if x.name not in locals():
        zz = f"zzgui/zz_qt5/widgets/{x.name}".replace("/", ".")
        locals()[f"{x.name}"] = __import__(zz, None, None, [""])

