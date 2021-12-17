import typing as t
from random import randint


def rand(l: t.List):
    return l[randint(0, len(l) - 1)]
