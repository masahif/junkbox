#!/usr/bin/env python

import re

pattern = [
	#"^\w{3} [ :0-9]{11} [._[:alunum:]-]+",
	#"^\w{3} [ :0-9]{11} [._[:alunum:]-]+",
	"pulseaudio\[[0-9]+\]: ratelimit\.c",
	"kernel: \[[\.0-9]+\] usbcore:",
	"kernel: \[[\.0-9]+\] scsi:",
]

ignore = [
    "ratelimit",
    ]

p = "(?:%s)" % ")|(?:".join(pattern)
i = "(?:%s)" % ")|(?:".join(ignore)

r = re.compile(p)
ri = re.compile(i)

f = open("/var/log/messages")
try:
  for line in f:
    if r.search(line) and not ri.search(line):
      print line,
finally:
  f.close()
