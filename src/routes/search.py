import src.bot
import src.models

from src.utils.logger import log

bot = src.bot.app
parser = src.bot.parser


@bot.message_handler(content_types=['text'])
def helper(message):
    output_message = bot.send_message(
        message.chat.id,
        log('Search', message.text),
        parse_mode="Markdown"
    )

    data = parser.search(message.text)

    print(data)

    bot.edit_message_text(
        'Найдено',
        chat_id=message.chat.id,
        message_id=output_message.message_id
    )
