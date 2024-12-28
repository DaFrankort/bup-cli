#!/usr/bin/env python3
import sys
from .commands import add_path
from .commands import list_paths
from .commands import del_path


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        # TODO -> Print help command or version or something :-)
        print('No arguments given.')
        return

    # TODO MAKE SWITCH CASE
    add_path.check_and_run(args)
    list_paths.check_and_run(args)
    del_path.check_and_run(args)

if __name__ == '__main__':
    main()