import src.bot
from src.models import Queue
from src.utils import logger

bot = src.bot.app
parser = src.bot.parser


def search_type_handler(task):
    context = parser.search(task.message['text'])

    task.user.update(context=context)
    task.user.save()

    message = 'Выполнено'

    bot.edit_message_text(
        message,
        chat_id=task.output['chat']['id'],
        message_id=task.output['message_id']
    )


def run():
    handlers = {
        'Search': search_type_handler
    }

    while True:
        task = Queue.pop()

        if not task:
            continue

        logger.info(
            'Task typed {} #{} started for @{} ({})'
            .format(
                task._type,
                task.id,
                task.user.username,
                task.user.user_id
            )
        )

        try:
            handlers[task._type](task)
        # else:
        #     logger.info(
        #         'Task typed {} #{} finished for @{} ({}) SUCCESS'
        #         .format(
        #             task._type,
        #             task.id,
        #             task.user.username,
        #             task.user.user_id
        #         )
        #     )
        finally:
            Queue.done(task.id)


if __name__ == "__main__":
    run()
