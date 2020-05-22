import pandas as pd
from os import path
from IPython.display import display


class Table(object):
    def __init__(self):
        self.path = path.join('data', 'example.csv')
        self.columns = ['value_id', 'some_column']
        self.table = pd.DataFrame(columns=self.columns)

    def record(self):
        self.table.to_csv(self.path, index=False)

    def reset(self, inplace=True):
        data = pd.DataFrame(columns=self.columns)
        if inplace:
            self.table = data
            self.record()
        else:
            return data

    def load_or_create(self):
        try:
            data = pd.read_csv(self.path)
            if data.columns.tolist() != self.columns:
                print('your data columns are not the same as specified class columns. please check')
                print(data.columns.tolist())
                print(self.columns)
        except FileNotFoundError:
            data = self.reset(False)
            self.record()

        return data

    def __getitem__(self, item):
        return self.table[self.table.value_id == item]

    def print(self):
        display(self.table)
        return ''

    def __repr__(self):
        return self.print()

    def sample(self, x=None):
        return self.table.sample(x)

    def groupby(self, *args, **kwargs):
        return self.table.groupby(*args, **kwargs)


