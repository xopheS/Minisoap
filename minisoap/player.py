from .listener import Listener
from .stream import Stream
import soundcard as sc
import time
from .microphone import Microphone

## Player class
#
# A stream player
class Player(Listener):
    def __init__(self, stream):
        if not isinstance(stream, Stream): raise TypeError
        Listener.__init__(self)
        self.stream = stream
        self.is_mic = isinstance(self.stream, Microphone)
        self._play = True
        self.sp = sc.default_speaker()
        self._stop = False
            
    ## @var stream
    # Stream to be played
    
    ## @var _play
    # Boolean indicating if playing
    
    ## @var sp
    # Spreakers (default value of soundcard library)
    
    ## @var stop
    # Boolean indicating if the player is stopped
    
    ## Run the player
    #
    def run(self):
        with self.sp.player(samplerate=self.stream.samplerate,
            channels=self.stream.channels) as sp:
            
            for block in self.stream:
                if block is None: continue # End of track
                while not self._play:
                    self._listening = False
                    if self.killed():return
                    time.sleep(0.1)
                self._listening = True
                if self.killed(): self._listening = False;break
                sp.play(block)
        self._listening = False

    ## Pause the player
    #
    def pause(self):
        self._play = False
    
    ## Play the player
    #
    def play(self):
        self._play = True
