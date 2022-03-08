'''
Evaluate and execute an abstract syntax program
'''

from scanner import ScannerException
from parser import ParserException
import parser as ps
from symbol_table import symbol_table

class InterpretException(Exception): pass

def interpret(string: str) -> any:
    '''
    interpret and execute a string
    '''
    try:
        return eval_tree(ps.program(string))
    except (ScannerException, ParserException, InterpretException) as e:
        print(e)

def eval_tree(node: ps.Node) -> any:
    '''
    interpret and execute a program
    '''
    match node:
        case ps.ExpressionsNode(left, right):
            ret = eval_tree(left)
            if right is not None:
                ret = eval_tree(right)
            return ret
        case ps.ValueNode(value=value):
            return value
        case ps.FunctionNode(name, args):
            func = symbol_table.get(name, None)
            if func is None:
                raise InterpretException(f'{name} is undefined')
            try:
                return func(*map(eval_tree, args))
            except TypeError as t:
                raise InterpretException(str(t))
        case ps.AssignNode(name, value):
            symbol_table[name] = eval_tree(value)
            return symbol_table[name]
        case ps.AddAssignNode(name, value):
            symbol_table[name] += eval_tree(value)
            return symbol_table[name]
        case ps.SubAssignNode(name, value):
            symbol_table[name] -= eval_tree(value)
            return symbol_table[name]
        case ps.MulAssignNode(name, value):
            symbol_table[name] *= eval_tree(value)
            return symbol_table[name]
        case ps.DivAssignNode(name, value):
            symbol_table[name] /= eval_tree(value)
            return symbol_table[name]
        case ps.IncrementNode(name):
            symbol_table[name] += 1
            return symbol_table[name]
        case ps.DecrementNode(name):
            symbol_table[name] -= 1
            return symbol_table[name]
        case ps.IdentNode(name):
            return symbol_table.get(name, None)
