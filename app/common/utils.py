import datetime


def strnow():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
