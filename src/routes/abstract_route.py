from telebot.apihelper import ApiException

import src.bot
from src.models import User
from src.utils import logger


bot = src.bot.app


class Route:
    def __init__(self, message):
        self.message = message

        User.create(message.from_user)

        try:
            self.output = self.primary()
        except ApiException as e:
            logger.error(e)
        else:
            logger.info(
                f'Message "{message.text}" from {message.from_user.id}'
            )

    def primary(self):
        return None
