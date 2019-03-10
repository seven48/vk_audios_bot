import os
import json

LANG = os.environ.get('LOCALIZATION') or 'RU'


def log(name, *args):
    with open('./src/texts/messages.json') as the_file:
        messages = json.loads(the_file.read())
        answer = messages.get(LANG).get(name)
        if answer:
            return answer.format(*args)
        else:
            return name.format(*args)
