from datetime import datetime, timedelta

## Clock class
#
# Clock used for timeouts in executions
class Clock:
    
    def __init__(self):
        self.exs = []
    
    ## @var exs
    # List of clock's stored executions
    
    ## Run and execute instructions
    #
    def step(self):
        t = datetime.now()
        l = []
        while len(self.exs):
            d, f = self.exs.pop()
            if d <= t: f()
            else: l.append((d, f))
        self.exs = l
        
    ## Add execution to clock
    #
    # @param f The function to execute
    # @param d Timeout in milliseconds 
    def wait(self, f, d=0): # d duration in ms
        self.exs.append((datetime.now()+timedelta(milliseconds=d), f))

