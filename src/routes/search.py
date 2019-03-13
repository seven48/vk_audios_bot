import src.bot
import src.models
import src.stack

from src.utils.logger import log

bot = src.bot.app
parser = src.bot.parser


@bot.message_handler(content_types=['text'])
def helper(message):
    output = bot.send_message(
        message.chat.id,
        log('Search', message.text),
        parse_mode="Markdown"
    )

    user = src.models.User.create(message.from_user)

    src.models.Queue.add(
        _type='Search',
        user=user,
        message=message.json,
        output=output.json
    )

    pop = src.models.Queue.pop()
    print(pop)
    import pdb; pdb.set_trace()

    # parser.search(message.text)

    # bot.edit_message_text(
    #     'done',
    #     chat_id=message.chat.id,
    #     message_id=output.message_id,
    #     parse_mode='Markdown'
    # )
