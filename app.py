import os

from multiprocessing import Process

import telebot

import src.routes
import src.bot
import src.stack


if __name__ == "__main__":
    if os.environ.get('PROXY'):
        telebot.apihelper.proxy = {
            "https": os.environ.get('PROXY')
        }

    PROC_COUNT = int(os.environ.get('PROC_COUNT', '1'))
    for _ in range(PROC_COUNT):
        queue = Process(target=src.stack.run)
        queue.start()

    src.bot.app.polling()
