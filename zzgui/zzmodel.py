from urllib.request import proxy_bypass


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
        self.proxy_records = []
        self.use_proxy = False
        self.meta = []
        self.editable = False
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

    def build_auto_form_from_records(self):
        # Define layout
        if self.records:
            self.zz_form.add_control("/f", "Frame with form layout")
            # Populate it with the columns from csv
            for x in self.records[0]:
                self.zz_form.add_control(x, x, control="line")
            # Assign data source
            self.zz_form.model.editable = True
            self.zz_form.actions.add_action(text="/view")

            def run_filter_data_form():
                filter_form = self.zz_form.__class__("Filter Conditions")
                #Populate form with columns
                for x in self.zz_form.controls.controls:
                    filter_form.controls.add_control(
                        name=x["name"],
                        label=x["label"],
                        control=x["control"],
                        check=False if x["name"].startswith("/") else True,
                    )

                def before_form_show():
                    #put previous filter conditions to form
                    for x in self.zz_form.model.get_where().split(" and "):
                        if "' in " not in x:
                            continue
                        column_name = x.split(" in ")[1].strip()
                        column_value = x.split(" in ")[0].strip()[1:-1]
                        filter_form.w.__getattr__(column_name).set_text(column_value)
                        filter_form.w.__getattr__(column_name).check.set_checked()

                def valid():
                    #apply new filter to grid
                    filter_list = []
                    for x in filter_form.widgets_list():
                        if x.check and x.check.is_checked():
                            filter_list.append(f"'{x.get_text()}' in {x.meta['name']}")
                    filter_string = " and ".join(filter_list)
                    self.zz_form.model.set_where(filter_string)

                filter_form.before_form_show = before_form_show
                filter_form.valid = valid
                filter_form.add_ok_cancel_buttons()
                filter_form.show_mdi_modal_form()

            self.zz_form.model.set_where()
            self.zz_form.actions.add_action("Filter", worker=run_filter_data_form, hotkey="F9")

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

    def get_where(self):
        return self.where_text

    def order_column(self, column):
        colname = self.columns[column]
        if self.proxy_records:
            work_records = self.proxy_records
        else:
            work_records = [x for x in range(len(self.records))]
        tmp_proxy_records = [0]
        # for rownum in range(1, len(self.records)):
        for rownum in work_records:
            current_value = self.records[rownum][colname]
            start = 0
            end = len(tmp_proxy_records) - 1
            while True:
                if end - start <= 4:
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

    def set_order(self, order_text=""):
        self.order_text = order_text

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
