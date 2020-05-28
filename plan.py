from os import path

from table import Table
from advice import Advice
import general_tools as tls


class Plan(Table):
    def __init__(self, add_tomorrow):
        super().__init__()
        self.for_tomorrow = add_tomorrow
        self.columns = []
        self.a = Advice(add_tomorrow)

    @property
    def path(self):
        if self.for_tomorrow:
            the_date = tl
        return path.join('data', 'plan_{}.csv')
