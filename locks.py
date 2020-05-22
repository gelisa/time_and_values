import pandas as pd
from os import path
from IPython.display import display

from table import Table


class Locks(Table):
    def __init__(self):
        super().__init__()
        self.path = path.join('data', 'locks.csv')
        self.columns = ['value_id', 'task', 'disturb_again_on']
        self.table = self.load_or_create()

    def load_or_create(self):
        try:
            data = pd.read_csv(self.path)
            data.loc[:, 'disturb_again_on'] = pd.to_datetime(data.disturb_again_on)
            if data.columns.tolist() != self.columns:
                print('your data columns are not the same as specified class columns. please check')
                print(data.columns.tolist())
                print(self.columns)
        except FileNotFoundError:
            data = self.reset(False)
            self.record()

        return data

    def add_new_lock(self, value_id, task, date):
        self.table = self.table.append(
            {'value_id': value_id,
             'task': task,
             'disturb_again_on': date},
            ignore_index=True
        )
        self.record()

