import os

import pymysql
from pymysql.cursors import DictCursor


class DataBaseConnector:
    def __init__(self):
        # データベース接続とカーソル生成
        self.connection = pymysql.connect(host=os.environ["DB_HOST"],
                                          user=os.environ["DB_USERNAME"],
                                          password=os.environ["DB_PASSWORD"],
                                          db=os.environ["DB_DATABASE"],
                                          charset='utf8',
                                          cursorclass=DictCursor)

        self.cursor = self.connection.cursor()
        self.cursor.execute(
                            "CREATE TABLE IF NOT EXISTS traffic ("
                            "id INTEGER PRIMARY KEY, "
                            "name TEXT, "
                            "pedestrian INTEGER, "
                            "bicycle INTEGER, "
                            "motorbike INTEGER, "
                            "passenger_car INTEGER, "
                            "small_freight_car INTEGER, "
                            "bus INTEGER, "
                            "ordinary_freight_car INTEGER"
                            ")")
        self.cursor.execute("SELECT COUNT(id) from traffic")
        rows = self.cursor.fetchall()
        self.id = list(rows[0].values())[0]

    def add_row(self, name, pedestrian, bicycle, motorbike, passenger_car,
                small_freight_car, bus, ordinary_freight_car):
        sql = "INSERT INTO traffic (id, name, pedestrian, bicycle, motorbike,"\
                                 "passenger_car, small_freight_car, bus," \
                                 "ordinary_freight_car) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        values = (self.id, name, pedestrian, bicycle, motorbike, passenger_car,
                  small_freight_car, bus, ordinary_freight_car)
        self.cursor.execute(sql, values)
        # 保存を実行（忘れると保存されないので注意）
        self.connection.commit()
        return 0

    def output_meta_date(self):
        # 1. カーソルをイテレータ (iterator) として扱う
        self.cursor.execute("SELECT * FROM traffic")
        out_put = []
        for row in self.cursor:
            # rowオブジェクトでデータが取得できる。タプル型の結果が取得
            out_put.append(row)
        return out_put

    def delete_rows(self):
        self.cursor.execute("TRUNCATE TABLE traffic")
        return 0

    def __del__(self):
        # 接続を閉じる
        self.connection.close()
        return 0
