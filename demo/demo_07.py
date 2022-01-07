if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")


from zzgui.qt5.zzapp import ZzApp
from zzgui.qt5.zzform import ZzForm as ZzForm
from zzdb.schema import ZzDbSchema
from zzdb.db import ZzDb
from random import randint

from zzgui.qt5.zzform import zzMess


class dataSchema(ZzDbSchema):
    def __init__(self):
        super().__init__()

        self.add_customers()
        self.add_products()
        self.add_orders()
        self.add_order_lines()

    def add_order_lines(self):
        self.add(table="order_lines", column="id", datatype="int", datalen=9, pk=True)
        self.add(
            table="order_lines",
            column="product_id",
            to_table="products",
            to_column="product_id",
            related="name",
        )
        self.add(
            table="order_lines",
            column="order_id",
            to_table="orders",
            to_column="order_id",
            related="date",
        )
        self.add(
            table="order_lines",
            column="quantity",
            datatype="num",
            datalen=10,
            datadec=4,
        )
        self.add(
            table="order_lines",
            column="price",
            datatype="num",
            datalen=10,
            datadec=2,
        )

    def add_orders(self):
        self.add(table="orders", column="order_id", datatype="int", datalen=9, pk=True)
        self.add(table="orders", column="date", datatype="date")
        self.add(
            table="orders",
            column="customer_id",
            to_table="customers",
            to_column="customer_id",
            related="name",
        )

    def add_products(self):
        self.add(
            table="products", column="product_id", datatype="int", datalen=9, pk=True
        )
        self.add(table="products", column="name", datatype="varchar", datalen=100)

    def add_customers(self):
        self.add(
            table="customers",
            column="customer_id",
            datatype="int",
            datalen=0,
            pk=True,
        )
        self.add(table="customers", column="name", datatype="varchar", datalen=100)


def data_load(db: ZzDb):
    for x in range(1, 10):
        db.insert("customers", {"customer_id": x, "name": f"Customer {x}"})
    for x in range(1, 50):
        db.insert("products", {"product_id": x, "name": f"Product {x}"})
    for x in range(1, 50):
        db.insert(
            "orders",
            {
                "order_id": x,
                "customer_id": randint(1, 9),
                "date": f"2022-01-{randint(1,31)}",
            },
        )
        for y in range(1, randint(1, 5)):
            db.insert(
                "order_lines",
                {
                    "order_id": x,
                    "product_id": randint(1, 9),
                    "quantity": randint(1, 100),
                    "price": randint(1, y),
                },
            )

    assert len(db.get_tables()) == 8
    assert db.cursor(table_name="customers").row_count() == 9
    assert db.cursor(table_name="products").row_count() == 49
    assert db.cursor(table_name="orders").row_count() == 49
    print(db.cursor(table_name="order_lines").row_count())


class databaseApp(ZzApp):
    def on_start(self):
        self.customers()

    def create_database(self):
        self.db = ZzDb("sqlite3", database_name=":memory:")
        self.db.set_schema(dataSchema())
        data_load(self.db)

    def on_init(self):
        self.add_menu("File|About", lambda: zzMess("First application!"))
        self.add_menu("File|-")
        self.add_menu("File|Exit", self.close, toolbar=1)
        self.add_menu("Catalogs|Customers", self.customers, toolbar=1)
        self.add_menu("Catalogs|Products", self.products, toolbar=1)
        self.add_menu("Documents|Orders", self.orders, toolbar=1)
        self.create_database()

        return super().on_init()

    def customers(self):
        form = ZzForm("Customers")
        form.add_control("", "First Label")
        form.add_control("field", "First Field")
        form.add_control("", "Close Form", control="button", valid=form.close)
        form.show_mdi_modal_form()

    def products(self):
        form = ZzForm("Products")
        form.add_control("", "First Label")
        form.add_control("field", "First Field")
        form.add_control("", "Close Form", control="button", valid=form.close)
        form.show_mdi_modal_form()

    def orders(self):
        form = ZzForm("Orders")
        form.add_control("", "First Label")
        form.add_control("field", "First Field")
        form.add_control("", "Close Form", control="button", valid=form.close)
        form.show_mdi_modal_form()


def demo():
    app = databaseApp("zzgui - the database app")
    app.run()


if __name__ == "__main__":
    demo()
