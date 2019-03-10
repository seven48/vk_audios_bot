import os
import sys

import telebot

TOKEN = os.environ.get('TG_TOKEN')

if not TOKEN:
    sys.exit('TG_TOKEN variable is required')

app = telebot.TeleBot(TOKEN)
