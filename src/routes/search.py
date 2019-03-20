import src.bot
from src.routes.abstract_route import Route
from src.models import Track, Artist, Playlist
from src.utils.escape import telegram_escape

bot = src.bot.app
parser = src.bot.parser


@bot.message_handler(content_types=['text'])
class SearchRoute(Route):
    def primary(self):
        return self.send_message(
            self.message.chat.id,
            f'Поиск по запросу `{self.message.text}`',
            parse_mode="Markdown"
        )

    def task(self):
        query = parser.search(self.message.text)

        title = query['query']

        artists = self._get_artists(query.get('artists'))
        playlists = self._get_playlists(query.get('playlists'))
        tracks = self._get_tracks(query.get('tracks'))

        result = ''
        if not any([artists, playlists, tracks]):
            result = 'Абсолютно ничего'

        message_text = f'По запросу `{title}` найдено:\n\n' \
            f'{artists}' \
            f'{playlists}' \
            f'{tracks}' \
            f'{result}'

        self.edit_message_text(
            message_text,
            chat_id=self.output.chat.id,
            message_id=self.output.message_id,
            parse_mode='Markdown'
        )

    @staticmethod
    def _get_playlists(playlists):
        if not playlists:
            return ''

        title = 'Плейлисты'

        items = []
        for item in playlists['list']:
            record = Playlist.create(item)
            _title = telegram_escape(item["title"])
            subtitle = telegram_escape(item["subtitle"])
            items.append(f'/p\_{record.owner_id}\_{record.data_id} *{_title}* - _{subtitle}_')  # noqa: W605,E501

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'

    @staticmethod
    def _get_artists(artists):
        if not artists:
            return ''

        title = 'Исполнители'

        items = []
        for item in artists['list']:
            record = Artist.create(item)
            name = telegram_escape(item["name"])
            link = telegram_escape(record.link)
            items.append(f'/a\_{link} *{name}*')  # noqa: W605

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'

    @staticmethod
    def _get_tracks(tracks):
        if not tracks:
            return ''

        title = 'Композиции'

        items = []
        for item in tracks['list']:
            record = Track.create(item)
            artist = telegram_escape(item["artist"])
            _title = telegram_escape(item["title"])
            items.append(
                f'/t\_{record.owner_id}\_{record.data_id} *{artist}* - {_title}'  # noqa: W605,E501
            )

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'
