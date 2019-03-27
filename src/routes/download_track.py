import os
from io import BytesIO

import requests
from vaud import decode

import src.bot
from src.routes.abstract_route import Route
from src.models import Track


bot = src.bot.app
parser = src.bot.parser


@bot.message_handler(regexp='^\/t_(\d+)_(\d+)$')  # noqa: W605
class DownloadTrackRoute(Route):
    def primary(self):
        return self.send_message(
            chat_id=self.message.chat.id,
            text='Загрузка композиции'
        )

    def task(self):
        _, owner_id, data_id = self.message.text.split('_')

        record = Track.get(owner_id, data_id)

        if not record:
            return self.edit_message_text(
                text='Не удалось найти такую композицию',
                chat_id=self.output.chat.id,
                message_id=self.output.message_id
            )

        vk_user_id = int(os.environ.get('VK_USER_ID'))
        link = decode(vk_user_id, record.link)

        track = requests.get(link, stream=True)

        self.send_audio(
            self.output.chat.id,
            BytesIO(track.content),
            performer=record.artist,
            title=record.title
        )

        self.delete_message(
            self.output.chat.id,
            self.output.message_id
        )
        self.delete_message(
            self.message.chat.id,
            self.message.message_id
        )
