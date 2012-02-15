#!/usr/bin/env python

import urllib

url = 'http://localhost:8081/'
#url = 'http://localhost:8888/'
params = urllib.urlencode({'hoge':1, 'fuga':2})
f = urllib.urlopen(url, params)
print f.read()
