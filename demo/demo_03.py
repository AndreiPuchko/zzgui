if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import csv
import os

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm

import zzgui.zzdialog
from zzgui.zzdialog import zzMess

zzgui.zzdialog.ZzForm = ZzForm


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("File|Quit", self.close)
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")

    def describe_grid_form(self):
        file_name = "temp/electronic-card-transactions-october-2021-csv-tables.csv"
        if not os.path.isfile(file_name):
            url = (
                "https://www.stats.govt.nz/assets/Uploads/"
                "Electronic-card-transactions/"
                "Electronic-card-transactions-October-2021/"
                "Download-data/electronic-card-transactions-october-2021-csv.zip"
            )
            data = request.urlopen(url).read()
            mem_zip_file_data = BytesIO()
            mem_zip_file_data.write(data)
            zip_file: ZipFile = ZipFile(mem_zip_file_data)
            csv_data = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
            csv_dict = csv.DictReader(csv_data)

        else:
            csv_dict = csv.DictReader(open(file_name))

        form = ZzForm("Grid form")
        form.add_control("/f")
        for x in csv_dict.fieldnames:  # Populate form with the columns froom csv
            form.add_control(x, x, control="line")

        form.model.set_records([x for x in csv_dict])

        return form

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
