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

def partial_assign(scan: sc.Scanner, assign_class) -> Node:
    ident = next(scan, None)
    if not isinstance(ident, sc.IdentToken):
        raise ParserException('Expected name of variable to assign to')
    ret = assign_class(ident.name, expression(scan))
    if not isinstance(scan.next, sc.RParenToken):
        raise ParserException(f'Expected \')\' after assignment')
    next(scan)
    return ret

def partial_increment(scan: sc.Scanner, increment_class) -> Node:
    ident = next(scan, None)
    if not isinstance(ident, sc.IdentToken):
        raise ParserException('Expected name of variable')
    ret = increment_class(ident.name)
    if not isinstance(scan.next, sc.RParenToken):
        raise ParserException(f'Expected \')\'')
    next(scan)
    return ret

def function(scan: sc.Scanner) -> Node:
    '''
    Get a function from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    next(scan, None) # this is the lparen
    ident = next(scan, None)
    if not isinstance(ident, sc.IdentToken):
        raise ParserException('Did not find identifier for function')
    elif ident.name in ('assign', '='):
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
    next(scan)
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
    if not isinstance(scan.next, sc.EndToken):
        raise ParserException(f'Unexpected token {scan.next}')
    return node
