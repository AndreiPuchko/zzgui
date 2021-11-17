if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

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
            valid=form.close,
        )

        form.add_control("/s")
        form.add_control("/")
    form.show_app_modal_form()
