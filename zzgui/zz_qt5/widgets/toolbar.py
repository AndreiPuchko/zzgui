import sys

if __name__ == "__main__":

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import zzgui.zz_qt5.widget as zzwiddet
from zzgui.zz_qt5.window import zz_align
from zzgui.zzapp import ZzAction

from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QToolBar,
    QToolButton,
    QSizePolicy,
    QMenu,
)
from PyQt5.QtCore import Qt


class toolbar(QFrame, zzwiddet.ZzWidget):
    def __init__(self, meta):
        super().__init__(meta)
        self.setLayout(QVBoxLayout() if "v" in meta.get("control") else QHBoxLayout())
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.layout().setAlignment(zz_align["7"])
        if not isinstance(meta.get("actions"), ZzAction):
            return
        if isinstance(meta.get("actions"), ZzAction):
            tool_bar_qt_actions = QMenu()
            cascade_action = {"": tool_bar_qt_actions}
            actions: ZzAction = meta.get("actions")
            for act in actions.action_list:
                worker = act.get("worker", None)
                action_text_list = act["text"].split("|")
                for x in range(len(action_text_list)):
                    action_key = "|".join(action_text_list[:x])
                    action_text = action_text_list[x]
                    if action_text == "-":
                        act["engineAction"] = cascade_action[action_key].addSeparator()
                    else:
                        if x + 1 == len(action_text_list):  # real action

                            act["engineAction"] = cascade_action[action_key].addAction(
                                action_text
                            )
                            if worker:
                                act["engineAction"].triggered.connect(worker)
                            # elif (
                            #     act.get("child_field") or act.get("parent_field")
                            # ) and act.get("child_form"):
                            #     # self.zzForm.gridChildren.append(act)
                            #     def getChildForm(act):
                            #         def rd():
                            #             child = act.get("child_form")()
                            #             if child.t:
                            #                 parent_field_vause = (
                            #                     self.zzForm.t.r.__getattr__(
                            #                         act.get("parent_field")
                            #                     )
                            #                 )
                            #                 child_field = act.get("child_field")
                            #                 filter = (
                            #                     f"{child_field}='{parent_field_vause}'"
                            #                 )
                            #                 child.t.setFilter(filter)
                            #                 child.t.refresh()
                            #             child.showForm()

                            #         return rd

                            #     act["engineAction"].triggered.connect(getChildForm(act))
                            # act["engineAction"].setShortcut(
                            #     act["hotkey"]
                            #     if not act["hotkey"] == "Spacebar"
                            #     else Qt.Key_Space
                            # )
                            # act["engineAction"].setShortcutContext(
                            #     Qt.WidgetWithChildrenShortcut
                            # )
                        else:  # cascade
                            subMenu = "|".join(action_text_list[: x + 1])
                            if subMenu not in cascade_action:
                                cascade_action[subMenu] = cascade_action[
                                    action_key
                                ].addMenu(
                                    f"{action_text}  {'' if '|' in subMenu else '  '}"
                                )
            self.main_button = QToolBar()
            self.main_button_action = self.main_button.addAction("☰")
            self.main_button_action.setMenu(tool_bar_qt_actions)
            self.main_button.widgetForAction(self.main_button_action).setPopupMode(
                QToolButton.InstantPopup
            )
            self.layout().addWidget(self.main_button)
            if actions.show_main_button is False:
                self.main_button.setVisible(False)

            self.toolBarButton = QToolBar()
            # self.toolBarButton.setOrientation(Qt.Orientation.Horizontal)
            self.toolBarButton.addSeparator()
            self.toolBarButton.addActions(tool_bar_qt_actions.actions())
            for x in self.toolBarButton.actions():
                if hasattr(self.toolBarButton.widgetForAction(x), "setPopupMode"):
                    self.toolBarButton.widgetForAction(x).setPopupMode(QToolButton.InstantPopup)

            if actions.show_actions:
                self.layout().addWidget(self.toolBarButton)

    def set_context_menu(self, widget):
        widget.setContextMenuPolicy(Qt.ActionsContextMenu)
        widget.addActions(self.toolBarButton.actions())
