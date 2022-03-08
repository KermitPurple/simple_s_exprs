#!/usr/bin/env python3

from interpret import interpret

def main():
    '''Driver Code'''
    interpret(
        '(print \'Hello World!\' 100)'
        '(print 1)'
        '(print(add 1 2))'
        '(print(add (mul 2.5 8) 20))'
    )

if __name__ == '__main__':
    main()
