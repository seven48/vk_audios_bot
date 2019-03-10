import os

import telebot

import src.routes
import src.bot

if __name__ == "__main__":
    if os.environ.get('PROXY'):
        telebot.apihelper.proxy = {
            "https": os.environ.get('PROXY')
        }

    src.bot.app.polling()
