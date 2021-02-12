import os

from huey import SqliteHuey

huey = SqliteHuey(
    filename="huey.db",
)


@huey.task(name='xxx')
def add(a, b):
    print(os.getpid(), f": {a}+{b}={a+b}")
    return a + b
