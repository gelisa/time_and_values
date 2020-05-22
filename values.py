import numpy as np
from os import path

from table import Table


class Values(Table):
    def __init__(self):
        super().__init__()
        self.path = path.join('data', 'values.csv')
        self.columns = ['value_id', 'value']
        self.table = self.load_or_create()

    def _get_next_id(self):
        if self.table.value_id.max() is np.nan:
            return 1
        else:
            return self.table.value_id.max() + 1

    def add_value(self, value_name):
        self.table = self.table.append(
            {'value_id': self._get_next_id(), 'value': value_name},
            ignore_index=True
        )
        self.record()

    def get_value_name(self, value_id):
        return self[value_id].value.iloc[0]




