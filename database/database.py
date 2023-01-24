import pandas as pd
import sqlite3
import json
import os

class Database():

    ## General purpose MySQL functions

    def __init__(self) -> None:
        self.con = None
        self.cur = None

    def connect(self):
        self.con = sqlite3.connect('database/db.sqlite')

    def close(self):
        self.con.close()
        self.con = None

    def exists(self):
        return os.path.exists('database/db.sqlite')

    ## End of general purposes functionss

    def save(self, data):
        self.connect()
        dataframe = pd.DataFrame.from_dict(data)
        dataframe.to_sql('deputies', self.con, if_exists='replace', index=False)
        self.close()

    def read_basic(self):
        self.connect()
        dataframe = pd.read_sql("SELECT id, name, party, state, status FROM deputies", self.con)
        self.close()

        ## Data needs some sanitizing before utilizing, as it comes in a [{'columns':[...], 'data':[[...], [...], ...]}]
        ## Needs to return a list of dicts with column, value pair.

        deputies = list()

        json_string = dataframe.to_json(orient='split', index=False, force_ascii=False)
        json_item = json.loads(json_string)
        for row in json_item['data']:
            dict_item = dict(zip(json_item['columns'], row))
            deputies.append(dict_item)
        return deputies

    def read_detailed(self, id):
        self.connect()
        dataframe = pd.read_sql(f"SELECT * FROM deputies WHERE id = ?", self.con, params=[id])
        self.close()
        data = dataframe.to_dict(orient='index')[0]
        return data
