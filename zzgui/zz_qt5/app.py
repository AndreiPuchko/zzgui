if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()


# from zzgui import zzform
from zzgui.zz_qt5.window import ZzQtWindow
import zzgui.zzapp as zzapp


from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QToolButton,
    qApp,
)
from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt


from zzgui.zz_qt5.tab import ZzTabWidget
from zzgui.zz_qt5.window import layout


class ZzApp(zzapp.ZzApp, QApplication):
    def __init__(self, title=""):
        super().__init__(title)
        QApplication.__init__(self, [])
        self.main_window = ZzMainWindow(title)

    def show_form(self, form=None, modal="modal"):
        if modal == "":  # mdiarea normal window
            self.main_window.zz_tabwidget.currentWidget().addSubWindow(form)
            form.show()
        else:  # mdiarea modal window
            prev_focus_widget = qApp.focusWidget()
            prev_mdi_window = (
                self.main_window.zz_tabwidget.currentWidget().activeSubWindow()
            )
            prev_tabbar_text = self.get_tabbar_text()

            if prev_mdi_window:
                prev_mdi_window.setDisabled(True)

            self.main_window.zz_tabwidget.currentWidget().addSubWindow(form)
            self.set_tabbar_text(form.title)

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

            if prev_focus_widget:
                prev_focus_widget.setFocus()
            self.set_tabbar_text(prev_tabbar_text)

    def build_menu(self):
        self.menu_list = super().reorder_menu(self.menu_list)
        self._main_menu = {}
        QMainWindow.menuBar(self.main_window).clear()
        QMainWindow.menuBar(self.main_window).show()
        for x in self.menu_list:
            _path = x["TEXT"]
            if _path == "" or _path in self._main_menu:
                continue
            prevNode = "|".join(_path.split("|")[:-1])
            topic = _path.split("|")[-1]
            if _path.count("|") == 0:  # first in chain - menu bar
                node = QMainWindow.menuBar(self.main_window)
            else:
                node = self._main_menu[prevNode]
            if _path.endswith("-"):
                node.addSeparator()
            elif x["WORKER"]:
                self._main_menu[_path] = node.addAction(topic)
                self._main_menu[_path].triggered.connect(x["WORKER"])
                if x["TOOLBAR"]:
                    button = QToolButton()
                    button.setText(topic)
                    button.setDefaultAction(self._main_menu[_path])
                    self.main_window.zz_toolbar.addAction(self._main_menu[_path])
            else:
                self._main_menu[_path] = node.addMenu(topic)
        # Show as context menu
        self.main_window.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.main_window.addActions(self.main_window.menuBar().actions())

    def show_menubar(self, mode=True):
        zzapp.ZzApp.show_menubar(self)
        if mode:
            QMainWindow.menuBar(self.main_window).show()
        else:
            QMainWindow.menuBar(self.main_window).hide()

    def is_menubar_visible(self):
        return QMainWindow.menuBar(self.main_window).isVisible()

    def show_toolbar(self, mode=True):
        zzapp.ZzApp.show_toolbar(self)
        if mode:
            self.main_window.zz_toolbar.show()
        else:
            self.main_window.zz_toolbar.hide()

    def disable_toolbar(self, mode=True):
        self.main_window.zz_toolbar.setDisabled(True if mode else False)

    def disable_menubar(self, mode=True):
        QMainWindow.menuBar(self.main_window).setDisabled(True if mode else False)

    def disable_tabbar(self, mode=True):
        self.main_window.zz_tabwidget.tabBar().setDisabled(True if mode else False)

    def is_toolbar_visible(self):
        return self.main_window.zz_toolbar.isVisible()

    def show_tabbar(self, mode=True):
        zzapp.ZzApp.show_tabbar(self)
        if mode:
            self.main_window.zz_tabwidget.tabBar().show()
        else:
            self.main_window.zz_tabwidget.tabBar().hide()

    def is_tabbar_visible(self):
        return self.main_window.zz_tabwidget.tabBar().isVisible()

    def get_tabbar_text(self):
        return self.main_window.zz_tabwidget.tabBar().tabText(
            self.main_window.zz_tabwidget.currentIndex()
        )

    def set_tabbar_text(self, text=""):
        self.main_window.zz_tabwidget.tabBar().setTabText(
            self.main_window.zz_tabwidget.currentIndex(), text
        )

    def show_statusbar(self, mode=True):
        zzapp.ZzApp.show_statusbar(self)
        if mode:
            self.main_window.statusBar().show()
        else:
            self.main_window.statusBar().hide()

    def is_statusbar_visible(self):
        return self.main_window.statusBar().isVisible()

    def run(self):
        self.main_window.restore_geometry(self.settings)
        self.main_window.show()
        super().run()
        self.exec_()


class ZzMainWindow(zzapp.ZzMainWindow, QMainWindow, ZzQtWindow):
    def __init__(self, title=""):
        self._core_app = QApplication([])
        super().__init__()
        self.zz_toolbar = QToolBar()
        self.zz_tabwidget = ZzTabWidget()
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout("v"))
        self.centralWidget().layout().addWidget(self.zz_toolbar)
        self.centralWidget().layout().addWidget(self.zz_tabwidget)
        self.statusBar().setVisible(True)
        self.set_title(title)

    # def focus_widget(self):
    #     return QApplication.focusWidget()

    def show(self):
        QMainWindow.show(self)

    def closeEvent(self, e):
        zzapp.zz_app.close()

    def close(self):
        super().close()
        QMainWindow.close(self)
