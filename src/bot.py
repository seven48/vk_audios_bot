import os

import telebot

import src.parser

TOKEN = os.environ.get('TOKEN')

app = telebot.TeleBot(TOKEN)

username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')

if os.environ.get('PROXY'):
    telebot.apihelper.proxy = {
        "https": os.environ.get('PROXY')
    }

parser = src.parser.Parser(username, password)
