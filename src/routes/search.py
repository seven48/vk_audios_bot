import src.models
import src.stack

from src.utils import logger

bot = src.bot.app


@bot.message_handler(content_types=['text'])
def helper(message):
    output = bot.send_message(
        message.chat.id,
        logger.bot('Search', message.text),
        parse_mode="Markdown"
    )

    user = src.models.User.create(message.from_user)

    logger.info(
        'Message "{}" in "{}" from "@{} ({})"'
        .format(
            message.text.replace('\n', '\\n'),
            message.chat.id,
            user.username,
            user.user_id
        )
    )

    src.models.Queue.add(
        _type='Search',
        user=user,
        message=message.json,
        output=output.json
    )

    # parser.search(message.text)

    # bot.edit_message_text(
    #     'done',
    #     chat_id=message.chat.id,
    #     message_id=output.message_id,
    #     parse_mode='Markdown'
    # )
