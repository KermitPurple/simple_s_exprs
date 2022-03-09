'''
Evaluate and execute an abstract syntax program
'''

from preprocess import PreprocesserException
from scanner import ScannerException
from parser import ParserException
from copy import deepcopy
import parser as ps
from symbol_table import new_symbol_table, copy_table
class InterpretException(Exception): pass

def interpret(string: str) -> any:
    '''
    interpret and execute a string
    :string: str to execute
    '''
    try:
        return eval_tree(ps.program(string), new_symbol_table())
    except (ScannerException, ParserException, InterpretException, PreprocesserException) as e:
        print(e)

def eval_tree(node: ps.Node, symbol_table: dict[str, any]) -> any:
    '''
    interpret and execute a program
    :node: tree to execute
    '''
    match node:
        case ps.ExpressionsNode(left, right):
            ret = eval_tree(left, symbol_table)
            if right is not None:
                ret = eval_tree(right, symbol_table)
            return ret
        case ps.ValueNode(value=value):
            return value
        case ps.FunctionNode(name, args):
            check_symbol(name, symbol_table)
            func = symbol_table[name]
            try:
                return func(*map(lambda x: eval_tree(x, symbol_table), args))
            except TypeError as t:
                raise InterpretException(str(t))
        case ps.AssignNode(name, value):
            symbol_table[name] = eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.AddAssignNode(name, value):
            check_symbol(name, symbol_table)
            symbol_table[name] += eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.SubAssignNode(name, value):
            check_symbol(name, symbol_table)
            symbol_table[name] -= eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.MulAssignNode(name, value):
            check_symbol(name, symbol_table)
            symbol_table[name] *= eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.DivAssignNode(name, value):
            check_symbol(name, symbol_table)
            symbol_table[name] /= eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.ModAssignNode(name, value):
            check_symbol(name, symbol_table)
            symbol_table[name] %= eval_tree(value, symbol_table)
            return symbol_table[name]
        case ps.IncrementNode(name):
            check_symbol(name, symbol_table)
            symbol_table[name] += 1
            return symbol_table[name]
        case ps.DecrementNode(name):
            check_symbol(name, symbol_table)
            symbol_table[name] -= 1
            return symbol_table[name]
        case ps.IdentNode(name):
            check_symbol(name, symbol_table)
            return symbol_table[name]
        case ps.IfNode(cond, block, else_block):
            if eval_tree(cond, symbol_table):
                return eval_tree(block, symbol_table)
            elif else_block is not None:
                return eval_tree(else_block, symbol_table)
        case ps.DefNode(name, names, body) as n:
            def new_function(*args):
                nonlocal symbol_table
                old_scope = deepcopy(symbol_table)
                for name, value in zip(names, args):
                    symbol_table[name] = value
                result = eval_tree(body, symbol_table)
                copy_table(old_scope, symbol_table)
                return result
            new_function.__name__ = name
            symbol_table[name] = new_function
            return symbol_table[name]

def check_symbol(name: str, symbol_table: dict[str, any]):
    if name not in symbol_table:
        raise InterpretException(f'{name} not in symbol table')
