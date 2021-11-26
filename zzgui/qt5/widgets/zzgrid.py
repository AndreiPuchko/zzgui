import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import (
    QTableView,
    QStyledItemDelegate,
    QAbstractItemView,
)
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import pyqtSignal, Qt, QAbstractTableModel, QVariant

from zzgui.qt5.zzwindow import zz_align
from zzgui.zzutils import num
from zzgui.zzform import ZzForm
from zzgui.zzmodel import ZzModel


class zzDelegate(QStyledItemDelegate):
    # def displayText(self, value, locale):
    #     return super().displayText(value, locale)

    def paint(self, painter, option, index):
        if self.parent().currentIndex().column() == index.column():
            color = option.palette.color(QPalette.AlternateBase).darker(900)
            color.setAlpha(color.alpha() / 10)
            painter.fillRect(option.rect, color)
        super().paint(painter, option, index)


class zzgrid(QTableView):
    class ZzTableModel(QAbstractTableModel):
        def __init__(self, zz_model):
            super().__init__(parent=None)
            self.zz_model: ZzModel = zz_model
            self.zz_model.refresh = self.refresh

        def set_order(self, column):
            self.zz_model.order_column(column)

        def rowCount(self, parent=None):
            return self.zz_model.row_count()

        def columnCount(self, parent=None):
            return self.zz_model.column_count()

        def refresh(self):
            self.beginResetModel()
            self.endResetModel()

        def data(self, index, role=Qt.DisplayRole):
            if role == Qt.DisplayRole:
                return QVariant(self.zz_model.data(index.row(), index.column()))
            elif role == Qt.TextAlignmentRole:
                return QVariant(zz_align[str(self.zz_model.alignment(index.column()))])
            else:
                return QVariant()

        def headerData(self, col, orientation, role=Qt.DisplayRole):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.zz_model.headers[col]
            elif orientation == Qt.Vertical and role == Qt.DisplayRole:
                return QVariant(" ")
            else:
                return QVariant()

    currentCellChangedSignal = pyqtSignal(int, int)

    def __init__(self, zz_form: ZzForm):
        super().__init__()
        self.zz_form = zz_form
        self.setModel(self.ZzTableModel(self.zz_form.model))
        self.setItemDelegate(zzDelegate(self))
        self.setTabKeyNavigation(False)

        self.horizontalHeader().setSectionsMovable(True)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.horizontalHeader().setDefaultAlignment(zz_align["7"])
        self.doubleClicked.connect(self.zz_form.grid_double_clicked)
        self.horizontalHeader().sectionClicked.connect(self.zz_form.grid_header_clicked)

    def currentChanged(self, current, previous):
        self.currentCellChangedSignal.emit(current.row(), current.column())
        super().currentChanged(current, previous)
        self.model().dataChanged.emit(current, previous)
        self.zz_form.grid_index_changed(
            self.currentIndex().row(), self.currentIndex().column()
        )

    def current_index(self):
        return self.currentIndex().row(), self.currentIndex().column()

    def set_focus(self):
        self.setFocus()

    def row_count(self):
        return self.model().rowCount()

    def column_count(self):
        return self.model().columnCount()

    def set_index(self, row, col):
        if row < 0:
            row = 0
        elif row > self.row_count() - 1:
            row = self.row_count() - 1
        if col < 0:
            col = 0
        elif col > self.column_count() - 1:
            col = self.column_count() - 1
        self.setCurrentIndex(self.model().index(row, col))

    def keyPressEvent(self, event):
        event.accept()
        # if ev.key() in [Qt.Key_F] and ev.modifiers() == Qt.ControlModifier:
        #     self.searchText()
        # if event.key() in [Qt.Key_Asterisk]:
        if (
            event.text()
            and event.key() not in (Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return)
            and self.model().rowCount() >= 0
        ):
            # lpb = zzGridLookUpBox(self, event.text())
            # lpb.show()
            pass
            # col = self.grid.currentIndex().column()
            # colName = self.model().columns[col].upper()

        else:
            super().keyPressEvent(event)

    def get_columns_headers(self):
        rez = {}
        hohe = self.horizontalHeader()
        for x in range(0, hohe.count()):
            rez[hohe.model().headerData(x, Qt.Horizontal, Qt.DisplayRole)] = x
        return rez

    def get_columns_settings(self):
        rez = []
        hohe = self.horizontalHeader()
        for x in range(0, hohe.count()):
            header = hohe.model().headerData(x, Qt.Horizontal, Qt.DisplayRole)
            width = self.columnWidth(x)
            pos = hohe.visualIndex(x)
            rez.append({"name": header, "data": f"{pos}, {width}"})
        return rez

    def set_column_settings(self, col_settings):
        headers = self.get_columns_headers()
        for x in col_settings:
            if "," not in col_settings[x]:
                continue
            column_pos = num(col_settings[x].split(",")[0])
            column_width = num(col_settings[x].split(",")[1])
            self.setColumnWidth(headers.get(x), column_width)
            old_visual = self.horizontalHeader().visualIndex(num(headers[x]))
            self.horizontalHeader().moveSection(old_visual, column_pos)
