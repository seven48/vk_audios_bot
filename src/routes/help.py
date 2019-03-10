import src.bot

bot = src.bot.app


@bot.message_handler(commands=['help'])
def helper(message):
    with open('./src/texts/help.md') as the_file:
        bot.send_message(
            message.chat.id,
            the_file.read(),
            parse_mode="Markdown"
        )
