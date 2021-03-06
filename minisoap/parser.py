"""
Sequence = Expression|Name=Expression
N = [a-Z'_$][a-Z'_$0-9]*
Expression' = Expression' Expression | Expression
E = Name Expression' | '.*' | [0-9]+ | (Expression)
"""



class LineParsingError(Exception):
    pass
# Exception used to tell minisoap that we need more lines to parse the sequence
class ContinueParsing(Exception):
    def __init__(self, vn=None, pile = None, txt = None):
        Exception.__init__(self)
        self.vn = vn
        self.pile = pile
        self.txt = txt

## These are the classes used to construct the parsing tree
#
class Sequence:
    def __init__(self, a1, a2=None):
        self.type = 'assign' if a2!=None else 'call'
        self.variable_name = a1 if a2!= None else None
        self.expr = a2 if a2!=None else a1
    def __str__(self):
        return 'Sequence('+self.variable_name.__str__()+', '+self.expr.__str__()+')'

class Help(Sequence):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Help('+self.name+')'

class Expr:
    def __init__(self, val, *args):
        self.val = val
        self.args = args
    def __str__(self):
        s = ', '.join(map(lambda x: x.__str__(), self.args))
        return 'Expr('+self.val.__str__()+', '+s+')'
        
class String(Expr):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return 'String('+self.val+')'
        
class Transition(Expr):
    def __init__(self, table):
        self.table = table
    def __str__(self):
        return 'Transition('+"; ".join([str(t[0])+" ->> "+str(t[1]) for t in self.table])+')'

class Number(Expr):
    def __init__(self, val):
        self.val = float(val)
    def __str__(self):
        return 'Number('+str(self.val)+')'

class VariableName(Expr):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return 'VariableName('+self.val+')'

