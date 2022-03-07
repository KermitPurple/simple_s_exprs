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
class BinaryOp(Node):
    left: Node
    right: Node

class Add(BinaryOp): pass
class Sub(BinaryOp): pass
class Mul(BinaryOp): pass
class Div(BinaryOp): pass

@dataclass
class UnaryOp(Node):
    child: Node

class Neg(UnaryOp): pass

@dataclass
class ValueNode(Node):
    type: sc.ValueType
    value: T

@dataclass
class IdentNode(Node):
    name: str

def expression(scan: sc.Scanner) -> Node:
    if isinstance(scan.next, sc.LParenToken):
        next(scan, None) # this is the lparen
        ident = next(scan, None)
        if not isinstance(ident, sc.IdentToken):
            return ErrorNode(f'Did not find identifier for function')
    elif isinstance(scan.next, sc.ValueType):
        token = next(scan)
        return ValueNode(token.type, token.value)
    elif isinstance(scan.next, sc.IdentToken):
        token = next(scan)
        return IdentNode(token.name)
    else:

