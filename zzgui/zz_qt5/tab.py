import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from PyQt5.QtWidgets import (
    QTabWidget,
    QTabBar,
    QWidget,
    QMdiArea,
    QToolButton,
    QSizePolicy,
)
from PyQt5.QtCore import Qt


class ZzTabWidget(QTabWidget):
    def __init__(self):
        super().__init__()
        # self.addTab(QWidget(), "")
        # self.removeTab(0)
        # create Add button
        self.addTab(QWidget(), "") 
        # self.addTabButton = QPushButton()
        self.addTabButton = QToolButton()
        self.addTabButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.addTabButton.setText("+")
        self.addTabButton.clicked.connect(self.addTab)
        self.tabBar().setTabButton(0, QTabBar.RightSide, self.addTabButton)
        self.tabBar().setTabEnabled(0, False)

        self.closeButton = QToolButton()
        self.closeButton.setText("x")
        self.closeButton.clicked.connect(self.closeSubWindow)
        self.setCornerWidget(self.closeButton)
        # self.currentChanged.connect(self._currentChanged)

        self.addTab()
        self.setCurrentIndex(0)

    # def _currentChanged(self, index: int):
    #     # bug path when subwindow in tab 0 lost focus if we close subwindow in other tab
    #     if index == 0 and self.currentWidget().subWindowList():
    #         self.currentWidget().subWindowList()[-1].setFocus()

    def closeSubWindow(self):
        currentTabIndex = self.currentIndex()
        if self.currentWidget().activeSubWindow():
            self.currentWidget().activeSubWindow().close()
        elif self.count() > 2:  # close tab if them >2
            self.setCurrentIndex(currentTabIndex - 1)
            self.removeTab(currentTabIndex)

    def addTab(self, widget=None, label="="):
        if not widget:
            widget = QMdiArea()
            widget.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)
            widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.insertTab(self.count() - 1, widget, label)
        self.setCurrentIndex(self.count() - 2)
