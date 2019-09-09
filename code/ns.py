#!/usr/bin/python3

import fileinput
import sys
import re
import subprocess
import os

# eighty '+'
re_lex_begin=re.compile(r'^\+{80}$')
# eighty '='
re_lex_end=re.compile(r'^={80}$')
# nsubj(,word-123)
re_nsubj=re.compile(r'^nsubj\(.* ([a-zA-Z]+)-[0-9]+\)$')
# /NN /NNP /NNS /NNPS
re_nn=re.compile(r'^(.*)\/NNP?S?$')
# <TEXT>
re_text_begin=re.compile(r'^<TEXT>$')
# </TEXT>
re_text_end=re.compile(r'^</TEXT>$')

# check args
if len(sys.argv) < 2:
  sys.exit(0)

#argv[1]: input text file
#argv[2]: output text file
with fileinput.input(files=sys.argv[1]) as fi:
  outfile=open(sys.argv[2], "w")
  inlex=False
  intext=False
  for line in fi:
    # check </TEXT> in case for filtering out the original text
    mb = re_text_end.match(line)
    if mb is not None:
      intext=False
    # check ++++
    mb = re_lex_begin.match(line)
    if mb is not None:
      inlex=True

    # processing
    if inlex == True:
      # (1) nsubj
      m = re_nsubj.match(line)
      if m is not None:
        outfile.write(m.group(1)+"\n")
    else:
      #if intext == False:
      # always write out original text
      outfile.write(line)

    # check ====
    me = re_lex_end.match(line)
    if me is not None:
      inlex=False
    # check <TEXT>
    mb = re_text_begin.match(line)
    if mb is not None:
      intext=True