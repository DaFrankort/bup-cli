#!/usr/bin/env python3
import sys
from .commands import add, list

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        # TODO -> Print help command or version or something :-)
        print('No arguments given.')
        return

    add.check_and_run(args)
    list.check_and_run(args)

if __name__ == '__main__':
    main()