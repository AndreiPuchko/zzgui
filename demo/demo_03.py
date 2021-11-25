if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile
import os

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess
from zzgui.zzmodel import ZzCsvModel


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")
        self.add_menu("File|Quit", self.close, toolbar=True)

    def show_grid_form(self):
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
            csv_file_object = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
        else:
            csv_file_object = open(file_name)
        # Define form
        form = ZzForm("Grid form")
        form.set_model(ZzCsvModel(csv_file_object=csv_file_object))
        form.build_grid_view_auto_form()

        form.actions.add_action(
            "Show Period", worker=lambda: zzMess(f"{form.r.Period}"), hotkey="F4"
        )
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
