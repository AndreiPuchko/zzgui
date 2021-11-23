if __name__ == "__main__":
    import sys

    sys.path.insert(0, ".")

    from demo.demo import demo

    demo()

# from zzgui.zzutils import num
# import datetime


class ZzModel:
    def __init__(self, zz_form):
        self.zz_form = zz_form
        self.columns = []
        self.headers = []
        self.alignments = []
        self.records = []
        self.meta = []
        self.editable = False

    def insert(self, record: dict):
        record
        pass

    def update(self, record: dict):
        record
        pass

    def delete(self, record: dict):
        record
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

    def refresh(self, row=None):
        pass

    def get_record(self, row):
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
        return len(self.records)

    def column_count(self):
        return len(self.columns)
