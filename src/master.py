import os

from multiprocessing import Process

from src.handler import SearchHandler
from src.models import Queue
from src.utils import logger


class MasterProcess:
    def __init__(self):
        self._processes = []
        self._proc_count = int(os.environ.get('PROC_COUNT', '1'))

        self._allocate()

    def _allocate(self):
        """ Task allocation """
        while True:
            self._clear_process_stack()
            self._adding_new_tasks()

    def _adding_new_tasks(self):
        # Adding new tasks
        for _ in range(self._proc_count - len(self._processes)):
            task = Queue.pop()

            if not task:
                break

            handlers = {
                'Search': SearchHandler
            }

            process = Process(
                target=handlers.get(task.type),
                args=(task, self._get_done_func(task.id))
            )
            process.start()
            logger.info(f'Created new process {process.ident}')
            self._processes.append(process)

    def _clear_process_stack(self):
        """ Clear process stack """
        for process in self._processes:
            if not process.is_alive():
                logger.info(f'Process ${process.ident} removed')
                self._processes.remove(process)

    @staticmethod
    def _get_done_func(_id):
        def func():
            Queue.done(_id)

        return func
