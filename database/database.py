import pandas as pd
import sqlite3
import os

class Database():

    def __init__(self) -> None:
        self.con = None
        self.cur = None

    def connect(self):
        self.con = sqlite3.connect('database/deputies.db')

    def close(self):
        self.con.close()
        self.con = None

    def exists(self):
        return os.path.exists('database/deputies.db')

    def save(self, data):
        self.connect()
        dataframe = pd.DataFrame.from_dict(data)
        dataframe.to_sql('deputies', self.con, if_exists='replace', index=False)