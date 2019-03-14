import json
import os
from datetime import datetime
from sys import stderr

LANG = os.environ.get('LOCALIZATION') or 'RU'


def bot(name, *args):
    with open('./src/texts/messages.json') as the_file:
        messages = json.loads(the_file.read())
        answer = messages.get(LANG).get(name)
        if answer:
            return answer.format(*args)
        else:
            return name.format(*args)


def info(text):
    prefix = '[ {} ]'.format(datetime.now().strftime('%x %X'))
    stderr.write('{} {}\n'.format(prefix, text))
