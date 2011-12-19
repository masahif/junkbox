#!/usr/bin/env python

#
# If you use under Python2.6, you can simply type "pip install argparse"
#
import argparse
import ConfigParser
import os, sys

def argparse_configread(argv):
    parser = argparse.ArgumentParser(prog='argparse-configparser')
    parser.add_argument('-c', '--config',
                        nargs = '*',
                        metavar = 'CONFIG',
                        help = '%(prog)s.ini etc....',
                        default = []
        )
    parser.add_argument('-d', '--dir',
                        nargs='*',
                        metavar = 'CONFIGDIR',
                        help='directories includes configurations',
                        default = []
        )

    args = parser.parse_args(argv)

    config_files = []
    for c in args.config:
        if not c.endswith('.ini') or not os.path.isfile(c):
            print 'Config file should be ends with ".ini"'
            parser.print_help()
            sys.exit(1)
        config_files.append(c)

    for d in args.dir:
        if not os.path.isdir(d):
            print 'Config directory (%s) is not found.' % d
            parser.print_help()
            sys.exit(1)

        for c in sorted(os.listdir(d)):
            if c.endswith('.ini'):
                config_files.append(c)

    if len(config_files) == 0:
        parser.print_help()
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.read(config_files)

    return config

if __name__ == "__main__":
    print argparse_configread('-c config.ini -d config'.split())
    argparse_configread('-c config.in -d config'.split())
