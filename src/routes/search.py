import src.models

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
        type='Search',
        user=user,
        message=message.json,
        output=output.json
    )
