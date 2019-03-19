import os

from multiprocessing import Process

from src.utils import logger


class MasterProcess:
    def __init__(self, queue):
        self._processes = []
        self.queue = queue
        self._proc_count = int(os.environ.get('PROC_COUNT', '1'))

        try:
            self._allocate()
        except KeyboardInterrupt:
            logger.error('Shutting down by keyboard interrupt...')
            for process in self._processes:
                process.terminate()
                pid = process.ident
                logger.info(f'Process {pid} killed')

    def _allocate(self):
        # Task allocation
        while True:
            # Clear process stack
            for process in self._processes:
                if not process.is_alive():
                    pid = process.ident
                    code = process.exitcode

                    logger.info(f'Process {pid} completed with code {code}')

                    self._processes.remove(process)

            # Adding new tasks
            for _ in range(self._proc_count - len(self._processes)):
                if not self.queue.qsize():  # If empty
                    break

                task = self.queue.get()

                process = Process(target=task)
                process.start()
                self._processes.append(process)

                logger.info(f'Process {process.ident} created')
