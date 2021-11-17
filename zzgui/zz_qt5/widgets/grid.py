import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet

from PyQt5.QtWidgets import QTableView, QStyledItemDelegate, QAbstractItemView, QWidget
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import pyqtSignal, Qt, QAbstractTableModel, QVariant
from zzgui.zz_qt5.window import zz_align


class zzDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        return super().displayText(value, locale)

    def paint(self, painter, option, index):
        if self.parent().currentIndex().column() == index.column():
            color = option.palette.color(QPalette.AlternateBase).darker(200)
            color.setAlpha(color.alpha() / 10)
            painter.fillRect(option.rect, color)
        super().paint(painter, option, index)


class grid(QTableView):
    class ZzTableModel(QAbstractTableModel):
        def __init__(self, zz_model):
            super().__init__(parent=None)
            self.zz_model = zz_model

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

    def __init__(self, zz_form):
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

    def currentChanged(self, current, previous):
        self.currentCellChangedSignal.emit(current.row(), current.column())
        super().currentChanged(current, previous)
        self.model().dataChanged.emit(current, previous)

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
            # if colName in self.model().zzTable.fields() and self.model().zzTable.tableName() in self.model().zzTable.zzDb.tables or 1:
        else:
            super().keyPressEvent(event)


class zzGridLookUpBox(QWidget):
    def __init__(self, zzGrid, text):
        super().__init__(zzGrid, Qt.Popup)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.col = zzGrid.currentIndex().column()
        self.zzGrid = zzGrid
        self.setLayout(zzApp.zzApp.layout("v"))
        self.le = zzLineEdit({"datalen": 99})
        self.lw = zzListWidget({"datalen": 99})
        self.lw.itemActivated.connect(self.lwSelected)
        self.layout().addWidget(self.le)
        self.layout().addWidget(self.lw)
        self.le.setFocus()
        self.le.setText(text)
        self.searchResult = []

        self.colName = self.zzGrid.zzForm.model.columns[self.zzGrid.zzForm.currentCol]
        pkCol = self.zzGrid.zzForm.t.getPkColumns()
        self.pkName = self.zzGrid.zzForm.t.getPkColumns()[0] if pkCol else None

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.doSearch)

        self.setSelfSizeAndPos()

        self.le.returnPressed.connect(self.leReturnPressed)
        self.le.textChanged.connect(self.leTextChanged)

    def leReturnPressed(self):
        self.timer.stop()
        self.doSearch()

    def leTextChanged(self):
        self.timer.start(550)

    def lwSelected(self):
        self.zzGrid.zzForm.setGridIndex(
            self.zzGrid.zzForm.t.getPkRow(
                self.searchResult[self.lw.currentIndex().row()]
            )
        )
        self.close()

    def doSearch(self):
        self.searchResult = self.zzGrid.zzForm.gridColumnSearch(self.le.text())
        self.lw.clear()
        for x in self.searchResult:
            self.lw.addItem(f"{x[self.colName]} ({x[self.pkName]})")

    def keyPressEvent(self, ev):
        if ev.key() in [Qt.Key_Down]:
            ev.accept()
            self.lw.setCurrentRow(0)
            self.focusNextChild()
        if ev.key() in [Qt.Key_Up]:
            if self.lw.hasFocus() and self.lw.currentRow() == 0:
                ev.accept()
                self.focusPreviousChild()
        super().keyPressEvent(ev)

    def setSelfSizeAndPos(self):
        # Установка размеров и положения всплывающего окна
        rect = self.zzGrid.visualRect(self.zzGrid.currentIndex())
        rect.moveTop(self.zzGrid.horizontalHeader().height() + 2)
        rect.moveLeft(self.zzGrid.verticalHeader().width() + rect.x() + 2)
        pos = rect.topLeft()
        pos = self.zzGrid.mapToGlobal(pos)
        self.setFixedWidth(self.zzGrid.width() - rect.x())
        self.move(pos)
