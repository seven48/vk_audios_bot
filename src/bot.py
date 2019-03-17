import os

import telebot

import src.parser

TOKEN = os.environ.get('TOKEN')

app = telebot.TeleBot(TOKEN)

_username = os.environ.get('USERNAME')
_password = os.environ.get('PASSWORD')

if os.environ.get('PROXY'):
    telebot.apihelper.proxy = {
        "https": os.environ.get('PROXY')
    }

parser = src.parser.Parser(_username, _password)
