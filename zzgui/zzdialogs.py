if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from urllib.request import HTTPPasswordMgrWithDefaultRealm
from zzgui.zzform import ZzForm


def zzMess(mess="", title="Message"):
    form = ZzForm(title)
    form.add_control("mess", control="text", data=f"{mess}", readonly=True)
    if form.add_control("/h"):
        form.add_control("/s")

        form.add_control(
            "close",
            "Ok",
            control="button",
            eat_enter=True,
            hotkey="PgDown",
            valid=form.close,
        )

        form.add_control("/s")
        form.add_control("/")
    form.show_app_modal_form()


def zzAskYN(mess, title="Ask"):
    form = ZzForm(title)
    form.choice = 0
    form.add_control("/")

    form.controls.add_control("mess", control="text", data=f"{mess}", readonly="*",disabled="*")

    if form.add_control("/h"):
        form.add_control("/s")

        def buttonPressed(form=form, answer=0):
            form.choice = answer
            form.close()

        form.add_control(
            "cancel",
            "Cancel",
            control="button",
            valid=lambda: buttonPressed(form, 1),
            eat_enter="*",
        )
        form.add_control(
            "ok",
            "Ok",
            control="button",
            valid=lambda: buttonPressed(form, 2),
            eat_enter="*",
            tag="ok",
            hotkey="PgDown",
        )
        form.add_control("/s")
        form.add_control("/")
    form.show_app_modal_form()
    return form.choice
