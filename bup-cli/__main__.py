#!/usr/bin/env python3
import sys

def main():
    print('BUP!')
    args = sys.argv[1:]
    for arg in args:
        print(format(arg))

if __name__ == '__main__':
    main()