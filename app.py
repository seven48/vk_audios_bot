import sys
from requests import exceptions
from multiprocessing import Process

import src.routes
import src.queue
from src.master import MasterProcess
from src.utils import logger


if __name__ == "__main__":
    master = Process(target=MasterProcess, args=(src.queue.QUEUE,))
    master.start()

    try:
        src.bot.app.get_me()
    except exceptions.ConnectionError:
        logger.error('Telegram proxy error. Terminating...')

        master.terminate()
        sys.exit(1)

    src.bot.app.polling()
