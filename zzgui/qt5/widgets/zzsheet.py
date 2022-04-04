import enum
import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from PyQt5.QtWidgets import QTableWidget, QSizePolicy


from zzgui.qt5.zzwidget import ZzWidget


class zzsheet(QTableWidget, ZzWidget):
    def __init__(self, meta):
        super().__init__({"label": meta.get("label", "")})
        self.column_headers = []
        self.row_headers = []
        self.horizontalHeader().setMinimumSectionSize(0)
        self.verticalHeader().setMinimumSectionSize(0)
        self.auto_expand = False

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
        # self.setFixedWidth(0)
        # self.setFixedHeight(0)

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

    def set_column_size(self, column, size):
        self.setColumnWidth(column, size)
        self.expand()

    def set_column_sizes(self, sizes=[]):
        if isinstance(sizes, list):
            for column, size in enumerate(sizes):
                self.set_column_size(column, size)
        elif isinstance(sizes, int):
            for x in range(self.columnCount()):
                self.set_column_size(x, sizes)
        self.expand()

    def set_row_size(self, row, size):
        self.setRowHeight(row, size)
        self.expand()

    def set_row_sizes(self, sizes=[]):
        if isinstance(sizes, list):
            for row, size in enumerate(sizes):
                self.set_row_size(row, size)
        elif isinstance(sizes, int):
            for x in range(self.rowCount()):
                self.set_row_size(x, sizes)
        self.expand()

    def set_span(self, row, column, row_span, column_span):
        self.setSpan(row, column, row_span, column_span)
        self.expand()
