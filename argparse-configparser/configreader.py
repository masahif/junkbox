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
            raise Exception
        config_files.append(c)

    for d in args.dir:
        if not os.path.isdir(d):
            print 'Config directory (%s) is not found.' % d
            parser.print_help()
            raise Exception

        for c in sorted(os.listdir(d)):
            p = os.path.join(d, c)
            if c.endswith('.ini') and os.path.isfile(p):
                config_files.append(p)

    if len(config_files) == 0:
        parser.print_help()
        raise Exception

    config = ConfigParser.ConfigParser()
    config.read(config_files)
    print config_files

    return config

if __name__ == "__main__":
    config =  argparse_configread('-c config.ini -d config'.split())

    print config.sections()
    for sect in config.sections():
        for d in config.items(sect):
            print "sect:%s" % sect,
            print d
            
