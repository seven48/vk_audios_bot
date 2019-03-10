import os
import sys

import telebot

TOKEN = os.environ.get('TOKEN')

if not TOKEN:
    sys.exit('TOKEN variable is required')

app = telebot.TeleBot(TOKEN)
