if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")


from zzgui.qt5.zzapp import ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzgui.qt5.zzform import zzMess

from zzgui.zzmodel import ZzCursorModel

from zzdb.schema import ZzDbSchema
from zzdb.db import ZzDb
from zzdb.cursor import ZzCursor
from random import randint


def mock_data_load(db: ZzDb):
    customer_qt = 100
    for x in range(1, customer_qt):
        db.insert(
            "customers",
            {
                "customer_id": x,
                "name": f"Customer {x}{str(randint(0,600)*6)}",
                "vip": {0: "", 1: "*"}[x % 2],
                "combo_status": x % 3 + 1,
                "list_status": x % 3 + 1,
                "radio_status": x % 3 + 1,
            },
        )


class databaseApp(ZzApp):
    def on_start(self):
        self.customers()

    def create_database(self):
        self.db = ZzDb("sqlite3", database_name=":memory:")

    def on_init(self):
        self.create_database()

        self.add_menu("File|About", lambda: zzMess("First application!"))
        self.add_menu("File|-")
        self.add_menu("File|Exit", self.close, toolbar=1)
        self.add_menu("Catalogs|Customers", self.customers, toolbar=1)

        data_schema = ZzDbSchema()

        for x in self.form_customers().get_table_schema():
            data_schema.add(x)

        self.db.set_schema(data_schema)
        mock_data_load(self.db)

        return super().on_init()

    def form_customers(self):
        form = ZzForm("Customers")

        form.add_control(name="customer_id", label="Customer Id", datatype="int", pk="*")
        form.add_control("name", "Name", datatype="char", datalen=100)
        form.add_control("vip", "VIP", datatype="char", datalen=1, control="check", pic="VIP client")

        status_control_num = {"datatype": "int", "datalen": 1, "pic": "active;frozen;blocked"}
        status_control_char = {"datatype": "char", "datalen": 15, "pic": "active;frozen;blocked"}

        form.add_control("radio_status", "Num Radio Status", control="radio", **status_control_num)
        form.add_control("radio_status_char", "Char Radio Status", control="radio", **status_control_char)

        form.add_control("combo_status", "Num Combo Status", control="combo", **status_control_num)
        form.add_control("combo_status", "Char Combo Status", control="combo", **status_control_char)

        form.add_control("/")
        form.add_control("/h")
        form.add_control("list_status", "Num List Status", control="list", **status_control_num)
        form.add_control("list_status_char", "Char List Status", control="list", **status_control_char)

        cursor: ZzCursor = self.db.table(table_name="customers")
        model = ZzCursorModel(cursor)
        form.set_model(model)
        form.actions.add_action("/crud")
        return form

    def customers(self):
        self.form_customers().show_mdi_modal_grid()


def demo():
    app = databaseApp("zzgui - the database app")
    app.run()


if __name__ == "__main__":
    demo()
