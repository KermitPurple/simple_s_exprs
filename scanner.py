'''
Handles scanning the character stream and converting it into a character stream
'''

from dataclasses import dataclass
from typing import TypeVar, Iterator
from enum import Enum

T = TypeVar('T')

class ScannerException(Exception): pass

class ScanningState(Enum):
    GENERAL = 0
    IDENT = 1
    INT = 2
    FLOAT = 3
    STRING = 4
    STRING_ESCAPE = 5

@dataclass
class Token: pass
class EndToken(Token): pass
class LParenToken(Token): pass
class RParenToken(Token): pass

@dataclass
class IdentToken(Token):
    name: str

@dataclass
class ValueToken(Token):
    value: T

def scanner_gen(string: str) -> Iterator[Token]:
    '''
    use a generator to convert character stream to tokens stream
    :string: the character stream to convert
    '''
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
                elif ch == "'":
                    state = ScanningState.STRING
                elif ch == ')':
                    yield RParenToken()
                elif ch == '(':
                    yield LParenToken()
                else:
                    partial += ch
                    state = ScanningState.IDENT
            case ScanningState.IDENT:
                if ch.isspace() or ch in '()':
                    if partial in ('True', 'False'):
                        if partial == 'True':
                            yield ValueToken(True)
                        else:
                            yield ValueToken(False)
                        state = ScanningState.GENERAL
                        partial = ''
                        continue
                    yield IdentToken(partial)
                    if ch == ')':
                        yield RParenToken()
                    elif ch == '(':
                        yield LParenToken()
                    state = ScanningState.GENERAL
                    partial = ''
                else:
                    partial += ch
            case ScanningState.INT:
                paren = ch in '()'
                if ch.isspace() or paren:
                    yield ValueToken(int(partial))
                    if ch == ')':
                        yield RParenToken()
                    elif ch == '(':
                        yield LParenToken()
                    state = ScanningState.GENERAL
                    partial = ''
                elif ch.isnumeric():
                    partial += ch
                elif ch == '.':
                    partial += ch
                    state = ScanningState.FLOAT
                else:
                    raise ScannerException(f'Unexpected character inside int: {ch}')
            case ScanningState.STRING:
                match ch:
                    case '\'':
                        yield ValueToken(partial)
                        state = ScanningState.GENERAL
                        partial = ''
                    case '\\':
                        state = ScanningState.STRING_ESCAPE
                    case _:
                        partial += ch
            case ScanningState.STRING_ESCAPE:
                match ch:
                    case 'n':
                        partial += '\n'
                    case 't':
                        partial += '\t'
                    case 'b':
                        partial += '\b'
                    case 'v':
                        partial += '\v'
                    case '\'':
                        partial += '\''
                    case _:
                        partial += '\\' + ch
                state = ScanningState.STRING
            case ScanningState.FLOAT:
                paren = ch in '()'
                if ch.isspace() or paren:
                    yield ValueToken(float(partial))
                    if ch == ')':
                        yield RParenToken()
                    elif ch == '(':
                        yield LParenToken()
                    state = ScanningState.GENERAL
                    partial = ''
                elif ch.isnumeric():
                    partial += ch
                else:
                    raise ScannerException(f'Unexpected character inside int: {ch}')
    yield EndToken()

class Scanner:
    '''
    A token stream iterator with 1 look ahead
    '''
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
