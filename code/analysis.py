#!/usr/bin/python3

import fileinput
import sys
import re
import subprocess
import os

re_text_begin=re.compile(r'^<TEXT>$')
re_text_end=re.compile(r'^</TEXT>$')
#re_nsubj=re.compile(r'^nsubj.* ([a-zA-Z]+)-[0-9]+\)$')
if len(sys.argv) < 2:
  sys.exit(0)
tmpname="/tmp/tmptext.%d.txt" % (os.getpid())

javacmd=["java", "-Xmx8G", "-cp", "/home/wuxb/lc/parser/*:",
  "edu.stanford.nlp.parser.lexparser.LexicalizedParser",
  "-outputFormat", "wordsAndTags,typedDependencies",
  "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
  tmpname]
#argv[1]: input text file
#argv[2]: output text file
with fileinput.input(files=sys.argv[1]) as fi:
  outfile=open(sys.argv[2], "w")
  intext=False
  tmpfile=None
  for line in fi:
    # find </TEXT>
    if intext == True:
      m = re_text_end.match(line)
      if (m is not None): # end
        intext=False
        tmpfile.close()
        # convert and write converted content to output
        outfile.write("+"*80+"\n")
        proc=subprocess.Popen(javacmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, universal_newlines=True)
        for line1 in iter(proc.stdout.readline,''):
          #n = re_nsubj.match(str(line1))
          #if n is not None:
          #  outfile.write(n.group(1)+"\n")
          outfile.write(line1)
        outfile.write("="*80+"\n")
    if intext == True: # continue in TEXT
      # write line to tmp file
      tmpfile.write(line)
    # copy to output anyway
    outfile.write(line)
    if intext == False:
      m = re_text_begin.match(line)
      if (m is not None):
        intext=True
        tmpfile=open(tmpname, "w")