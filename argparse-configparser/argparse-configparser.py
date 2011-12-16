#!/usr/bin/env python

#
# If you use under Python2.6, you can simply type "pip install argparse"
#
import argparse

parser = argparse.ArgumentParser(prog='SampleApp')
parser.add_argument('-d')

config = configparser.ConfigParser()
