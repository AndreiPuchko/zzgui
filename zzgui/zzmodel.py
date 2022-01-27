if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import csv
import datetime
import re


import zzgui.zzapp as zzapp
from zzgui.zzutils import num
from zzdb.cursor import ZzCursor
from zzdb.db import ZzDb


class ZzModel:
    def __init__(self):
        self.zz_form = None
        self.columns = []
        self.headers = []
        self.alignments = []

        self.records = []
        self.proxy_records = []
        self.use_proxy = False
        self.relation_cache = {}
        self.lastdata_error_text = ""

        self.meta = []

        self.readonly = True
        self.filterable = False
        self.data_changed = False

        self.order_text = ""
        self.where_text = ""

    def get_table_name(self):
        return ""

    def get_data_error(self):
        return self.lastdata_error_text

    def set_data_error(self, text=""):
        self.lastdata_error_text = text

    def insert(self, record: dict, current_row=0):
        # print(record)
        return True

    def update(self, record: dict, current_row=0):
        # print(record)
        return True

    def delete(self, current_row=0):
        # print(current_row)
        return True

    def set_where(self, where_text=""):
        self.where_text = where_text

    def get_where(self):
        return self.where_text

    def set_order(self, order_data=""):
        if isinstance(order_data, int):
            self.order_text = self.columns[order_data]
        elif isinstance(order_data, list):
            self.order_text = ",".join(order_data)
        else:
            self.order_text = order_data

    def refresh(self):
        self.relation_cache = {}

    def reset(self):
        self.records = []
        self.proxy_records = []
        self.use_proxy = False
        self.relation_cache = {}
        self.lastdata_error_text = ""

    def set_records(self, records):
        self.records = records

    def build(self):
        self.columns = []
        self.headers = []
        self.alignments = []
        self.meta = []
        for meta in self.zz_form.controls:
            if meta.get("name", "").startswith("/") or meta.get("nogrid"):
                continue
            if meta.get("control", "") in ["button", "widget", "form"]:
                continue
            self.zz_form.model.add_column(meta)

    def add_column(self, meta):
        if not meta.get("control"):
            meta["control"] = "line"

        meta = zzapp.ZzControls.validate(meta)
        self.columns.append(meta["name"])
        self.headers.append(meta["label" if meta.get("saygrid") else "label"])
        self.alignments.append(meta.get("alignment", "7"))
        self.meta.append(meta)

    def get_record(self, row):
        if self.use_proxy:
            return self.records[self.proxy_records[row]]
        else:
            return self.records[row]

    def _get_related(self, value, meta, do_not_show_value=False, reset_cache=False):
        if meta.get("num") and num(value) == 0:
            return ""
        elif value == "":
            return ""
        key = (meta["to_table"], f"{meta['to_column']}='{value}'", meta["related"])
        if not reset_cache and key in self.relation_cache:
            related = self.relation_cache[key]
        else:
            related = self.get_related(
                meta["to_table"], f"{meta['to_column']}='{value}'", meta["related"]
            )
            self.relation_cache[key] = related
        if related is None:
            related = ""
        if do_not_show_value:
            return f"{related}"
        else:
            return f"{value},{related}"

    def get_related(self, to_table, filter, related):
        return "get_related"

    def data(self, row, col, role="display"):
        if role == "display":
            colName = self.columns[col]
            value = self.get_record(row).get(colName, "")
            meta = self.meta[col]
            if meta.get("relation"):
                value = self._get_related(value, meta)
            elif "radio" in meta["control"]:
                if meta.get("num"):
                    value = meta.get("pic").split(";")[int(num(value)) - 1]
            elif meta["datatype"] == "date":
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d").strftime(
                        zzapp.DATA_FORMAT_STRING
                    )
                except Exception:
                    value = ""
            return value

    def alignment(self, col):
        if self.meta[col].get("relation"):
            return 7
        elif "radio" in self.meta[col]["control"] and self.meta[col].get("num"):
            return 7
        return self.alignments[col]

    def column_header_data(self, col):
        return self.headers[col]

    def row_header_data(self, row):
        return f"{row}"

    def row_count(self):
        if self.use_proxy:
            return len(self.proxy_records)
        else:
            return len(self.records)

    def column_count(self):
        return len(self.columns)


