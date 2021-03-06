from typing import TypeVar

T = TypeVar('T')

KEYWORDS = [
    'assign', '=',
    'add_assign', '+=',
    'sub_assign', '-=',
    'mul_assign', '*=',
    'div_assign', '/=',
    'mod_assign', '%=',
    'inc', '++',
    'dec', '--',
    'if',
    'def',
    'while',
    'for',
    'fore',
]

def copy_table(src: dict[str, any], dst: dict[str, any]):
    '''
    copy contents of one symbol table into another
    :src: the table to copy from
    :dst: the table to copy to
    '''
    # delete all keys
    for key in list(dst.keys()):
        del dst[key]
    # add keys back
    for key, value in src.items():
        dst[key] = value

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

    def lst(*args: T) -> list[T]:
        return list(args)

    def append(list_: list[T], item: T) -> list[T]:
        if not isinstance(list_, list):
            raise TypeError('the first argument in the append function must be a list')
        list_.append(item)
        return list_

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
        'append': append,
        'app': append,
        'input': input,
        'int': int,
        'float': float,
        'str': str,
        'len': len,
    }

