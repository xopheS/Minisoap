# pylint: disable=F0401
from colorama import init, Cursor, Fore, Back, Style
import os, sys

## Get character from stdin
#
def getch():
    if os.name == 'nt':
        import msvcrt
        return ord(msvcrt.getch()) 
    else:
        s = str.encode(sys.stdin.read(1))
        return ord(s) if len(s) > 0 else None

## Detect Kb hit (return boolean)
#
def kbhit():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.kbhit()
    else:
        from select import select
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []

## Console
#
# This object is the console of the Minisoap that will take user's instructions
class Console:
    
    def __init__(self):
        init()
        self.cursor_pos = 0
        self.line = ''
        self.hist_up = []
        self.hist_down = []
        
    ## @var cursor_pos
    # Position of the cursor
    
    ## @var line
    # Current line
    
    ## @var hist_op
    # History of previous op
    
    ## @var hist_down
    # History of next op
    
    ## Prints in stdout
    #
    # @param *args arguments to print
    def log(self, *args, end='\n', prefix='', join=' '):
        """
        Equivalent to sys.stdout.write
        """
        if len(args) > 0:
            for i in range(len(args)):
                arg = args[i].__str__()
                if i > 0 : sys.stdout.write(join)
                sys.stdout.write(prefix+arg.replace('\n', '\n'+prefix))
            sys.stdout.write(end)
            sys.stdout.flush()

    ## Prints an info (in blue)
    #
    # @param *args arguments to print
    def info(self, *args, **kw):
        """
        Prints infos
        """
        self.log(*args, **kw, prefix=Back.BLUE + Fore.WHITE + 'INFO:' + Back.RESET + Fore.RESET + ' ')

    ## Prints warning (in yellow)
    #
    # @param *args arguments to print
    def warn(self, *args, **kw):
        """
        Prints warnings
        """
        self.log(*args, **kw, prefix=Back.YELLOW + Fore.BLACK + 'WARNING:' + Back.RESET + Fore.RESET + ' ')

    ## Prints an error (in red)
    #
    # @param *args arguments to print
    def error(self, *args, **kw):
        """
        Prints errors
        """
        self.log(*args, **kw, prefix=Back.RED + Fore.WHITE + 'ERROR:' + Back.RESET + Fore.RESET + ' ')
    
    ## Input function, listens to user's input
    #
    def input(self):
        """
        Non blocking input listener
        """
        ret = [ord(b'\r')] if os.name == "nt" else [10,13]
        backspace = [ord(b'\x08')] if os.name == "nt" else [127]
        mod = [0,ord(b'\xe0')] if os.name == "nt" else [27]
        puts = lambda x : self.log(x, end='')
        
        
        def backspace_f(n=1):
            puts(Cursor.BACK(n)+self.line[self.cursor_pos:]+' '*n+Cursor.BACK(len(self.line)-self.cursor_pos+n))
            self.line = self.line[:self.cursor_pos-1] + self.line[self.cursor_pos:]
            self.cursor_pos-=n
            if self.cursor_pos < 0: self.cursor_pos = 0
        if kbhit():
            c = getch()
            if c == None: return
            if c in ret : 
                self.hist_up.append(self.line)
                self.line = ''
                self.cursor_pos = 0
                puts('\n')
                return self.hist_up[-1]
            elif c in backspace:
                backspace_f()
            elif c in mod:
                if not os.name == 'nt': getch()
                c = getch()
                K = ord(b'K') if os.name == 'nt' else 68
                M = ord(b'M') if os.name == 'nt' else 67
                H = ord(b'H') if os.name == 'nt' else 65
                P = ord(b'P') if os.name == 'nt' else 66
                S = ord(b'S') if os.name == 'nt' else 51
                if c == K and self.cursor_pos > 0: # left arrow
                    self.cursor_pos-=1
                    puts(Cursor.BACK())

                elif c == M and self.cursor_pos < len(self.line): # right arrow
                    self.cursor_pos+=1
                    puts(Cursor.FORWARD())

                elif c == H and len(self.hist_up) > 0: # up arrow
                    puts(Cursor.BACK(len(self.line[:self.cursor_pos]))+' '*len(self.line)+Cursor.BACK(len(self.line)))
                    self.hist_down.append(self.line)
                    self.line = self.hist_up.pop()
                    self.log(self.line, end='')
                    self.cursor_pos=len(self.line)

                elif c == P and len(self.hist_down) > 0: # down arrow
                    puts(Cursor.BACK(len(self.line[:self.cursor_pos]))+' '*len(self.line)+Cursor.BACK(len(self.line)))
                    self.hist_up.append(self.line)
                    self.line = self.hist_down.pop()
                    self.log(self.line, end='')
                    self.cursor_pos=len(self.line)

                elif c == S and self.cursor_pos < len(self.line): #suppr
                    if os.name != 'nt': getch()
                    self.cursor_pos+=1
                    puts(Cursor.FORWARD())
                    backspace_f()
            else:
                c = chr(c)
                self.line = self.line[:self.cursor_pos] + c + self.line[self.cursor_pos:]
                puts(self.line[self.cursor_pos:] + Cursor.BACK(len(self.line[self.cursor_pos:]))+Cursor.FORWARD())
                self.cursor_pos+=1
        return None


        
    
