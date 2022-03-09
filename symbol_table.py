from typing import TypeVar

T = TypeVar('T')

def new_symbol_table() -> dict[str, any]:
    '''Create a symbol table'''
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

    def mod(a: T, b: T) -> T:
        return a % b

    def eq(a: T, b: T) -> bool:
        return a == b

    def lt(a: T, b: T) -> bool:
        return a < b

    def gt(a: T, b: T) -> bool:
        return a > b

    def le(a: T, b: T) -> bool:
        return a <= b

    def ge(a: T, b: T) -> bool:
        return a >= b

    def nop(*args: T):
        if args:
            return args[-1]

    def lst(*args: T) -> list[T]: return list(args)

    return {
        'print': print,
        'neg': neg,
        'add': add,
        '+': add,
        'sub': sub,
        '-': sub,
        'mul': mul,
        '*': mul,
        'div': div,
        '/': div,
        'mod': mod,
        '%': mod,
        'eq': eq,
        '==': eq,
        'lt': lt,
        '<': lt,
        'gt': gt,
        '>': gt,
        'le': le,
        '<=': le,
        'ge': ge,
        '>=': ge,
        'nop': nop,
        'lst': lst,
    }

