import enum
import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTableWidget, QSizePolicy
from PyQt5.QtCore import Qt


from zzgui.qt5.zzwidget import ZzWidget
from zzgui.qt5.widgets.zzlabel import zzlabel

from zzgui.zzutils import num


class zzsheet(QTableWidget, ZzWidget):
    def __init__(self, meta):
        # super().__init__({"label": meta.get("label", "")})
        super().__init__(meta)
        self.column_headers = []
        self.row_headers = []
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setMinimumSectionSize(0)
        self.auto_expand = False
        self.setEditTriggers(self.NoEditTriggers)

        if self.meta.get("when"):
            self.clicked.connect(self.meta.get("when"))

        if self.meta.get("valid"):
            self.currentCellChanged.connect(self.meta.get("valid"))

    def set_auto_expand(self, mode=True):
        self.auto_expand = mode

    def expand(self):
        if self.auto_expand:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum))
            height = self.horizontalHeader().height() + 0
            for x in range(self.rowCount()):
                height += self.rowHeight(x)
            self.setFixedHeight(height)

            width = self.verticalHeader().width() + 0
            for x in range(self.columnCount()):
                width += self.columnWidth(x)
            self.setFixedWidth(width)
        else:
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            self.setMinimumWidth(0)
            self.setMinimumHeight(0)

    def set_row_count(self, row=2):
        self.setRowCount(row)
        self.expand()

    def set_column_count(self, column=2):
        self.setColumnCount(column)
        self.expand()

    def set_row_column_count(self, row=2, column=2):
        self.set_row_count(row)
        self.set_column_count(column)
        self.expand()

    def set_column_headers(self, headers_list=[]):
        self.column_headers = headers_list
        self.setHorizontalHeaderLabels(self.column_headers)
        self.expand()

    def set_row_headers(self, headers_list=[]):
        self.row_headers = headers_list
        self.setVerticalHeaderLabels(self.row_headers)
        self.expand()

    def set_column_header(self, column=0, header=""):
        if column >= self.columnCount():
            return

        if not column < len(self.column_headers):
            for x in range(len(self.column_headers), self.columnCount()):
                self.column_headers.append("")
        self.column_headers[column] = header
        self.set_column_headers(self.column_headers)
        self.expand()

    def set_row_header(self, row=0, header=""):
        if row >= self.rowCount():
            return
        if not row < len(self.row_headers):
            for x in range(len(self.row_headers) - 1, self.rowCount()):
                self.row_headers.append("")
        self.row_headers[row] = header
        self.set_row_headers(self.row_headers)
        self.expand()

    def hide_column_headers(self):
        self.horizontalHeader().hide()
        self.expand()

    def show_column_headers(self):
        self.horizontalHeader().show()
        self.expand()

    def hide_row_headers(self):
        self.verticalHeader().hide()
        self.expand()

    def show_row_headers(self):
        self.verticalHeader().show()
        self.expand()

    def set_column_size(self, width=[], column=None):
        if isinstance(width, list):
            for column, size in enumerate(width):
                self.set_column_size(size, column)
        elif isinstance(width, int) and column is None:
            for x in range(self.columnCount()):
                self.set_column_size(width, x)
        else:
            self.setColumnWidth(column, width)
        self.expand()

    def set_row_size(self, heights=[], row=None):
        if isinstance(heights, list):
            for row, size in enumerate(heights):
                self.set_row_size(size, row)
        elif isinstance(heights, int) and row is None:
            for x in range(self.rowCount()):
                self.set_row_size(heights, x)
        else:
            self.setRowHeight(row, heights)
        self.expand()

    def set_span(self, row, column, row_span, column_span):
        self.setSpan(row, column, row_span, column_span)
        self.expand()

    def set_cell_text(self, text="", row=None, column=None):
        if isinstance(text, list):
            if row is None and column is None:
                row = 0
            if row is not None:
                for x in range(self.columnCount()):
                    if x < len(text):
                        self.set_cell_text(text[x], row, x)
            else:
                for x in range(self.rowCount()):
                    if x < len(text):
                        self.set_cell_text(text[x], x, column)
        else:
            row = num(row)
            column = num(column)
            cell_widget = self.get_cell_widget(row, column)
            cell_widget.setText(text)

    def set_cell_style(self, style_text="", row=None, column=None):
        if row is None and column is None:
            row = 0
        if row is not None and column is None:
            for x in range(self.columnCount()):
                if isinstance(style_text, dict):
                    if x < len(style_text):
                        self.set_cell_style(style_text[x], row, x)
                else:
                    self.set_cell_style(style_text, row, x)
        elif row is None and column is not None:
            for x in range(self.rowCount()):
                if isinstance(style_text, dict):
                    if x < len(style_text):
                        self.set_cell_style(style_text[x], x, column)
                else:
                    self.set_cell_style(style_text, x, column)
        else:
            row = num(row)
            column = num(column)
            cell_widget = self.get_cell_widget(row, column)
            cell_widget.set_style_sheet(style_text)

    def get_cell_widget(self, row, column):
        cell_widget = self.cellWidget(row, column)
        if cell_widget is None:
            cell_widget = zzlabel()
            cell_widget.set_maximum_height(9999)
            self.setCellWidget(row, column, cell_widget)
        return cell_widget
