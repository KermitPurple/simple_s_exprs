'''
Evaluate and execute an abstract syntax tree
'''

import parser as ps

def interpret(string: str):
    '''
    interpret and execute a string
    '''
    eval_tree(ps.tree(string))

def eval_tree(node: ps.Node) -> int | None:
    '''
    interpret and execute a tree
    '''
    match node:
        case ps.ProgramNode(left, right):
            ret = eval_tree(left)
            if node is not None:
                ret = eval_tree(right)
            return ret
        case ps.ValueNode(value=value):
            return value
        case ps.FunctionNode(func=func, arguments=args):
            try:
                return func(*map(eval_tree, args))
            except TypeError as t:
        case ps.IdentNode(name):
            return ps.symbol_table.get(name, None)
