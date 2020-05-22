from datetime import datetime, timedelta

from tasks import Tasks
from values import Values
from locks import Locks
from time_sheet import TimeSheet
from table import Table


class Advice(Table):
    def __init__(self, add_tomorrow):
        super().__init__()
        self.path = None
        self.columns = []
        self.v = Values()
        self.t = Tasks()
        self.l = Locks()
        self.ts = TimeSheet()
        self.table = self.compare_goal_actual(add_tomorrow)

    @staticmethod
    def _get_week(add_tomorrow):

        if add_tomorrow:
            last_date = (datetime.today() + timedelta(days=1)).date()
        else:
            last_date = datetime.today().date()

        first_date = last_date - timedelta(days=7)
        return str(first_date), str(last_date)

    @staticmethod
    def _add_deficit(actuals):
        actuals = actuals.copy()
        actuals.loc[:, 'deficit'] = (actuals.goal_min - actuals.entry).apply(lambda x: max(0, x))
        return actuals

    @staticmethod
    def _add_excess(actuals):
        actuals = actuals.copy()
        actuals.loc[:, 'excess'] = (actuals.entry - actuals.goal_max).apply(lambda x: max(0, x))
        return actuals

    @staticmethod
    def _add_opportunity(actuals):
        actuals = actuals.copy()
        actuals.loc[:, 'opportunity'] = (actuals.goal_max - actuals.entry).apply(lambda x: max(0, x))
        return actuals

    @staticmethod
    def _add_points(actuals):
        actuals = actuals.copy()
        actuals.loc[:, 'deficit_points'] = actuals.points * actuals.deficit
        actuals.loc[:, 'excess_points'] = actuals.points * actuals.excess
        actuals.loc[:, 'opportunity_points'] = actuals.points * actuals.opportunity
        return actuals

    def compare_goal_actual(self, add_tomorrow=False):
        relevant = self.ts.between(*self._get_week(add_tomorrow))
        # print(relevant)
        actuals = relevant.groupby(['value_id', 'task']).entry.sum().reset_index()
        actuals = actuals.merge(self.t.table, on=['value_id', 'task'], how='right').fillna(0)
        return (
            actuals
            .pipe(self._add_deficit)
            .pipe(self._add_excess)
            .pipe(self._add_opportunity)
            .pipe(self._add_points)
        ).sort_values(['deficit_points', 'opportunity_points'], ascending=[False, False])

    def _get_ith_candidate(self, i):
        return self.table.sort_values(
            ['deficit_points', 'opportunity_points'],
            ascending=[False, False]
        ).iloc[i]

    def propose_next(self):
        for i in range(self.table.shape[0]):
            top_choice = self._get_ith_candidate(i)
            has_lock = self._check_the_locks(top_choice['value_id'], top_choice['task'])
            if not has_lock:
                answer = input(self._format_proposal(top_choice))
                if_stop, till_when = interpret_answer(answer)
                if if_stop:
                    print("Okay. Let's do it!")
                    break
                else:
                    self.l.add_new_lock(top_choice['value_id'], top_choice['task'], till_when)
            else:
                continue
        else:
            print('out of options wanna repeat?')

    def _format_proposal(self, entry):
        vn = self.v.get_value_name(entry['value_id'])
        return '''
        Should you do {vn}. {t} perhaps?
        Deficit: {dp} ({d} hours),
        Opportunity: {op} ({o} hours)
        '''.format(
            vn=vn,
            t=entry['task'],
            dp=entry['deficit_points'],
            d=entry['deficit'],
            op=entry['opportunity_points'],
            o=entry['opportunity']
        )

    def _check_the_locks(self, value_id, task):
        disturb_times = self.l.table.groupby(['value_id', 'task']).disturb_again_on.max()
        try:
            max_time = disturb_times[value_id, task]
        except KeyError:
            return False
        if datetime.now() > max_time:
            return False
        else:
            return True


def interpret_answer(answer):
    if answer in ['yes', 'sure']:
        return True, None
    if answer in ['later', 'tomorrow', 'next week']:
        if answer == 'tomorrow':
            date = get_today_datetime() + timedelta(days=1)
        elif answer == 'next week':
            date = get_today_datetime() + timedelta(days=7)
        else:
            date = datetime.now() + timedelta(hours=1)
        return False, date


def get_today_datetime():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)












