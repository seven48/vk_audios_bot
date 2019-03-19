from datetime import datetime
from sys import stderr


def error(text):
    prefix = f'[ {datetime.now().strftime("%x %X")} ] ERROR '
    stderr.write(f'\033[93m{prefix} {text}\033[0m\n')


def info(text):
    prefix = f'[ {datetime.now().strftime("%x %X")} ] INFO '
    stderr.write(f'{prefix} {text}\n')
