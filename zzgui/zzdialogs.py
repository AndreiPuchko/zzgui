if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from threading import Thread
import time
from zzgui.zzform import ZzForm
import zzgui.zzapp as zzapp


def center_window(form: ZzForm):
    w, h = zzapp.zz_app.main_window.get_size()
    form.form_stack[0].set_size(w * 0.33, h * 0.5)
    form.form_stack[0].set_position(w * 0.33, h * 0.15)


def zzMess(mess="", title="Message"):
    form = ZzForm(title)
    form.do_not_save_geometry = True
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

    form.before_form_show = lambda: center_window(form)
    form.show_app_modal_form()


def zzAskYN(mess, title="Ask"):
    form = ZzForm(title)
    form.do_not_save_geometry = True
    form.choice = 0
    form.add_control("/")

    form.controls.add_control(
        "mess", control="text", data=f"{mess}", readonly="*", disabled="*"
    )

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
    form.before_form_show = lambda: center_window(form)
    form.show_app_modal_form()
    return form.choice


class ZzThread(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._target = target
        self._args = args
        self._return = None
        self.start_time = time.time()

    def time(self):
        return time.time() - self.start_time

    def run(self):
        self._return = self._target(*self._args)


class ZzWaitForm:
    def __init__(self, mess):
        self.wait_window = ZzForm("Wait...")
        self.wait_window.add_control("/s")
        self.wait_window.add_control("/h")
        self.wait_window.add_control("/s")
        self.wait_window.add_control("", label=mess, control="label")
        self.wait_window.add_control("/s")
        self.wait_window.add_control("/")
        self.wait_window.add_control("pb", mess, control="progressbar")
        self.wait_window.add_control("/s")
        self.show()

    def show(self):
        self.wait_window.show_mdi_form()
        zzapp.zz_app.process_events()
        w, h = zzapp.zz_app.main_window.get_size()
        self.wait_window.form_stack[0].set_size(w * 0.8, h * 0.15)
        self.wait_window.form_stack[0].set_position(w * 0.1, h * 0.3)
        zzapp.zz_app.process_events()

    def close(self):
        self.wait_window.close()
        zzapp.zz_app.process_events()


def zzWait(worker, mess=""):
    wait_window = None
    wait_window_on = False
    last_focus_widget = zzapp.zz_app.focus_widget()
    zzapp.zz_app.lock()
    t = ZzThread(target=worker)
    t.start()
    while t.is_alive():
        if t.time() > 1 and wait_window_on is not True:
            wait_window_on = True
            wait_window = ZzWaitForm(mess)
        zzapp.zz_app.process_events()
    zzapp.zz_app.unlock()
    if wait_window is not None:
        wait_window.close()
    if last_focus_widget:
        last_focus_widget.set_focus()

    zzapp.zz_app.show_statusbar_mess(f"{t.time():.3f}")
    return t._return
