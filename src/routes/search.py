import src.bot
from src.routes.abstract_route import Route

bot = src.bot.app


@bot.message_handler(content_types=['text'])
class SearchRoute(Route):
    def primary(self):
        return bot.send_message(
            self.message.chat.id,
            f'Поиск по запросу `{self.message.text}`',
            parse_mode="Markdown"
        )
