import os
import sys

import telebot

import src.parser

TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    sys.exit('TOKEN variable is required')

app = telebot.TeleBot(TOKEN)

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if not username or not password:
    sys.exit('USERNAME and PASSWORD are required')

if os.environ.get('PROXY'):
    telebot.apihelper.proxy = {
        "https": os.environ.get('PROXY')
    }

parser = src.parser.Parser(username, password)
