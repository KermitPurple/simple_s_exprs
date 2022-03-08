'''
Evaluate and execute an abstract syntax tree
'''

import parser as ps

def interpret(string: str) -> any:
    '''
    interpret and execute a string
    '''
    return eval_tree(ps.tree(string))

def eval_tree(node: ps.Node) -> any:
    '''
    interpret and execute a tree
    '''
    match node:
        case ps.ProgramNode(left, right):
            ret = eval_tree(left)
            if right is not None:
                ret = eval_tree(right)
            return ret
        case ps.ValueNode(value=value):
            return value
        case ps.FunctionNode(name, func, args):
            try:
                return func(*map(eval_tree, args))
            except TypeError as t:
                print(f'{name!r} got the incorrect number of arguments: \n\t{t}')
        case ps.IdentNode(name):
            return ps.symbol_table.get(name, None)
