import time
import datetime
from random import random


def get_random_datetime(start, end, format='%Y-%m-%dT%H:%M:%S'):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + random() * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def get_current_date():
    """
    Return datetime object of current date
    """
    return datetime.datetime.now()


def get_date_with_shift_by_hours(hours=12):
    """
    Return datetime object with shift to <hours> of current date
    """
    return datetime.datetime.now() + datetime.timedelta(hours=hours)


def date_to_unix_time(date):
    """
    Convert datetime date to unix time format (ms from 01.01.1970)
    :param date: datetime object
    """
    return time.mktime(date.timetuple())
