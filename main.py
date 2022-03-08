#!/usr/bin/env python3

from interpret import interpret
from typing import IO
from sys import argv

def interactive():
    try:
        while 1:
            interpret(input('interpreter> '))
    except EOFError:
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

if __name__ == '__main__':
    main()
