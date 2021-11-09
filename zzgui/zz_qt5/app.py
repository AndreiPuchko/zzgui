if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo_01 import demo

    demo()


from zzgui.zz_qt5.window import ZzQtWindow
import zzgui.zzapp as zzapp


from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QMainWindow, QToolButton
from PyQt5.QtWidgets import QToolBar


from zzgui.zz_qt5.tab import ZzTabWidget
from zzgui.zz_qt5.window import layout

class ZzApp(zzapp.ZzApp, QMainWindow, ZzQtWindow):
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

    def zz_layout(self, arg="h"):
        return layout(arg)

    def show_form(self, form=None, modal="modal"):
        if modal == "super":  # real modal dialog
            form.setModal(True)
            form.show()
        else:
            if "modal" in modal:  # mdiarea modal window
                form.prev_form = self.zz_tabwidget.currentWidget().activeSubWindow()
                # if form.prev_form:
                #     form.prev_form._lastWidget = qApp.focusWidget()
                self.zz_tabwidget.currentWidget().addSubWindow(form)

                if form.prev_form:
                    form.prev_form.setDisabled(True)
                # form.exec_()
                # QDialog.exec_(form)
                QDialog.show(form)
            else:  # mdiarea normal window
                self.zz_tabwidget.currentWidget().addSubWindow(form)
                form.show()

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
                    button = QToolButton()
                    button.setText(topic)
                    button.setDefaultAction(self._main_menu[_path])
                    self.zz_toolbar.addAction(self._main_menu[_path])
            else:
                self._main_menu[_path] = node.addMenu(topic)

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

    def show_statusbar(self, mode=True):
        zzapp.ZzApp.show_statusbar(self)
        if mode:
            self.statusBar().show()
        else:
            self.statusBar().hide()

    def is_statusbar_visible(self):
        return self.statusBar().isVisible()

    def focus_widget(self):
        return QApplication.focusWidget()

    def run(self):
        super().run()
        self.show()
        self._core_app.exec_()

    def closeEvent(self, e):
        self.close()
        e.accept()

    def close(self):
        super().close()
        QMainWindow.close(self)
