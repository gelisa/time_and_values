from datetime import datetime, timedelta


def get_today_datetime():
    return datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)


def get_today_datestr():
    return str(datetime.today().date())


def datestr_to_date(datestr):
    return datetime.strptime(datestr, '%Y-%m-%d')


def add_days_to_datestr(datestr, day_delta):
    new_day = datestr_to_date(datestr) + timedelta(days=day_delta)
    return datetime.strftime(new_day, '%Y-%m-%d')


def make_date_range_generator(startdt, enddt, step=1):
    dt = startdt
    while dt < enddt:
        yield dt
        dt = add_days_to_datestr(dt, step)

