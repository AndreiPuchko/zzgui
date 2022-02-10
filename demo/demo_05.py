if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")


from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import time
import csv
import os


from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.zzmodel import ZzModel

from zzgui.zzdialogs import zzMess, zzWait, zzWaitMax, zzWaitStep


class DemoApp(ZzApp):
    def on_start(self):
        def worker():
            def real_worker():
                zzWaitMax(300)
                for x in range(300):
                    zzWaitStep()
                    time.sleep(0.03)

            return real_worker

        zzWait(worker(), "W o r k i n g")
        # self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|MdiNonModal", self.mdi_non_modal, toolbar="*")

        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")

        self.add_menu("File|-")
        self.add_menu("File|Quit", self.close, toolbar="*")

    def describe_grid_form(self):
        file_name = "temp/electronic-card-transactions-october-2021-csv-tables.csv"
        if not os.path.isfile(file_name):
            url = (
                "https://www.stats.govt.nz/assets/"
                "Uploads/Electronic-card-transactions/"
                "Electronic-card-transactions-October-2021/"
                "Download-data/"
                "electronic-card-transactions-october-2021-csv.zip"
            )
            data = request.urlopen(url).read()
            mem_zip_file_data = BytesIO()
            mem_zip_file_data.write(data)
            zip_file: ZipFile = ZipFile(mem_zip_file_data)

            csv_file_object = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
            csv_file_object2 = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))

        else:
            csv_file_object = open(file_name)
            csv_file_object2 = open(file_name)

        csv_dict = csv.DictReader(csv_file_object)
        csv_dict2 = csv.DictReader(csv_file_object2)

        form = ZzForm("Grid form")
        form.set_model(ZzModel())

        def w1(form: ZzForm = form, csv_dict2=csv_dict2):
            def real_do():
                for x in [x for x in csv_dict2]:
                    form.model.records.append(x)

            return real_do

        zzWait(w1(), "Loading")

        form.add_control("/f")
        for x in csv_dict.fieldnames:
            form.add_control(x, x, control="line")

        form.actions.add_action("/view")
        return form

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()

    def mdi_non_modal(self):
        wait_window = ZzForm("wai")
        wait_window.add_control(label="333333333333")
        wait_window.show_mdi_form()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
