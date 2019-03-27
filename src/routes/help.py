import src.bot
from src.routes.abstract_route import Route

bot = src.bot.app


@bot.message_handler(commands=['help'])
class HelpRoute(Route):
    def primary(self):
        with open('./src/texts/help.md') as the_file:
            bot.send_message(
                self.message.chat.id,
                the_file.read(),
                parse_mode='Markdown'
            )
