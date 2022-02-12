if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


# from zzgui import zzform

import os


from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QToolButton,
    QToolBar,
    QFileDialog,
    QTabWidget,
    QTabBar,
    QMdiArea,
    QSizePolicy,
    qApp,
)

from PyQt5.QtCore import QEvent, Qt, QCoreApplication, QTimer
from PyQt5.QtGui import QFontMetrics

from zzgui.qt5.zzwindow import ZzQtWindow
from zzgui.qt5.zzwindow import layout
import zzgui.zzapp as zzapp


class ZzApp(QMainWindow, zzapp.ZzApp,  ZzQtWindow):
    class ZzTabWidget(QTabWidget):
        def __init__(self, parent):
            super().__init__(parent)
            self.main_window = parent
            self.addTab(QWidget(), "")
            self.setAttribute(Qt.WA_DeleteOnClose)
            self.addTabButton = QToolButton(self)
            self.addTabButton.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.addTabButton.setText("+")
            self.addTabButton.clicked.connect(self.addTab)
            self.tabBar().setTabButton(0, QTabBar.RightSide, self.addTabButton)
            self.tabBar().setTabEnabled(0, False)

            self.closeButton = QToolButton(self)
            self.closeButton.setText("x")
            self.closeButton.clicked.connect(self.closeSubWindow)
            self.setCornerWidget(self.closeButton)
            self.currentChanged.connect(self._currentChanged)

            # self.addTab()
            # self.setCurrentIndex(0)

        def _currentChanged(self, index: int):
            # bug path when subwindow in tab 0 lost focus if we close subwindow in other tab
            if index == 0 and self.currentWidget().subWindowList():
                self.currentWidget().subWindowList()[-1].setFocus()

        def closeSubWindow(self):
            currentTabIndex = self.currentIndex()
            if self.currentWidget().activeSubWindow():
                self.currentWidget().activeSubWindow().close()
            elif self.count() > 2:  # close tab if them >2
                self.setCurrentIndex(currentTabIndex - 1)
                self.removeTab(currentTabIndex)

        def addTab(self, widget=None, label="="):
            if not widget:
                widget = QMdiArea(self)
                widget.setOption(QMdiArea.DontMaximizeSubWindowOnActivation)
                widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
                widget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            self.insertTab(self.count() - 1, widget, label)
            self.setCurrentIndex(self.count() - 2)
            if self.count() > 1:
                self.main_window.on_new_tab()

    def __init__(self, title=""):
        if QCoreApplication.startingUp():  # one and only qApp allowed
            self.qApp = QApplication([])
        QMainWindow.__init__(self)
        if not hasattr(qApp, "_mw_count"):
            qApp._mw_count = 0
            qApp._mw_list = []
        qApp._mw_count += 1
        qApp._mw_list.append(self)
        self.closing = False
        self.zz_toolbar = QToolBar(self)
        self.zz_tabwidget = self.ZzTabWidget(self)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(layout("v"))
        self.centralWidget().layout().addWidget(self.zz_toolbar)
        self.centralWidget().layout().addWidget(self.zz_tabwidget)
        self.statusBar().setVisible(True)
        self.set_title(title)

        super().__init__(title)
        qApp.focusChanged.connect(self.focus_changed)

    def get_self(self):
        if qApp.activeWindow():
            return qApp.activeWindow()
        else:
            return self

    def show_form(self, form=None, modal="modal"):
        if modal == "":  # mdiarea normal window
            self.zz_tabwidget.currentWidget().addSubWindow(form)
            form.show()
        else:  # mdiarea modal window
            prev_focus_widget = qApp.focusWidget()
            prev_mdi_window = self.zz_tabwidget.currentWidget().activeSubWindow()
            prev_tabbar_text = self.get_tabbar_text()

            if prev_mdi_window:
                prev_mdi_window.setDisabled(True)

            self.zz_tabwidget.currentWidget().addSubWindow(form)

            self.set_tabbar_text(form.window_title)

            if modal == "super":  # real modal dialog
                self.disable_toolbar(True)
                self.disable_menubar(True)
                self.disable_tabbar(True)
            form.exec_()

            if modal == "super":  # real modal dialog
                self.disable_toolbar(False)
                self.disable_menubar(False)
                self.disable_tabbar(False)

            if prev_mdi_window:
                prev_mdi_window.setEnabled(True)

            if prev_focus_widget is not None:
                prev_focus_widget.setFocus()
            self.set_tabbar_text(prev_tabbar_text)

    def build_menu(self):
        self.menu_list = super().reorder_menu(self.menu_list)
        self._main_menu = {}
        QMainWindow.menuBar(self).clear()
        QMainWindow.menuBar(self).show()
        for x in self.menu_list:
            _path = x["TEXT"]
            if _path == "" or _path in self._main_menu:
                continue
            prevNode = "|".join(_path.split("|")[:-1])
            topic = _path.split("|")[-1]
            if _path.count("|") == 0:  # first in chain - menu bar
                node = QMainWindow.menuBar(self)
            else:
                node = self._main_menu[prevNode]
            if _path.endswith("-"):
                node.addSeparator()
            elif x["WORKER"]:
                self._main_menu[_path] = node.addAction(topic)
                self._main_menu[_path].triggered.connect(x["WORKER"])
                if x["TOOLBAR"]:
                    button = QToolButton(self)
                    button.setText(topic)
                    button.setDefaultAction(self._main_menu[_path])
                    self.zz_toolbar.addAction(self._main_menu[_path])
            else:
                self._main_menu[_path] = node.addMenu(topic)
        # Show as context menu
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addActions(self.menuBar().actions())

    def focus_widget(self):
        return qApp.focusWidget()

    def set_style_sheet(self):
        if os.path.isfile(self.style_file):
            try:
                with open(self.style_file, "r") as style_data:
                    self.setStyleSheet(style_data.read())
            except Exception:
                print(f"File {self.style_file} reading error...")

    def lock(self):
        self.menuBar().setDisabled(True)
        self.zz_toolbar.setDisabled(True)
        self.zz_tabwidget.setDisabled(True)

    def unlock(self):
        self.menuBar().setDisabled(False)
        self.zz_toolbar.setDisabled(False)
        self.zz_tabwidget.setDisabled(False)

    def process_events(self):
        qApp.processEvents()

    def show_menubar(self, mode=True):
        zzapp.ZzApp.show_menubar(self)
        if mode:
            QMainWindow.menuBar(self).show()
        else:
            QMainWindow.menuBar(self).hide()

    def is_menubar_visible(self):
        return QMainWindow.menuBar(self).isVisible()

    def show_toolbar(self, mode=True):
        zzapp.ZzApp.show_toolbar(self)
        if mode:
            self.zz_toolbar.show()
        else:
            self.zz_toolbar.hide()

    def disable_toolbar(self, mode=True):
        self.zz_toolbar.setDisabled(True if mode else False)

    def disable_menubar(self, mode=True):
        QMainWindow.menuBar(self).setDisabled(True if mode else False)

    def disable_tabbar(self, mode=True):
        self.zz_tabwidget.tabBar().setDisabled(True if mode else False)

    def is_toolbar_visible(self):
        return self.zz_toolbar.isVisible()

    def show_tabbar(self, mode=True):
        zzapp.ZzApp.show_tabbar(self)
        if mode:
            self.zz_tabwidget.tabBar().show()
        else:
            self.zz_tabwidget.tabBar().hide()

    def is_tabbar_visible(self):
        return self.zz_tabwidget.tabBar().isVisible()

    def get_tabbar_text(self):
        return self.zz_tabwidget.tabBar().tabText(self.zz_tabwidget.currentIndex())

    def show_statusbar_mess(self, text=""):
        self.statusBar().showMessage(f"{text}")

    def set_tabbar_text(self, text=""):
        self.zz_tabwidget.tabBar().setTabText(self.zz_tabwidget.currentIndex(), text)

    def show_statusbar(self, mode=True):
        zzapp.ZzApp.show_statusbar(self)
        if mode:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def is_statusbar_visible(self):
        return self.statusBar().isVisible()

    def get_char_width(self, char="w"):
        return QFontMetrics(self.font()).width(char)

    def get_char_height(self):
        return QFontMetrics(self.font()).height()

    @staticmethod
    def get_open_file_dialoq(header="Open file", path="", filter=""):
        return QFileDialog.getOpenFileName(None, header, path, filter)

    @staticmethod
    def get_save_file_dialoq(header="Save file", path="", filter=""):
        return QFileDialog.getSaveFileName(None, header, path, filter)

    def _wait_for_show(self):
        while qApp.activeWindow() is None:
            pass
        self.process_events()
        self.add_new_tab()
        self.process_events()
        self.on_start()

    def save_geometry(self, settings):
        ZzQtWindow.save_geometry(self, settings)

    def run(self):
        # self.restore_geometry(self.settings)
        ZzQtWindow.restore_geometry(self, self.settings)
        self.show()
        super().run()
        QTimer.singleShot(111, self._wait_for_show)
        if len(QApplication.allWindows()) == 1:
            QApplication.exec_()

    def add_new_tab(self):
        self.zz_tabwidget.addTab()

    def show(self):
        QMainWindow.show(self)

    def on_new_tab(self):
        return super().on_new_tab()

    def showEvent(self, event):
        event.accept()
        super().showEvent(event)

    def closeEvent(self, event: QEvent):
        if not self.closing:
            self.close()
        event.accept()

    def close(self):
        self.closing = True
        super().close()
        qApp._mw_count -= 1
        QMainWindow.close(self)
        if qApp._mw_count <= 0:
            os._exit(0)
