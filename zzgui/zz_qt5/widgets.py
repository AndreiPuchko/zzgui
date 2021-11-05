from zzgui import ZzApp
from zzgui import ZzWindow

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QToolBar

# from PyQt5.Qsci import *


class ZzQtWindow(ZzWindow):
    def set_position(self, left, top):
        self.move(left, top)

    def set_size(self, width, height):
        self.resize(width, height)

    def get_position(self):
        return (self.pos().x(), self.pos().y())

    def get_size(self):
        return (self.size().width(), self.size().height())


class ZzQtApp(ZzApp):
    def run(self):
        self._core_app = QApplication([])
        self.main_widget = ZzMainWindow(self)
        super().run()
        self.main_widget.show()
        self._core_app.exec_()


class ZzMainWindow(ZzQtWindow, QMainWindow):
    def __init__(self, zz_app):
        super().__init__()
        # self.engine = engine
        # self.centralWidget().setLayout(self.engine.layout("v"))

        # self.tabWidget = tabWidget()
        # self.tabWidget.addTab()
        # self.tabWidget.setCurrentIndex(0)

        # self.centralWidget().layout().addWidget(self.toolBoxFrame)
        # self.centralWidget().layout().addWidget(self.tabWidget)
        self.zz_app = zz_app
        self.toolBoxFrame = QToolBar()
        self.setCentralWidget(QWidget())

        self.statusBar().setVisible(True)

    def closeEvent(self, e):
        # if zzApp.zzApp.engine.justClosed:
            # return
        self.zz_app.close()
        e.accept()
