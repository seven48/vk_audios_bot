from multiprocessing import Process

import src.routes
from src.master import MasterProcess


if __name__ == "__main__":
    master = Process(target=MasterProcess)
    master.start()

    src.bot.app.polling()
