import os
import csv
import time
from io import StringIO

from flask import request, make_response
from models.models import DataBaseConnector

# 保存できるファイルの拡張子
ALLOWED_EXTENSION_NAMES = {"mp4", "MOV"}
COLUMN_NAME = ["ID", "動画名", "歩行者数", "自転車", "動力付き二輪車", "乗用車",
               "小型貨物車", "バス", "普通貨物"]

NAME_THRESH = 20


def allowed_extensions(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSION_NAMES


class Flask_Event:
    def __init__(self):
        self.file_name = None
        pass

    def save_file_name(self, file_name):
        self.file_name = file_name
        return 0

    @staticmethod
    def upload_files(upload_folder, file):
        if file and allowed_extensions(file.filename):
            print("AAAAAAAAAA", allowed_extensions(file.filename))
            file_name = file.filename
            start = time.time()
            file.save(os.path.join(upload_folder, file_name))
            print("upload time is ", str(time.time() - start))
            return 0
        else:
            return 1

    def insert_date(self):
        title = self.file_name
        pedestrian = int(request.form["pedestrian_num"])
        bicycle = int(request.form["bicycle_num"])
        motorbike = int(request.form["motorbike_num"])
        passenger_car = int(request.form["passenger_car_num"])
        small_freight_car = int(request.form["small_freight_car_num"])
        bus = int(request.form["bus_num"])
        ordinary_freight_car = int(request.form["ordinary_freight_car_num"])
        data_base = DataBaseConnector()
        data_base.add_row(title, pedestrian, bicycle, motorbike, passenger_car,
                          small_freight_car, bus, ordinary_freight_car)
        return 0

    @staticmethod
    def init_table():
        data_base = DataBaseConnector()
        data_base.delete_rows()
        return data_base.output_meta_date()

    @staticmethod
    def output_meta_date():
        data_base = DataBaseConnector()
        output_data = data_base.output_meta_date()
        for row in output_data:
            if row["name"] is None:
                row["long_name"] = 0
            elif len(row["name"]) >= NAME_THRESH:
                row["long_name"] = 1
            else:
                row["long_name"] = 0
        return output_data

    @staticmethod
    def save_csv():
        f = StringIO()
        data_base = DataBaseConnector()
        data_rows = data_base.output_meta_date()
        output_keys = COLUMN_NAME
        output_values = []
        for row in data_rows:
            output_values.append(list(row.values()))
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_ALL,
                            lineterminator="\n")
        writer.writerow(output_keys)
        writer.writerows(output_values)
        res = make_response()
        res.data = f.getvalue()
        res.headers["Content-Type"] = "text/csv"
        res.headers["Content-Disposition"] = "attachment; filename=traffic.csv"
        return res
