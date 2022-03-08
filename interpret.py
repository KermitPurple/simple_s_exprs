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
    :string: str to execute
    '''
    try:
        return eval_tree(ps.program(string))
    except (ScannerException, ParserException, InterpretException) as e:
        print(e)

def eval_tree(node: ps.Node) -> any:
    '''
    interpret and execute a program
    :node: tree to execute
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
            check_symbol(name)
            func = symbol_table[name]
            try:
                return func(*map(eval_tree, args))
            except TypeError as t:
                raise InterpretException(str(t))
        case ps.AssignNode(name, value):
            symbol_table[name] = eval_tree(value)
            return symbol_table[name]
        case ps.AddAssignNode(name, value):
            check_symbol(name)
            symbol_table[name] += eval_tree(value)
            return symbol_table[name]
        case ps.SubAssignNode(name, value):
            check_symbol(name)
            symbol_table[name] -= eval_tree(value)
            return symbol_table[name]
        case ps.MulAssignNode(name, value):
            check_symbol(name)
            symbol_table[name] *= eval_tree(value)
            return symbol_table[name]
        case ps.DivAssignNode(name, value):
            check_symbol(name)
            symbol_table[name] /= eval_tree(value)
            return symbol_table[name]
        case ps.IncrementNode(name):
            check_symbol(name)
            symbol_table[name] += 1
            return symbol_table[name]
        case ps.DecrementNode(name):
            check_symbol(name)
            symbol_table[name] -= 1
            return symbol_table[name]
        case ps.IdentNode(name):
            check_symbol(name)
            return symbol_table[name]
        case ps.IfNode(cond, block, else_block):
            if eval_tree(cond):
                return eval_tree(block)
            elif else_block is not None:
                return eval_tree(else_block)

def check_symbol(name: str):
    if name not in symbol_table:
        raise InterpretException(f'{name} not in symbol table')
