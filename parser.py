'''
Handles converting token stream into abstract syntax tree
'''

from dataclasses import dataclass
from typing import TypeVar
from enum import Enum
import scanner as sc

T = TypeVar('T')

@dataclass
class Node: pass

@dataclass
class ErrorNode(Node):
    message: str

@dataclass
class FunctionNode(Node):
    ident: str
    func: 'function'
    arguments: list[Node]

@dataclass
class ValueNode(Node):
    value: T

@dataclass
class IdentNode(Node):
    name: str

# forward declaration
class ProgramNode(Node): pass
@dataclass
class ProgramNode(Node):
    left: Node
    right: ProgramNode | None = None

symbol_table = {
    'print': print,
    'neg': lambda a: -a,
    'add': lambda a, b: a + b,
    'sub': lambda a, b: a - b,
    'mul': lambda a, b: a * b,
    'div': lambda a, b: a / b,
}

def expression(scan: sc.Scanner) -> Node:
    '''
    Get an expression from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    if isinstance(scan.next, sc.LParenToken):
        next(scan, None) # this is the lparen
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Did not find identifier for function')
        elif ident.name not in symbol_table:
            return ErrorNode(f'Did not find identifier, {ident.name} in symbol table')
        arguments = []
        while not isinstance(scan.next, sc.RParenToken):
            expr = expression(scan)
            if isinstance(expr, ErrorNode):
                return expr
            arguments.append(expr)
        next(scan)
        return FunctionNode(ident.name, symbol_table[ident.name], arguments)
    elif isinstance(scan.next, sc.ValueToken):
        token = next(scan)
        return ValueNode(token.value)
    elif isinstance(scan.next, sc.IdentToken):
        token = next(scan)
        return IdentNode(token.name)
    else:
        return ErrorNode(f'Unexpected token {scan.next}')

def program(scan: sc.Scanner) -> Node:
    '''
    Get an program from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    node = ProgramNode(expression(scan))
    if isinstance(node.left, ErrorNode):
        return node.left
    elif not isinstance(scan.next, sc.EndToken):
        node.right = program(scan)
        if isinstance(node.right, ErrorNode):
            return node.right
    return node

def tree(string: str) -> Node:
    scan = iter(sc.Scanner(string))
    return program(scan)
