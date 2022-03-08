from typing import TypeVar

T = TypeVar('T')

def neg(a: T) -> T:
    return -a

def add(first: T, *rest: T) -> T:
    for i in rest:
        first += i
    return first

def sub(a: T, b: T) -> T:
    return a - b

def mul(first: T, *rest: T) -> T:
    for i in rest:
        first *= i
    return first

def div(a: T, b: T) -> T:
    return a / b

symbol_table = {
    'print': print,
    'neg': neg,
    '+': add,
    'add': add,
    '-': sub,
    'sub': sub,
    '*': mul,
    'mul': mul,
    '/': div,
    'div': div,
}

