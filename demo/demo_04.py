if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import csv
import os

from PyQt5.QtWidgets import qApp

from zzdb.schema import ZzDbSchema
from zzdb.db import ZzDb

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm

import zzgui.zzdialogs
from zzgui.zzdialogs import zzMess

zzgui.zzdialogs.ZzForm = ZzForm


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("File|Quit", self.close, toolbar="*")
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")

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
            csv_data = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
            csv_dict = csv.DictReader(csv_data)

        else:
            csv_dict = csv.DictReader(open(file_name))

        # mem_zip_file_data = BytesIO()
        # mem_zip_file_data.write(data)
        # zip_file: ZipFile = ZipFile(mem_zip_file_data)
        # csv_data = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
        # csv_dict = csv.DictReader(csv_data)

        # csv_dict = csv.DictReader(
        #     open("temp/electronic-card-transactions-october-2021-csv-tables.csv")
        # )

        # schema = ZzDbSchema()
        # db = ZzDb(guest_mode=True)
        # schema.add(table="t1", column="row_uid", datatype="int", pk=True, ai=True)
        # for x in csv_dict.fieldnames:
        #     schema.add(table="t1", column=x, datatype="char")
        # db.set_schema(schema)

        # for x in [x for x in csv_dict][:100]:
        #     qApp.processEvents()
        #     db.insert("t1", x)

        form = ZzForm("Grid form")
        form.actions.add_action("Plot", lambda: zzMess("New"))
        form.actions.add_action("Graph|1", lambda: zzMess("Edit"))
        form.actions.add_action("Graph|2", lambda: zzMess("Edit"))
        form.actions.add_action("Nt", lambda: zzMess("Nt"))
        form.actions.add_action("Graph|3", lambda: zzMess("Edit"))

        for x in csv_dict.fieldnames:
            form.add_control(x, x, control="line")

        # form.model.set_records([x for x in db.cursor(table_name="t1").records()])
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
