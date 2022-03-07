#!/usr/bin/env python3

from scanner import Scanner

def main():
    '''Driver Code'''
    scan = Scanner('(+ 5 10)')
    for token in scan:
        print(token)

if __name__ == '__main__':
    main()
