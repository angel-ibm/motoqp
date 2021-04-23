#!/usr/bin/env python3
# This is to capture the print statements of a command
# and display them in a browser. A dirty trick, I know.

import subprocess

def myexec(program='') :
  if (program == '') :
    return ("Hi there!")
  result = subprocess.run([program], stdout=subprocess.PIPE)
  return ('<pre>' + result.stdout.decode('utf-8') + '</pre>')
