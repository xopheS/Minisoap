from .stream import Stream
import soundcard as sc
import numpy as np

## Microphone Stream
#
# This object represents the Microphone as a Stream
class Microphone(Stream):
    
    def __init__(self, mic=None):
        if mic == None:
            try: 
                mic = sc.default_microphone()
            except:
                raise Exception("No microphones avalaible")
        Stream.__init__(self)
        if not mic.record : raise Exception("Not a microphone")
        self._mic = mic
    
    ## @var _mic
    # Default microphone from soundcard library
    
    ## Start recording
    #
    def _gen(self):
        with self._mic.recorder(self.samplerate, self.channels) as rec:
            while True:
                yield rec.record(self.chunk)
    
    ## Iterate over the stream
    #
    def __iter__(self):
        self.__gen = self._gen()
        return self
    
    ## String representation of microphone
    #
    def __str__(self):
        return 'Microphone('+self._mic.__str__()+')'
    
    ## Next function of the iterator 
    #
    def __next__(self):
        return next(self.__gen)
        


