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
        url = "https://eforexcel.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/"
        req = request.Request(url, headers={"User-Agent": "Safari"})
        data: str = str(request.urlopen(req).read())
        links = []
        for x in data.split('<a href="'):
            link = x.split('">')[0]
            if ".zip" in link:
                links.append({"link": link})

        form = ZzForm("Grid form")
        form.model.set_records(links)
        form.model.build_auto_form_from_records()
        form.actions.add_action(text="Download", worker=lambda: self.load_link(form))
        return form

    def load_link(self, form: ZzForm):
        url = form.model.get_record(form.current_row)["link"]
        req = request.Request(url, headers={"User-Agent": "Safari"})
        data = request.urlopen(req).read()
        mem_zip_file_data = BytesIO()
        mem_zip_file_data.write(data)
        zip_file: ZipFile = ZipFile(mem_zip_file_data)
        csv_data = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))
        csv_dict = csv.DictReader(csv_data)
        fieldnames = [x.replace(" ", "_") for x in csv_dict.fieldnames]
        csv_dict = csv.DictReader(csv_data, fieldnames)
        form = ZzForm("CSV")
        form.model.set_records([x for x in csv_dict])
        form.model.build_auto_form_from_records()
        form.show_mdi_modal_grid()

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