class ZzCsvModel(ZzModel):
    def __init__(self, csv_file_object=None):
        super().__init__()
        csv_dict = csv.DictReader(csv_file_object)

        # If there are names with space -  replace spaces in columns names
        if [filename for filename in csv_dict.fieldnames if " " in filename]:
            fieldnames = [x.replace(" ", "_") for x in csv_dict.fieldnames]
            csv_dict = csv.DictReader(csv_file_object, fieldnames)
        self.set_records([x for x in csv_dict])
        self.filterable = True

    def update(self, record: dict, current_row):
        self.records[current_row] = record
        self.data_changed = True
        self.refresh()
        return True

    def insert(self, record: dict, current_row):
        self.records.append(record)
        self.data_changed = True
        self.refresh()
        return True

    def delete(self, row_number):
        self.records.pop(row_number)
        self.data_changed = True
        self.refresh()
        return True

    def set_where(self, where_text=""):
        self.where_text = where_text
        if self.where_text:
            self.use_proxy = True
            self.proxy_records = []
            for row, rec in enumerate(self.records):
                if eval(self.where_text, rec):
                    self.proxy_records.append(row)
        else:
            self.use_proxy = False
        self.refresh()

    def set_order(self, order_data=""):
        super().set_order(order_data=order_data)

        colname = self.order_text

        if self.proxy_records:
            sort_records = {}
            for x in range(len(self.proxy_records)):
                value = self.records[self.proxy_records[x]][colname]
                if value not in sort_records:
                    sort_records[value] = [self.proxy_records[x]]
                else:
                    sort_records[value].append(self.proxy_records[x])
        else:
            sort_records = {}
            for x in range(len(self.records)):
                if self.records[x][colname] not in sort_records:
                    sort_records[self.records[x][colname]] = [x]
                else:
                    sort_records[self.records[x][colname]].append(x)

        sorted_keys = sorted([x for x in sort_records.keys()])
        # sorted_keys.sort()
        tmp_proxy_records = []
        for x in sorted_keys:
            for y in sort_records[x]:
                tmp_proxy_records.append(y)

        self.proxy_records = tmp_proxy_records
        self.use_proxy = True


class ZzCursorModel(ZzModel):
    def __init__(self, cursor: ZzCursor = None):
        super().__init__()
        self.cursor = cursor

    def get_table_name(self):
        return self.cursor.table_name

    def row_count(self):
        return self.cursor.row_count()

    def get_record(self, row):
        return self.cursor.record(row)

    def refresh(self):
        super().refresh()
        self.cursor.refresh()

    def delete(self, current_row=0):
        self.set_data_error()
        record = self.get_record(current_row)
        if self.cursor.delete(record):
            self.refresh()
            return True
        else:
            self.set_data_error(self.cursor.last_sql_error())
            return False

    def update(self, record: dict, current_row=0):
        self.set_data_error()
        if self.cursor.update(record):
            self.refresh()
            return True
        else:
            self.set_data_error(self.cursor.last_sql_error())
            return False

    def insert(self, record: dict, current_row=0):
        self.set_data_error()
        if self.cursor.insert(record):
            self.refresh()
            return True
        else:
            self.set_data_error(self.cursor.last_sql_error())
            return False

    def get_related(self, to_table, filter, related):
        db: ZzDb = self.cursor.zz_db
        return db.get(to_table, filter, related)

    def set_order(self, order_data):
        super().set_order(order_data=order_data)
        colname = self.order_text
        self.cursor.set_order(colname)

    def add_column(self, meta):
        db: ZzDb = self.cursor.zz_db
        db_meta = db.db_schema.get_schema_table_attr(
            self.cursor.table_name, meta["name"]
        )
        meta["pk"] = db_meta.get("pk", "")
        meta["datatype"] = db_meta.get("datatype", meta["datatype"])
        if num(meta["datalen"]) < num(db_meta.get("datalen", 10)):
            meta["datalen"] = int(num(db_meta.get("datalen", 10)))
        if "datadec" not in meta:
            meta["datadec"] = int(num(db_meta.get("datadec", 2)))
        return super().add_column(meta)

    def set_where(self, where_text=""):
        self.cursor.set_where(where_text)
        return super().set_where(where_text)
