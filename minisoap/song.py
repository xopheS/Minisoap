from .stream import Stream
from pathlib import Path
import  numpy, subprocess


## @var extensions
# Available songs extensions
extensions = ["wav", "mp3", "flac", "aac", "m4a", "ogg"]

## Song class
#
# Wrapper of a Song
class Song(Stream):
    
    def __init__(self, filename):
        self.path = Path(filename).absolute()
        Stream.__init__(self)
        if not self.path.suffix[1:] in extensions : raise Exception("Extension not supported")
        if not self.path.exists(): raise Exception("File not found")
        p = subprocess.Popen(["ffmpeg", "-i", self.path],
            stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        info = p.stderr.read().decode("utf-8") 
        duration = info[info.index('Duration')+10:]
        duration = duration[:duration.index(',')].split(':')
        self.duration = float(duration[-1]) + 60*float(duration[-2]) + 24*60*float(duration[-3])

    ## @var path
    # Path of the song
    
    ## Print the song
    #
    def __str__(self):
        return 'Song('+self.path.__str__()+')'
    
    ## Iterates over the song
    #
    def __iter__(self):
        self._t = 0.0
        p = subprocess.Popen(["ffmpeg", "-i", self.path, "-f", "f32le", "-acodec", "pcm_f32le",
                    "-ac", str(self.channels), "-ar", str(self.samplerate), "-"],
                    stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self._pcmbuf = p.stdout
        return self
    
    ## Read next chunk
    #
    def __next__(self):
        a = self._pcmbuf.read(self.chunk*4*self.channels)
        if not len(a): raise StopIteration
        self.update_t()
        return numpy.frombuffer(a, dtype=numpy.float32).reshape((-1,self.channels))
        


