from datetime import datetime
from sys import stderr


def error(text):
    prefix = f'[ {datetime.now().strftime("%x %X")} ] ERROR '
    message = f'{prefix} {text}\n'
    stderr.write(f'\033[93m{message}\033[0m')
    with open('errors.txt', 'a') as file:
        file.write(message)


def info(text):
    prefix = f'[ {datetime.now().strftime("%x %X")} ] INFO '
    message = f'{prefix} {text}\n'
    stderr.write(message)
    with open('info.txt', 'a') as file:
        file.write(message)
