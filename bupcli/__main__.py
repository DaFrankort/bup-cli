#!/usr/bin/env python3
import sys
from . import add

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print('no args given')
        return

    for arg in args:
        arg = format(arg)
        print(arg)

    add.check(args)

if __name__ == '__main__':
    main()