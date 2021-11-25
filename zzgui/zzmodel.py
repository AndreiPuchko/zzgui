if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

import csv


# from zzgui.zzutils import num
# import datetime


class ZzModel:
    def __init__(self, zz_form=None):
        self.zz_form = zz_form
        self.columns = []
        self.headers = []
        self.alignments = []

        self.records = []
        self.proxy_records = []
        self.use_proxy = False

        self.meta = []

        self.readonly = True
        self.filterable = False

        self.order_text = ""
        self.where_text = ""

    def insert(self, record: dict):
        print(record)
        return True

    def update(self, record: dict):
        print(record)
        return True

    def delete(self, record: dict):
        print(record)
        return True

    def set_where(self, where_text=""):
        self.where_text = where_text

    def get_where(self):
        return self.where_text

    def set_order(self, order_data=""):
        if isinstance(order_data, int):
            self.order_text = self.column_header_data(order_data)
        elif isinstance(order_data, list):
            self.order_text = ",".join(order_data)
        else:
            self.order_text = order_data

    def refresh(self):
        pass

    def set_records(self, records):
        self.records = records

    def build(self):
        for meta in self.zz_form.controls.controls:
            if meta.get("name", "").startswith("/") or meta.get("formonly"):
                continue
            if meta.get("control", "") in ["button", "widget", "form"]:
                continue
            self.zz_form.model.add_column(meta)

    def add_column(self, meta):
        self.columns.append(meta["name"])
        self.headers.append(meta["label" if meta.get("saygrid") else "label"])
        self.alignments.append(meta.get("align", "7"))
        self.meta.append(meta)

    def get_record(self, row):
        if self.use_proxy:
            return self.records[self.proxy_records[row]]
        else:
            return self.records[row]

    # def _get_related(self, value, meta):
    #     if meta.get("num") and num(value) == 0:
    #         return ""
    #     elif value == "":
    #         return ""
    #     key = (meta["to_table"], f"{meta['to_field']}='{value}'", meta["related"])
    #     if key in self.relatedCache:
    #         related = self.relatedCache[key]
    #     else:
    #         related = self.get_related(
    #             meta["to_table"], f"{meta['to_field']}='{value}'", meta["related"]
    #         )
    #         self.relatedCache[key] = related
    #     if related is None:
    #         related = ""
    #     return f"{value},{related}"

    # def get_related(self, to_table, filter, related):
    #     return self.dbEngine.get(to_table, filter, related)

    def data(self, row, col, role="display"):
        if role == "display":
            colName = self.columns[col]
            value = self.get_record(row).get(colName, "")
            # meta = self.meta[col]
            # if meta.get("relation"):
            #     value = self._get_related(value, meta)
            # elif "radio" in meta["control"]:
            #     if meta.get("num"):
            #         value = meta.get("pic").split(";")[int(num(value)) - 1]
            # elif meta["datatype"] == "date":
            #     try:
            #         value = datetime.datetime.strptime(value, "%Y-%m-%d").strftime(
            #             "%d.%m.%Y"
            #         )
            #     except:
            #         value = ""
            return value

    def alignment(self, col):
        return 7
        # if self.meta[col].get("relation"):
        #     return 7
        # elif "radio" in self.meta[col]["control"] and self.meta[col].get("num"):
        #     return 7
        # return self.alignments[col]

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
    def __init__(self, zz_form=None, csv_file_object=None):
        super().__init__(zz_form=zz_form)
        csv_dict = csv.DictReader(csv_file_object)

        csv_dict = csv.DictReader(csv_file_object)
        # If there are names with space -  replace spaces in columns names
        if [filename for filename in csv_dict.fieldnames if ' ' in filename]:
            fieldnames = [x.replace(" ", "_") for x in csv_dict.fieldnames]
            csv_dict = csv.DictReader(csv_file_object, fieldnames)
        self.set_records([x for x in csv_dict])
        self.filterable = True

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
            work_records = self.proxy_records
        else:
            work_records = [x for x in range(len(self.records))]
        tmp_proxy_records = [work_records[0]]
        # for rownum in range(1, len(self.records)):
        for rownum in work_records[1:]:
            current_value = self.records[rownum][colname]
            start = 0
            end = len(tmp_proxy_records) - 1
            while True:
                if end - start <= 5:
                    for x in range(start, end + 1):
                        if current_value <= self.records[tmp_proxy_records[x]][colname]:
                            tmp_proxy_records.insert(x, rownum)
                            break
                        if x == end:
                            if x == len(tmp_proxy_records) - 1:
                                tmp_proxy_records.append(rownum)
                            else:
                                tmp_proxy_records.insert(x + 1, rownum)
                            break
                    break
                else:
                    middlepos = int((end - start) / 2) + start
                    if (
                        current_value
                        >= self.records[tmp_proxy_records[middlepos]][colname]
                    ):
                        start = middlepos
                    else:
                        end = middlepos
        self.proxy_records = tmp_proxy_records
        self.use_proxy = True
        self.refresh()
