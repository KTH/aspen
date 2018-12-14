__author__ = 'tinglev@kth.se'

from threading import Thread, Event, current_thread

class SyncThread(Thread):

    def __init__(self, target):
        super(SyncThread, self).__init__(target=target, name='SyncThread')
        self._stop_event = Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

def thread_is_stoppped():
    if current_thread().name is 'SyncThread':
        this_thread = current_thread()
        return this_thread.stopped()
    return False
