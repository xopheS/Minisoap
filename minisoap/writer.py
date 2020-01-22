from .listener import Listener
from .stream import Stream
import subprocess as sp
from pathlib import Path
import tempfile, time

## Stream writer
#
# Writes a stream on hard drive
class Writer(Listener): 
    def __init__(self, stream, filename):
        if not isinstance(stream, Stream): raise TypeError
        Listener.__init__(self)
        self.path = Path(filename).absolute()
        self.stream = stream
        
    ## @var path
    # Path for the file
    
    ## @var stream
    # Stream to write
    
    ## @var chunk
    # Chunk size
    
    ## @var samplerate
    # Sampling rate
    
    ## @var Channels
    # Number of channels
    

    ## Run function of the thread, writes the stream to path
    #
    def run(self):
        command = [ "ffmpeg",
                "-f", 
                "f32le", 
                "-acodec", 
                "pcm_f32le",
                "-ac", str(self.stream.channels), 
                "-ar", str(self.stream.samplerate),
                '-i', '-', # The imput comes from a pipe
                '-y', # (optional) overwrite output file if it exists,
                self.path ]
        pipe = sp.Popen( command, stdin=sp.PIPE, stderr=sp.PIPE, stdout=sp.PIPE)
        _pcmbuf = pipe.stdin
        for data in self.stream:
            if data is None: continue
            if self.killed():break
            _pcmbuf.write(data.tobytes())
            _pcmbuf.flush()
        self.kill()
