#!/usr/bin/env python3

from symbol_table import new_symbol_table
from interpret import interpret
from typing import IO
from sys import argv

def interactive():
    symbol_table = new_symbol_table()
    try:
        while 1:
            val = interpret(input('interpreter> '), symbol_table)
            if val is not None:
                print(f'{val!r}')
    except (KeyboardInterrupt, EOFError):
        pass

def from_file(file: IO[str]):
    interpret(file.read())

def main():
    '''Driver Code'''
    _ = argv.pop(0)
    match len(argv):
        case 0:
            interactive()
        case 1:
            with open(argv[0], 'r') as file:
                from_file(file)
        case _:
            print('Invalid number of arguments')

if __name__ == '__main__':
    main()
