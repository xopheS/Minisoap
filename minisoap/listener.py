from threading import Thread, Event

## Listener class
#
# A killable thread
class Listener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self._kill = Event()
        self._listening = False

    def __str__(self):
        return 'Listener: '+self.__class__.__name__ + (' listening...' if self._listening else '')
    ## Kill the Thread
    #
    def kill(self):
        self._kill.set()
    def killed(self):
        return self._kill.isSet()
