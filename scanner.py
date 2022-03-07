'''
Handles scanning the character stream and converting it into a character stream
'''

from dataclasses import dataclass
from typing import TypeVar
from enum import Enum

T = TypeVar('T')

class ScanningState(Enum):
    GENERAL = 0
    IDENT = 1
    INT = 2

class ValueType(Enum):
    INT = 0

@dataclass
class Token: pass
class EndToken(Token): pass
class LParenToken(Token): pass
class RParenToken(Token): pass

@dataclass
class ErrorToken(Token):
    message: str

@dataclass
class IdentToken(Token):
    name: str

@dataclass
class ValueToken(Token):
    type: ValueType
    value: T

def scanner_gen(string: str):
    string += ' '
    state = ScanningState.GENERAL
    partial = ''
    for ch in string:
        match state:
            case ScanningState.GENERAL:
                if ch.isspace():
                    continue
                elif ch.isnumeric():
                    partial += ch
                    state = ScanningState.INT
                elif ch == ')':
                    yield RParenToken()
                elif ch == '(':
                    yield LParenToken()
                else:
                    partial += ch
                    state = ScanningState.IDENT
            case ScanningState.IDENT:
                if ch.isspace() or ch in '()':
                    yield IdentToken(partial)
                    state = ScanningState.GENERAL
                    partial = ''
                else:
                    partial += ch
            case ScanningState.INT:
                paren = ch in '()'
                if ch.isspace() or paren:
                    yield ValueToken(ValueType.INT, int(partial))
                    if ch == ')':
                        yield RParenToken()
                    elif ch == '(':
                        yield LParenToken()
                    state = ScanningState.GENERAL
                    partial = ''
                elif ch.isnumeric():
                    partial += ch
                else:
                    yield ErrorToken(f'Unexpected character inside int: {ch}')
    yield EndToken()

class Scanner:
    def __init__(self, string: str):
        self.string = string

    def __iter__(self):
        self.iter = scanner_gen(self.string)
        self.next = next(self.iter, None)
        return self

    def __next__(self) -> Token:
        if self.next is None:
            raise StopIteration
        ret = self.next
        self.next = next(self.iter, None)
        return ret
