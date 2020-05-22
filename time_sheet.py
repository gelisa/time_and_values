from datetime import datetime
import numpy as np
from os import path

from table import Table
from tasks import Tasks


class TimeSheet(Table):
    def __init__(self):
        super().__init__()
        self.path = path.join('data', 'time_sheet.csv')
        self.columns = ['datestr', 'value_id', 'task', 'entry', 'points']
        self.table = self.load_or_create()

    def add_entry(self, value_id, task, how_long, datestr=str(datetime.today().date())):
        t = Tasks()
        try:
            points = t.table[
                (t.table.value_id == value_id) &
                (t.table.task == task)].points.iloc[0]
        except IndexError:
            print('no task {} for value {}'.format(task, value_id))
        else:
            self.table = self.table.append(
                {
                    'datestr': datestr,
                    'value_id': value_id,
                    'task': task,
                    'entry': np.round(how_long, 2),
                    'points': np.round(how_long * points, 2)
                },
                ignore_index=True
            ).sort_values(['datestr', 'value_id'], ascending=[False, True])

            self.record()

    def sum(self, value_id=None):
        if not value_id:
            return self.table.entry.sum()
        else:
            return self[value_id].entry.sum()

    def select_task(self, value_id, task):
        return self.table[
            (self.table.value_id == value_id) &
            (self.table.task == task)
        ]

    def sum_task(self, value_id, task):
        return self.select_task(value_id, task).entry.sum()

    def between(self, ds1, ds2):
        return self.table[self.table.datestr.between(ds1, ds2)]


