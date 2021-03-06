from .stream import Stream
import numpy as np

## Returns a convexe combination of two numpy vectors
#
# @param p1 First vector
# @param p2 Second vector
# @param t Scalar value
def bar(p1, p2, t):
    return t*p1+(1-t)*p2


## Transition class
#
# Realize transition between two streams
class Transition:
    def __init__(self, table=[]):
        self.duration = 0 if table == [] else max([i[0] for i in table])
        self._table = sorted(table)
    
    ## @var duration
    # Duration of the transition
    
    ## @var _table
    # table of (time, amplitude) elements
    
    ## Makes the transition between of samples in _table
    #
    # @param t Time of transition
    def amplitude(self, t):
        """
        Linear approximation of the transition table
        Returns amplitude of the stream which is ending
        t in s
        """
        try:
            i = len(self._table)-1
            while self._table[i][0] > t: i-=1
            t1,a1=self._table[i]
            t2,a2=self._table[i+1]
            return (a2-a1)/(t2-t1)*(t-t1)+a1         
        except:
            return 0
    
    ## String representation of transition objects
    #
    def __str__(self):
        return 'Transition(\n.     '+"\n.     ".join([str(t[0])+"s ->> "+str(t[1]) for t in self._table])+'\n)'
