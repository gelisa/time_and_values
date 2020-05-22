import numpy as np
from os import path
from IPython.display import display

from table import Table


class Tasks(Table):
    def __init__(self):
        super().__init__()
        self.path = path.join('data', 'tasks.csv')
        self.columns = ['value_id', 'task_id', 'task', 'goal_min', 'goal_max', 'points']
        self.table = self.load_or_create()

    def _get_next_id(self, value_id):
        the_max = self.table[self.table.value_id == value_id].task_id.max()
        if the_max is np.nan:
            return 1
        else:
            return the_max + 1

    def add_task(self, value_id, task_name, goal_min=0, goal_max=0):
        if not self._is_task_present(task_name):
            if goal_min > goal_max:
                goal_max, goal_min = goal_min, goal_max
            self.table = self.table.append(
                {'value_id': value_id,
                 'task_id': self._get_next_id(value_id),
                 'task': task_name,
                 'goal_min': np.round(goal_min, 2),
                 'goal_max': np.round(goal_max, 2)},
                ignore_index=True
            )
            self.record()
        else:
            print('The task is present. Do you want to adjust goals?')

    def _is_task_present(self, task_name):
        if self.table[self.table.task == task_name].shape[0] > 0:
            return True
        else:
            return False

    def _locate_value(self, task_name):
        return self.table[self.table.task == task_name].value_id.iloc[0]

    def remove_task(self, task_name):
        self.table = self.table[self.table.task != task_name].copy()

    def show_value(self, value_id):
        di


