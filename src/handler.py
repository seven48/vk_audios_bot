import src.bot

bot = src.bot.app
parser = src.bot.parser


class AbstractHandler:
    def __init__(self, task, done):
        self.task = task
        self.done = done

        query = self.query()
        message = self.parse_query(query)
        self.send(message)

    def query(self):
        return {}

    def parse_query(self, query):
        return str(query)

    def send(self, message):
        return bot.edit_message_text(
            message,
            chat_id=self.task.output['chat']['id'],
            message_id=self.task.output['message_id'],
            parse_mode='Markdown'
        )


class SearchHandler(AbstractHandler):
    def query(self):
        return parser.search(self.task.message['text'])

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

    def parse_query(self, query):
        title = query['query']

        artists = self._get_artists(query.get('artists'))
        playlists = self._get_playlists(query.get('playlists'))
        tracks = self._get_tracks(query.get('tracks'))

        result = ''
        if not any([artists, playlists, tracks]):
            result = 'Абсолютно ничего'

        return f'По запросу `{title}` найдено:\n\n' \
            f'{artists}' \
            f'{playlists}' \
            f'{tracks}' \
            f'{result}'
