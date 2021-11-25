if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

from urllib import request
from io import BytesIO, TextIOWrapper
from zipfile import ZipFile

from zzgui.qt5.zzapp import ZzApp as ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.zzmodel import ZzCsvModel
from zzgui.qt5.zzform import zzMess, zzWait


class DemoApp(ZzApp):
    def on_start(self):
        self.show_grid_form()

    def on_init(self):
        self.add_menu("File|Grid", self.show_grid_form, toolbar="*")
        self.add_menu("File|-")
        self.add_menu("Help|About", lambda: zzMess("About zzgui"), toolbar="*")
        self.add_menu("File|Quit", self.close, toolbar=1)

    def describe_grid_form(self):
        url = "https://eforexcel.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/"
        req = request.Request(url, headers={"User-Agent": "Safari"})
        # data: str = str(request.urlopen(req).read())

        def loader(req=req):
            def real_do():
                return str(request.urlopen(req).read())

            return real_do

        data: str = zzWait(loader(), "Loading")

        links = []
        for x in data.split('<a href="'):
            link = x.split('">')[0]
            if ".zip" in link:
                links.append({"link": link})

        form = ZzForm("Grid form")
        form.model.set_records(links)
        form.build_grid_view_auto_form()
        form.actions.add_action(
            text="Download", worker=lambda: self.load_and_show_link(form)
        )
        return form

    def load_and_show_link(self, form: ZzForm):
        url = form.r.link  # get current row column data
        req = request.Request(url, headers={"User-Agent": "Safari"})
        # data = request.urlopen(req).read()

        def loader():
            data = request.urlopen(req).read()
            return data

        data = zzWait(loader, "Loading")

        mem_zip_file_data = BytesIO()
        mem_zip_file_data.write(data)
        zip_file: ZipFile = ZipFile(mem_zip_file_data)
        csv_file_object = TextIOWrapper(zip_file.open(zip_file.namelist()[0]))

        form = ZzForm("CSV")
        form.set_model(ZzCsvModel(csv_file_object=csv_file_object))
        form.build_grid_view_auto_form()
        form.show_mdi_modal_grid()

    def show_grid_form(self):
        form = self.describe_grid_form()
        form.show_mdi_modal_grid()


def demo():
    app = DemoApp("zzgui Demo application")
    app.run()


if __name__ == "__main__":
    demo()
