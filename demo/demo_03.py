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
from zzgui.qt5.zzform import zzMess


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("File|Quit", self.close)
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")

    def describe_grid_form(self):
        # load some CSV data from ...
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
        # Define form
        form = ZzForm("Grid form")
        # Define layout
        form.add_control("/f", "Frame with form layout")
        # Populate it with the columns from csv
        for x in csv_dict.fieldnames:
            form.add_control(x, x, control="line")
        # Assign data source
        form.model.set_records([x for x in csv_dict])
        form.actions.add_action(text="/crud")
        return form

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
