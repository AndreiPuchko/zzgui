import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


from PyQt5.QtWidgets import (
    QTableView,
    QStyledItemDelegate,
    QAbstractItemView,
    QStyle,
    QStyleOptionButton,
    QApplication,
)
from PyQt5.QtGui import QPalette, QPainter

from PyQt5.QtCore import Qt, QAbstractTableModel, QVariant

from zzgui.qt5.zzwindow import zz_align
from zzgui.zzutils import int_
from zzgui.zzmodel import ZzModel
from zzgui.qt5.widgets.zzlookup import zzlookup


class zzDelegate(QStyledItemDelegate):
    def paint(self, painter: QPainter, option, index):
        if self.parent().currentIndex().column() == index.column():
            color = option.palette.color(QPalette.AlternateBase).darker(900)
            color.setAlpha(color.alpha() / 10)
            painter.fillRect(option.rect, color)
        meta = self.parent().model().zz_model.meta[index.column()]
        if meta.get("control") == "check":
            self.paint_checkbox(painter, option, index, meta)
            return
        # elif meta.get("relation"):
        #     super().paint(painter, option, index)
        #     self.paint_relation_button(painter, option, index, meta)
        #     return
        super().paint(painter, option, index)

    # def paint_relation_button(self, painter: QPainter, option, index, meta):
    #     pb_option = QStyleOptionButton()
    #     pb_option.text = "?"
    #     checkBoxRect = QApplication.style().subElementRect(QStyle.SE_PushButtonBevel, pb_option, None)
    #     sz = 30
    #     pb_option.rect = option.rect
    #     pb_option.rect.setX(pb_option.rect.x() - sz + option.rect.width())
    #     print(checkBoxRect.height())
    #     pb_option.rect.setHeight(sz)
    #     pb_option.rect.setWidth(sz)
    #     QApplication.style().drawControl(QStyle.CE_PushButton, pb_option, painter)

    def paint_checkbox(self, painter: QPainter, option, index, meta):
        """paint checkbox - left - with top+left alignment"""
        if meta.get("num"):
            checked = True if int_(index.data()) else False
        else:
            checked = True if index.data() else False
        cb_option = QStyleOptionButton()
        if checked:
            cb_option.state |= QStyle.State_On
        else:
            cb_option.state |= QStyle.State_Off
        checkBoxRect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, cb_option, None)
        cb_option.rect = option.rect
        cb_option.rect.setX(cb_option.rect.x() + checkBoxRect.width() / 2)
        if cb_option.rect.height() > checkBoxRect.height() * 2 + 3:
            cb_option.rect.setHeight(checkBoxRect.height() * 2)
        QApplication.style().drawControl(QStyle.CE_CheckBox, cb_option, painter)


class zzgrid(QTableView):
    class ZzTableModel(QAbstractTableModel):
        def __init__(self, zz_model):
            super().__init__(parent=None)
            self.zz_model: ZzModel = zz_model
            self._zz_model_refresh = self.zz_model.refresh
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
            self._zz_model_refresh()

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
                return QVariant("")
            else:
                return QVariant()

    # currentCellChangedSignal = pyqtSignal(int, int)

    def __init__(self, meta):
        super().__init__()
        self.meta = meta

        self.zz_form = self.meta.get("form")
        self.zz_model = self.zz_form.model

        # self.setModel(self.ZzTableModel(self.zz_form.model))
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
        self.setModel(self.ZzTableModel(self.zz_form.model))

    def currentChanged(self, current, previous):
        # self.currentCellChangedSignal.emit(current.row(), current.column())
        super().currentChanged(current, previous)
        self.model().dataChanged.emit(current, previous)
        self.zz_form.grid_index_changed(self.currentIndex().row(), self.currentIndex().column())

    def current_index(self):
        return self.currentIndex().row(), self.currentIndex().column()

    def set_focus(self):
        self.setFocus()

    def row_count(self):
        return self.model().rowCount()

    def column_count(self):
        return self.model().columnCount()

    def set_index(self, row, column=None):
        if row < 0:
            row = 0
        elif row > self.row_count() - 1:
            row = self.row_count() - 1

        if column is None:
            column = self.currentIndex().column()
        elif column < 0:
            column = 0
        elif column > self.column_count() - 1:
            column = self.column_count() - 1

        self.setCurrentIndex(self.model().index(row, column))

    def keyPressEvent(self, event):
        event.accept()
        # if ev.key() in [Qt.Key_F] and ev.modifiers() == Qt.ControlModifier:
        #     self.searchText()
        # if event.key() in [Qt.Key_Asterisk]:
        if (
            event.text()
            and event.key() not in (Qt.Key_Escape, Qt.Key_Enter, Qt.Key_Return, Qt.Key_Space)
            and self.model().rowCount() >= 1
            and event.modifiers() != Qt.ControlModifier
            and event.modifiers() != Qt.AltModifier
        ):
            lookup_widget = zz_grid_lookup(self, event.text())
            lookup_widget.show(self, self.currentIndex().column())
        else:
            super().keyPressEvent(event)

    def get_selected_rows(self):
        return [x.row() for x in self.selectionModel().selectedRows()]

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
            column_pos = int_(col_settings[x].split(",")[0])
            column_width = int_(col_settings[x].split(",")[1])
            # column_width = column_width if column_width else 10
            self.setColumnWidth(headers.get(x), column_width)
            old_visual = self.horizontalHeader().visualIndex(int_(headers[x]))
            self.horizontalHeader().moveSection(old_visual, column_pos)
        self.set_index(0, self.horizontalHeader().logicalIndex(0))


class zz_grid_lookup(zzlookup):
    def lookup_list_selected(self):
        self.zz_grid.set_index(self.found_rows[self.lookup_list.currentRow()][0])
        self.close()

    def lookup_search(self):
        self.lookup_list.clear()
        self.found_rows = self.zz_model.lookup(self.zz_model_column, self.lookup_edit.get_text())
        for x in self.found_rows:
            self.lookup_list.addItem(f"{x[1]}")

    def show(self, zz_grid, column):
        self.zz_grid = zz_grid
        self.zz_model_column = column
        self.zz_model = zz_grid.zz_model
        return super().show()

    def set_geometry(self):
        parent = self.parent()
        rect = parent.visualRect(parent.currentIndex())
        rect.moveTop(parent.horizontalHeader().height() + 2)
        rect.moveLeft(parent.verticalHeader().width() + rect.x() + 2)
        pos = rect.topLeft()
        pos = parent.mapToGlobal(pos)
        self.setFixedWidth(parent.width() - rect.x())
        self.move(pos)
