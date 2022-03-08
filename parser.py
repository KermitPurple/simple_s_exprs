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
    arguments: list[Node]

@dataclass
class ValueNode(Node):
    value: T

@dataclass
class _IdentNode(Node):
    name: str
class IdentNode(_IdentNode): pass

# forward declaration
class ProgramNode(Node): pass
@dataclass
class ProgramNode(Node):
    left: Node
    right: ProgramNode | None = None

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

def function(scan: sc.Scanner) -> Node:
    '''
    Get a function from the token stream
    :scan: iterator over token stream with 1 look ahead
    '''
    next(scan, None) # this is the lparen
    ident = next(scan, None)
    if not isinstance(ident, sc.IdentToken):
        return ErrorNode('Did not find identifier for function')
    elif ident.name in ('assign', '='):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to assign to')
        ret = AssignNode(ident.name, expression(scan))
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after assignment')
        next(scan)
        return ret
    elif ident.name in ('add_assign', '+='):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to assign to')
        ret = AddAssignNode(ident.name, expression(scan))
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after assignment')
        next(scan)
        return ret
    elif ident.name in ('sub_assign', '-='):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to assign to')
        ret = SubAssignNode(ident.name, expression(scan))
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after assignment')
        next(scan)
        return ret
    elif ident.name in ('mul_assign', '*='):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to assign to')
        ret = MulAssignNode(ident.name, expression(scan))
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after assignment')
        next(scan)
        return ret
    elif ident.name in ('div_assign', '/='):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to assign to')
        ret = DivAssignNode(ident.name, expression(scan))
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after assignment')
        next(scan)
        return ret
    elif ident.name in ('inc', '++'):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to increment')
        ret = IncrementNode(ident.name)
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after increment')
        next(scan)
        return ret
    elif ident.name in ('dec', '--'):
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode('Expected name of variable to decrement')
        ret = DecrementNode(ident.name)
        if not isinstance(scan.next, sc.RParenToken):
            return ErrorNode(f'Expected \')\' after decrement')
        next(scan)
        return ret
    arguments = []
    while not isinstance(scan.next, sc.RParenToken):
        expr = expression(scan)
        if isinstance(expr, ErrorNode):
            return expr
        arguments.append(expr)
    next(scan)
    print(ident.name, arguments)
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
