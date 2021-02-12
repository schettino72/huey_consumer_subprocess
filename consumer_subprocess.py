from multiprocessing import Process

from huey import constants
from huey import consumer
from huey.api import TaskWrapper



def create_task(self, func, context=False, name=None, **settings):
    def execute(self):
        args, kwargs = self.data
        if self.context:
            kwargs['task'] = self

        # execute in subprocess instead of thread itself
        # return func(*args, **kwargs)
        proc = Process(target=func, args=args, kwargs=kwargs, daemon=True)
        proc.start()
        proc.join()

    attrs = {
        'context': context,
        'execute': execute,
        '__module__': func.__module__,
        '__doc__': func.__doc__}
    attrs.update(settings)

    if not name:
        name = func.__name__

    return type(name, (self.task_base,), attrs)



def monkeypatch():
    """monkeypatch huey to add subprocess worker"""
    constants.WORKER_TYPES = ('subprocess', ) # WORKER_THREAD, WORKER_GREENLET, WORKER_PROCESS
    consumer.WORKER_TO_ENVIRONMENT['subprocess'] = consumer.ThreadEnvironment
    TaskWrapper.create_task = create_task


if __name__ == '__main__':
    monkeypatch()

    # this import must be AFTER monkeypatch
    from huey.bin.huey_consumer import consumer_main

    # python consumer_subprocess.py demo_tasks.huey -k subprocess --disable_health_check --simple
    consumer_main()
