from os import makedirs
from os.path import exists
from datetime import datetime


def complete_digits(digits, n_digits):
    digits = str(digits)
    return '0' * (n_digits - len(digits)) + digits


def current_date_time():
    now = datetime.now()
    return '{}_{}_{}__{}_{}_{}'.format(
        complete_digits(now.year, 4),
        complete_digits(now.month, 2),
        complete_digits(now.day, 2),
        complete_digits(now.hour, 2),
        complete_digits(now.minute, 2),
        complete_digits(now.second, 2)
    )


def touch_dir(directory):
    if not(exists(directory)):
        makedirs(directory)
