from .parser import Sequence, Help, Expr, String, Number, VariableName, Transition
from .transition import Transition as Tr
from .builtins import Builtins
class InterpreterError(Exception):
    pass

class Interpreter:
    
    def __init__(self):
        self.builtins = Builtins()
        self.builtins_names = [f for f in dir(Builtins) if callable(getattr(Builtins, f)) and not f.startswith("__")]
        self.variables = {}

    ## @var builtins
    # Builtins of the Minisoap
    
    ## @var builtins_names
    # Names of Minisoap builtins
    
    ## @var variables
    # User variables definitions
    
    
    ## Applies a sequence of instructions
    #
    # @param seq The sequence
    def run(self, seq):
        if seq == None: return
        if isinstance(seq, Help):
            try:
                s = getattr(Builtins, seq.name).__doc__[2:]
                return '\n'.join([line.strip() for line in s.split('\n')])
            except AttributeError:
                raise InterpreterError('Unknown function')
        elif seq.type == 'assign':
            if seq.variable_name.val in self.builtins_names: raise InterpreterError('Variable name not allowed')
            if seq.variable_name.val in self.variables: raise InterpreterError('Variable already defined')
            self.variables[seq.variable_name.val] = self.run_expr(seq.expr)
            return 'Variable ' + seq.variable_name.val + ' defined'
        else:
            return self.run_expr(seq.expr).__str__()
    
    
    ## Runs an expression
    #
    # @param expr The expression
    def run_expr(self, expr):
        if isinstance(expr, String) or isinstance(expr, Number):
            return expr.val
        elif isinstance(expr, Transition):
            return Tr(expr.table)
        elif isinstance(expr, VariableName):
            if not expr.val in self.variables: raise InterpreterError('Use of undefined variable: '+expr.val)
            return self.variables[expr.val]
        elif isinstance(expr, Expr):
            if not isinstance(expr.val, VariableName): raise InterpreterError('Cannot call a non callable')
            if not expr.val.val in self.builtins_names: raise InterpreterError('Unknown callable')
            return getattr(Builtins, expr.val.val)(self.builtins, *map(self.run_expr, filter(lambda x:x!=None, expr.args)))
        else: pass

