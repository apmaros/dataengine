import typing as t
from datetime import datetime
from random import randint


def rand(l: t.List):
    return l[randint(0, len(l) - 1)]


def to_datetime(s):
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
