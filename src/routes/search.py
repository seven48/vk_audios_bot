import src.bot
from src.routes.abstract_route import Route

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

        title = f'{len(playlists["list"])} плейлистов'

        items = []
        for item in playlists['list']:
            items.append(f'*{item["title"]}* - _{item["subtitle"]}_')

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'

    @staticmethod
    def _get_artists(artists):
        if not artists:
            return ''

        title = f'{len(artists["list"])} исполнителей'

        items = []
        for item in artists['list']:
            items.append(f'*{item["name"]}*')

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'

    @staticmethod
    def _get_tracks(tracks):
        if not tracks:
            return ''

        title = f'{len(tracks["list"])} композиций'

        items = []
        for item in tracks['list']:
            items.append(f'*{item["artist"]}* - {item["title"]}')

        return f'{title}\n' + \
            '\n'.join(items) + \
            '\n\n'
