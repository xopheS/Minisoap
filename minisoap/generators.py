from .stream import Stream
import numpy as np

## Generator class
#
# Generates synthetical waves
class Generator(Stream):
    
    def __init__(self, duration=float('inf')):
        Stream.__init__(self)
        self.duration = duration if duration != None else float('inf')

    
    ## @var duration
    # The duration of the wave
    
    
    ## Generates an empty wave
    #
    # @param The size of the wave
    def _gen(self, size):
        return np.zeros((size, self.channels))
    
    
    ## Iterate over the wave
    #
    def __iter__(self):
        self._t = 0.0
        return self
    
    ## Extract the next chunk
    #
    def __next__(self):
        
        if self.duration < float('inf'):
            if self._t > self.duration: raise StopIteration
            a = int((self.duration-self._t)*self.samplerate)
            if a == 0: raise StopIteration
            if a < self.chunk:
                self.update_t(a)
                return self._gen(a)
        self.update_t()
        return self._gen(self.chunk)

## Silent stream generator
#
# Generate a silent stream
class Silence(Generator):
    pass

## Constant stream generator
#
# Generate a silent stream
class Constant(Generator):
    def __init__(self, constant=1, duration=float('inf')):
        super(Constant, self).__init__(duration)
        self._c = constant
    def _gen(self, size):
        return self._c*np.exp(np.zeros((size, self.channels)))

## Sine wave generator
#
# Generate a sine wave
class Sine(Generator):
    def __init__(self, freq=440, amplitude=1, duration=None):
        self._freq = freq
        self._amplitude = amplitude
        self._i = 0
        Generator.__init__(self, duration)
    
    ## @var _freq
    # The frequency of the sine wave
    
    ## @var _amplitude
    # The amplitude of the sine wave
    
    ## Sine wave generator
    #
    # @param The size of the wave
    def _gen(self, size):
        dt = float(self.chunk)/self.samplerate
        t = np.array([[i*dt]*self.channels for i in range(self._i,self._i+size)])
        self._i+=size
        return np.sin(2*np.pi*t*self._freq) * self._amplitude
        





