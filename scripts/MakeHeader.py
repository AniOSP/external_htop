#!/usr/bin/python

import os, sys, string

ANY=1
COPY=2
SKIP=3
SKIPONE=4

state = ANY

file = open(sys.argv[1])
name = sys.argv[1][:-2]

out = open(name + ".h", "w")
class writer:
   def __init__(self, file):
      self.file = file
   def write(self, text):
      self.file.write(text + "\n")
out = writer(out)

selfheader = '#include "' + name + '.h"'

out.write( "/* Do not edit this file. It was automatically generated. */" )
out.write( "" )

out.write( "#ifndef HEADER_" + name )
out.write( "#define HEADER_" + name )
for line in file.readlines():
   line = line[:-1]
   if state == ANY:
      if line == '/*{':
         state = COPY
      elif line == selfheader:
         pass
      elif string.find(line, "typedef") == 0 or line == "/* private */":
         state = SKIP
      elif string.find(line, "/* private property */") == 0:
         state = SKIPONE
      elif len(line) > 1 and line[-1] == "{":
         out.write( line[:-2] + ";" )
         state = SKIP
      elif line == "":
         out.write( "" )
      else:
         out.write( line )
   elif state == COPY:
      if line == "}*/":
         state = ANY
      else:
         out.write( line )
   elif state == SKIP:
      if len(line) >= 1 and line[0] == "}":
         state = ANY
   elif state == SKIPONE:
      state = ANY

out.write( "" )
out.write( "#endif" )