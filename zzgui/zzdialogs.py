if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

from threading import Thread, current_thread
import time
from zzgui.zzform import ZzForm
import zzgui.zzapp as zzapp


def center_window(form: ZzForm):
    w, h = zzapp.zz_app.get_size()
    form.form_stack[0].set_size(w * 0.33, h * 0.5)
    form.form_stack[0].set_position(w * 0.33, h * 0.15)


def zzMess(mess="", title="Message"):
    form = ZzForm(title)
    form.do_not_save_geometry = True
    form.add_control("/v")
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

    form.controls.add_control("mess", control="text", data=f"{mess}", readonly="*", disabled="*")

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
        self.min = 0
        self.max = 0
        self.shadow_value = 0
        self.value = 0
        self._return = None
        self.start_time = time.time()

    @staticmethod
    def set_min(value):
        current_thread().min = value

    @staticmethod
    def set_max(value):
        current_thread().max = value

    @staticmethod
    def get_max():
        c_thread = current_thread()
        if hasattr(c_thread, "max"):
            return c_thread.max
        else:
            return 0

    @staticmethod
    def step(step_value=1):
        current_thread().shadow_value += 1
        sv = current_thread().shadow_value
        if sv % step_value == 0:
            current_thread().value = sv

    @staticmethod
    def get_current():
        return current_thread().value

    def time(self):
        return time.time() - self.start_time

    def run(self):
        self._return = self._target(*self._args)


class ZzWaitForm:
    def __init__(self, mess, worker_thread):
        self.tick = {}
        self.worker_thread = worker_thread
        self.wait_window = ZzForm("Wait...")
        self.wait_window.do_not_save_geometry = True
        # self.wait_window.add_control("/s")
        self.wait_window.add_control("/h")
        self.wait_window.add_control("/s")
        self.wait_window.add_control("", label=mess, control="label")
        self.wait_window.add_control("/s")
        self.wait_window.add_control("/")
        steps_count_separator = ""
        if ZzThread.get_max() != 0:
            steps_count_separator = "/"

        if self.wait_window.add_control("/h"):
            self.wait_window.add_control("progressbar", "", control="progressbar")
            self.wait_window.add_control("min", "", control="label")
            self.wait_window.add_control("", steps_count_separator, control="label")
            self.wait_window.add_control("value", "", control="label")
            self.wait_window.add_control("", steps_count_separator, control="label")
            self.wait_window.add_control("max", "", control="label")
            self.wait_window.add_control("time", "", control="label")
        self.wait_window.add_control("/")
        self.show()

        if self.worker_thread.min != 0:
            self.wait_window.w.progressbar.set_min(self.worker_thread.min)
            self.wait_window.s.min = self.worker_thread.min
        if self.worker_thread.max != 0:
            self.wait_window.w.progressbar.set_max(self.worker_thread.max)
            self.wait_window.s.max = self.worker_thread.max

    def step(self):
        if self.worker_thread.value != 0:
            self.wait_window.w.progressbar.set_value(self.worker_thread.value)
            self.wait_window.s.value = self.worker_thread.value

        thread_time = int(self.worker_thread.time())
        # print(self.worker_thread.time())
        sec = thread_time % 60
        min = (thread_time - sec) % 3600
        hours = thread_time - min * 3600 - sec
        sec = int(sec)
        self.wait_window.s.time = f" Time {hours:02}:{min:02}:{sec:02}"
        zzapp.zz_app.process_events()

    def show(self):
        self.wait_window.show_mdi_form()
        zzapp.zz_app.process_events()
        w = zzapp.zz_app.get_size()[0]
        fh = self.wait_window.form_stack[0].get_size()[1]
        self.wait_window.form_stack[0].set_size(w * 0.9, fh)
        left, top = self.wait_window.form_stack[0].center_pos()
        self.wait_window.form_stack[0].set_position(left, top)
        zzapp.zz_app.process_events()

    def close(self):
        self.wait_window.close()
        zzapp.zz_app.process_events()


def zzWaitStep(step_value=1):
    ZzThread.step(step_value)


def zzWaitMax(max_value=0):
    ZzThread.set_max(max_value)


def zzWait(worker, mess=""):
    wait_window = None
    wait_window_on = False
    last_focus_widget = zzapp.zz_app.focus_widget()
    last_progressbar_value = 0
    last_progressbar_time = 0
    zzapp.zz_app.lock()
    worker_thread = ZzThread(target=worker)
    worker_thread.start()
    while worker_thread.is_alive():
        time.sleep(0.3)
        if worker_thread.time() > 1 and wait_window_on is not True:
            wait_window_on = True
            wait_window = ZzWaitForm(mess, worker_thread)
        if wait_window_on is True:
            if worker_thread.min < worker_thread.max:
                if worker_thread.value != 0 and last_progressbar_value != worker_thread.value:
                    wait_window.step()
            elif worker_thread.time() - last_progressbar_time > 1:
                wait_window.step()
                last_progressbar_time = worker_thread.time()
        last_progressbar_value = worker_thread.value
        zzapp.zz_app.process_events()
    zzapp.zz_app.unlock()
    if wait_window is not None:
        wait_window.close()
    if hasattr(last_focus_widget, "set_focus"):
        last_focus_widget.set_focus()

    zzapp.zz_app.show_statusbar_mess(f"{worker_thread.time():.2f}")
    return worker_thread._return
