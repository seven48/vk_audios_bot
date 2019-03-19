from multiprocessing import Process

import src.routes
import src.queue
from src.master import MasterProcess


if __name__ == "__main__":
    master = Process(target=MasterProcess, args=(src.queue.QUEUE,))
    master.start()

    src.bot.app.polling()