## The Parser class
#
class Parser:
    
    def __init__(self):
        self._w = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + ['\'', '_', "$"]
        self._n = [chr(i) for i in range(48, 58)]
        self._wn = self._w + self._n
        self._wh = [' ', '\t']

        ## @var _w
        # Contains all accepted caracters for variable naming except numbers
        ## @var _n
        # Contains numbers
        ## @var _wn
        # Contains all accepted caracters for variable naming
        ## @var _wh
        # Contains caraters considered as whitespace
        
        
    # Parses a line 
    # It checks if the line is looking like these three possible types:
    #  - vn = expr
    #  - expr
    #  - vn ?
    # Or continues parsing expression if it is needed
    def parse_line(self, line, continueparsing=None):
        if continueparsing!=None:
            vn = continueparsing.vn 
            if vn==None:
                e = self.parse_expr(line, continueparsing)
                return Sequence(e) if e != None else None 
            else:
                return Sequence(vn,self.parse_expr(line, continueparsing))
        l = line[:(line.index('//'))] if '//' in line else line
        cur = 0
        while cur < len(l) and l[cur] in self._wh:
            cur+=1
        if cur >= len(l):
            return None
        if l[cur] in self._w:
            name = ''
            while cur < len(l)-1 and l[cur] in self._wn:
                name += l[cur]
                cur+=1
            while cur < len(l)-1 and l[cur] in self._wh:
                cur+=1
            if l[cur] == "=":
                try:
                    return Sequence(VariableName(name), self.parse_expr(l[cur+1:]))
                except ContinueParsing as cp:
                    cp.vn = VariableName(name)
                    raise cp
            elif l[cur] == "?":
                for i in l[cur+1:]:
                    if not i in self._wh:
                        break
                else:
                    return Help(name)
        e = self.parse_expr(l)
        return Sequence(e) if e != None else None
    
    ## Parses an expression
    # It launches sequentially the methods beginning with __
    # And save the result of the first one whitch does not return None
    # on a stack and updates cursor position
    def parse_expr(self, t, continueparsing=None):
        cur = 0
        funcs = [getattr(self, f) for f in dir(Parser) if f.startswith("_"+self.__class__.__name__)]
        pile = []
        try:
            if continueparsing != None:
                pile = continueparsing.pile
                ep, cur = self.__get_brackets(t, cur, continueparsing)
                pile.append(ep)
            while cur < len(t):
                cur = self._skip_white_space(t, cur)
                for f in funcs:
                    e = f (t, cur)
                    if e != None:
                        ep, cur = e
                        pile.append(ep)
                        break
                else:
                    raise LineParsingError('Unexpected character: '+t[cur-1:cur+1], cur)
                cur = self._skip_white_space(t, cur)
        except ContinueParsing as cp:
            cp.pile = pile
            raise cp
        if len(pile) > 1 and not isinstance(pile[0], VariableName):
            raise LineParsingError('Calling a non callable')
        if len(pile) < 1:
            return None
        if len(pile) == 1:
            return pile[0]
        return Expr(pile[0], *pile[1:])
    
    # Parses a transition (the text between two brackets)
    def parse_transition(self, txt):
        try:
            table = []
            for l in txt.split(";"):
                if l.replace(' ', '').replace('\t', '') == "": continue
                [time, amplitude] = [i.replace(' ', '').replace('\t', '') for i in l.split(':')]
                if time[-2:] == "ms": table.append((float(time[:-2])/1000, float(amplitude)))
                else: table.append((float(time[:-1]), float(amplitude)))
            return Transition(table)
        except:
            raise LineParsingError("Syntax error in transition definition")

    # Skips white space
    def _skip_white_space(self, t, i):
        cur = i
        while cur < len(t) and t[cur] in self._wh :
            cur+=1
        return cur
    
    # Parses a string and returns the new cursor position
    def __get_string(self, t, i):
        cur = i
        if t[cur] != '"' : return None
        s = ''
        while t[cur+1] != '"':
            cur+=1
            s+=t[cur]
        cur+=2
        if cur < len(t) and not t[cur] in self._wh : raise LineParsingError('Expected whitespace after string', cur)
        return String(s),cur
    
    # Parses a variable name and returns the new cursor position
    def __get_variable_name(self, t, i):
        cur = i
        if not t[cur] in self._w : return None
        vn = t[cur]
        while cur < len(t)-1 and t[cur+1] in self._wn :
            cur+=1
            vn+=t[cur]
        cur+=1
        if cur < len(t) and not t[cur] in self._wh : raise LineParsingError('Expected whitespace after variable name', cur)
        return VariableName(vn),cur
    
    # Parses a parenthesis and returns the new cursor position
    def __get_parenthesis(self, t, i):
        cur = i
        if t[cur] != '(': return None
        _t = ''
        d = cur+1
        p = 0
        try:
            while t[cur+1] != ')' or p:
                if t[cur+1] == '(': p+=1
                if t[cur+1] == ')': p-=1
                if p < 0: raise LineParsingError('Unexpected parenthesis', cur)
                cur+=1
                _t+=t[cur]
        except IndexError:
            raise LineParsingError('Parenthesis not closed', cur)
        cur+=2
        return self.parse_expr(t[d:cur-1]),cur
    
    # Parses a parenthesis and returns the new cursor position
    # or raises ContinueParsing exception if more lines are needed 
    def __get_brackets(self, t, i, continueparsing=None):
        brkts='' if continueparsing==None else continueparsing.txt+' '
        cur = i
        if continueparsing == None:
            if t[cur] != '{': return None
            else:cur+=1
        try:
            while t[cur] != '}':
                brkts+=t[cur]
                cur+=1
        except IndexError:
            if continueparsing == None: raise ContinueParsing(txt=brkts)
            else:
                continueparsing.txt = brkts
                raise continueparsing
        cur+=1
        return self.parse_transition(brkts),cur
    
    # Parses a number and returns the new cursor position
    def __get_number(self, t, i):
        cur = i
        comma = False
        if not t[cur] in self._n and not t[cur] == '.': return None
        a = t[cur]
        while cur < len(t)-1 and (t[cur+1] in self._n or t[cur+1] == '.'):
            if t[cur+1] == '.':
                if comma: 
                    raise LineParsingError("Not a number", cur)
                else:
                    comma = True
            cur+=1
            a+=t[cur]
        cur+=1
        if cur < len(t) and not t[cur] in self._wh : raise LineParsingError('Expected whitespace after number', cur)
        return Number(float(a)), cur

