from telebot.apihelper import ApiException

import src.bot
import src.queue
from src.models import User
from src.utils import logger


bot = src.bot.app


class Route:
    def __init__(self, message):
        self.message = message

        User.create(message.from_user)

        self.output = self.primary()

        logger.info(
            f'Message "{message.text}" from {message.from_user.id}'
        )

        if self.output:
            src.queue.QUEUE.put(self.task)

    @staticmethod
    def send_message(*args, **kwargs):
        try:
            return bot.send_message(*args, **kwargs)
        except ApiException as e:
            logger.error(e)

    @staticmethod
    def edit_message_text(*args, **kwargs):
        try:
            return bot.edit_message_text(*args, **kwargs)
        except ApiException as e:
            logger.error(e)

    @staticmethod
    def send_audio(*args, **kwargs):
        try:
            return bot.send_audio(*args, **kwargs)
        except ApiException as e:
            logger.error(e)

    @staticmethod
    def delete_message(*args, **kwargs):
        try:
            return bot.delete_message(*args, **kwargs)
        except ApiException as e:
            logger.error(e)

    def primary(self):
        return None

    def task(self):
        pass
