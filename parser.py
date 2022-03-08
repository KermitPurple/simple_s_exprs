'''
Handles converting token stream into abstract syntax tree
'''

from dataclasses import dataclass
from typing import TypeVar
from enum import Enum
import scanner as sc

T = TypeVar('T')

class ParserException(Exception): pass

@dataclass
class Node: pass

@dataclass
class FunctionNode(Node):
    ident: str
    arguments: list[Node]

@dataclass
class ValueNode(Node):
    value: T

@dataclass
class _IdentNode(Node):
    name: str
class IdentNode(_IdentNode): pass

# forward declaration
class ExpressionsNode(Node): pass
@dataclass
class ExpressionsNode(Node):
    left: Node
    right: ExpressionsNode | None = None

@dataclass
class _AssignNode(Node):
    name: str
    value: Node
class AssignNode(_AssignNode): pass
class AddAssignNode(_AssignNode): pass
class SubAssignNode(_AssignNode): pass
class MulAssignNode(_AssignNode): pass
class DivAssignNode(_AssignNode): pass
class IncrementNode(_IdentNode): pass
class DecrementNode(_IdentNode): pass

def token(scan: sc.Scanner, tok) -> sc.Token:
    '''
    Get a specified token from the token stream
    fail if expected token is not there
    :scan: iterator over token stream with 1 look ahead
    :tok: the token to expect
    '''
    if isinstance(scan.next, tok):
        return next(scan)
    raise ParserException(f'Expected {tok.__name__} but found {scan.next}')

def partial_assign(scan: sc.Scanner, assign_class) -> Node:
    '''
    Get the rest of an assign statement e.g. "x 10)"
    :scan: iterator over token stream with 1 look ahead
    :assign_class: assign subclass used to construct node
    '''
    ident = token(scan, sc.IdentToken)
    ret = assign_class(ident.name, expression(scan))
    token(scan, sc.RParenToken)
    return ret

def partial_increment(scan: sc.Scanner, increment_class) -> Node:
    '''
    get the rest of an increment statement e.g. "x)"
    :scan: iterator over token stream with 1 look ahead
    :increment_class: increment subclass used to construct node
    '''
    ident = token(scan, sc.IdentToken)
    ret = increment_class(ident.name)
    token(scan, sc.RParenToken)
    return ret

def function(scan: sc.Scanner) -> Node:
    '''
    Get a function from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    token(scan, sc.LParenToken)
    ident = token(scan, sc.IdentToken)
    if ident.name in ('assign', '='):
        return partial_assign(scan, AssignNode)
    elif ident.name in ('add_assign', '+='):
        return partial_assign(scan, AddAssignNode)
    elif ident.name in ('sub_assign', '-='):
        return partial_assign(scan, SubAssignNode)
    elif ident.name in ('mul_assign', '*='):
        return partial_assign(scan, MulAssignNode)
    elif ident.name in ('div_assign', '/='):
        return partial_assign(scan, DivAssignNode)
    elif ident.name in ('inc', '++'):
        return partial_increment(scan, IncrementNode)
    elif ident.name in ('dec', '--'):
        return partial_increment(scan, DecrementNode)
    arguments = []
    while not isinstance(scan.next, sc.RParenToken):
        expr = expression(scan)
        if isinstance(expr, ParserException):
            return expr
        arguments.append(expr)
    next(scan) # RParen
    return FunctionNode(ident.name, arguments)

def expression(scan: sc.Scanner) -> Node:
    '''
    Get an expression from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    if isinstance(scan.next, sc.LParenToken):
        return function(scan)
    elif isinstance(scan.next, sc.ValueToken):
        token = next(scan)
        return ValueNode(token.value)
    elif isinstance(scan.next, sc.IdentToken):
        token = next(scan)
        return IdentNode(token.name)
    else:
        raise ParserException(f'Unexpected token {scan.next}')

def expressions(scan: sc.Scanner) -> Node:
    '''
    Get an expressions from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    node = ExpressionsNode(expression(scan))
    if isinstance(node.left, ParserException):
        return node.left
    elif not isinstance(scan.next, sc.EndToken | sc.RParenToken):
        node.right = expressions(scan)
        if isinstance(node.right, ParserException):
            return node.right
    return node

def program(string: str) -> Node:
    scan = iter(sc.Scanner(string))
    node = expressions(scan)
    token(scan, sc.EndToken)
    return node
