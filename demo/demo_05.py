if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from typing_extensions import runtime
from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import time
import csv
import os
# import threading


from zzdb.schema import ZzDbSchema
from zzdb.db import ZzDb

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm

import zzgui.zzdialogs
from zzgui.zzdialogs import zzMess, zzWait

from PyQt5.QtWidgets import QApplication, qApp

zzgui.zzdialogs.ZzForm = ZzForm


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

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

        # db = ZzDb(guest_mode=True)

        # def dbcreate(db, csv_dict2, form):
        #     # schema = ZzDbSchema()
        #     schema = ZzDbSchema()
        #     schema.add(table="t1", column="row_uid", datatype="int", pk=True, ai=True)
        #     for x in csv_dict.fieldnames:
        #         schema.add(table="t1", column=x, datatype="char")
        #     db.set_schema(schema)
        #     i = 1
        #     dico = [x for x in csv_dict2]
        #     print(len(dico))
        #     for x in dico[:10]:
        #         # qApp.processEvents()
        #         time.sleep(2)
        #         db.insert("t1", x)
        #         i += 1
        #         print(i)
        #     print("Done")
        #     form.close()

        # dbcreate(db, csv_dict2)

        form = ZzForm("Grid form")

        def w1(form: ZzForm = form, csv_dict2=csv_dict2):
            def real_do():
                for x in [x for x in csv_dict2]:
                    form.model.records.append(x)
                    # time.sleep(0.00000000000001)
                form.model.refresh()
            return real_do

        zzWait(w1(), "Loading")

        form.add_control("/f")
        for x in csv_dict.fieldnames:
            form.add_control(x, x, control="line")

        # form.model.set_records([x for x in db.cursor(table_name="t1").records()])
        # form.model.set_records([x for x in csv_dict][:5])
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
