#!/usr/bin/env python
#
#       Author:  Peter Harding  <plh@performiq.com.au>
#
#                Mobile:   0418 375 085 
#
#           @(#) [2.3.01] skel.py 2013-02-20
#
#
# NAME
#   skel.py - Skeleton python script
#
# SYNOPSIS
#   skel.py [-dv]
#
# PARAMETERS
#   See __doc__ below
#
# DESCRIPTION
#   ...
#
# RETURNS
#   0 for successful completion, 1 for any error
#
# FILES
#   ...
#
#--------------------------------------------------------------------------
"""
Usage:

   $ skel.py [-dv] -apn 10y

   $ skel.py [-dv] -o             # ...

Parameters:

   -a              ...
   -p              ...
   -n 10           No of ...
   -o              ...
   -d              Debug
   -v              Verbose

"""
#--------------------------------------------------------------------------

import os
import re
import sys
import time
import getopt
import random
import pickle
import pprint
import logging
import urllib

from datetime import datetime

from performiq import Enum, Logger

#--------------------------------------------------------------------------

__version__   = "2.3.01"
__at_id__     = "@(#)  skel.py  [%s]  2013-02-20" % __version__

verbose_flg   = False

debug_level   = 0

lf            = None
log           = None

LOG_DIR       = "/tmp"
home_dir      = None

p_crlf        = re.compile(r'[\r\n]*')

pp            = pprint.PrettyPrinter(indent=3)

#==========================================================================

class Data:
   TotalCount = 0

   #--------------------------------------------------------------------

   @classmethod
   def count_row(cls):
   
      cls.TotalCount += 1

   #--------------------------------------------------------------------

   def __init__(self, row):
   
      Data.count_row()
      
      cols = row.split(',')
      
      self.One = cols[0]
      self.Two = cols[1]

#==========================================================================
# And here is the real work...

def do_work(fname):

   Logger.Info("[do_work]")

   fname_in  = "%s.log" % fname
   fname_out = "%s.dat" % fname

   try:
      f_in = open(fname_in, 'r')
   except IOError, msg:
      sys.stderr.write(fname_in + ': cannot open: ' + `msg` + '\n')
      sys.exit(1)

   try:
      f_out = open(fname_out, 'a+')
   except IOError, msg:
      sys.stderr.write(fname_out + ': cannot open: ' + `msg` + '\n')
      sys.exit(1)

   while True:
      line = f_in.readline()

      if not line: break

      #  Truncate EoL markers from end of line

      line = p_crlf.sub('', line)  # or 'line = line[:-1]'

      data = Data(line)

      f_out.write("[%s]\n" % (line, ))

   f_in.close()
   f_out.close()

#=========================================================================

def usage():

   print __doc__

#-------------------------------------------------------------------------

def main(argv):

   global verbose_flg
   global debug_level
   global target
   global home_dir

   try:
      home_dir = os.environ['HOME']
   except:
      print "Set HOME environment variable and re-run"
      sys.exit(0)

   Modes    = Enum(["Info", "Parse", ])

   mode     = Modes.Info
   filename = "test"

   try:
      opts, args = getopt.getopt(argv, "dD:f:hvV?",
              ("debug", "debug-level=", "file=", "help", "verbose", "version"))
   except getopt.error, msg:
      usage()
      return 1

   for opt, arg in opts:
      if opt in ("-?", "-h", "--help"):
         usage()
         return 0
      elif opt in ('-d', '--debug'):
         debug_level    += 1
      elif opt in ('-D', '--debug-level'):
         debug_level     = int(arg)
      elif opt in ('-f', '--file'):
         mode = Modes.Parse
         filename        = arg
      elif opt in ('-v', '--verbose'):
         verbose_flg     = True
      elif opt in ('-v', '--version'):
         print "[skel]  Version: %s" % __version__
         return 1
      else:
         usage()
         return 1

   sys.stderr.write("[skel]  Working directory is %s\n" % os.getcwd())

   if (debug_level > 0): sys.stderr.write("[skel]  Debugging level set to %d\n" % debug_level)

   sys.stderr.flush()

   Logger.Init(name='skel')

   if mode == Modes.Info:
      Logger.Info('Info')
   elif mode == Modes.Parse:
      Logger.Info('Parsing')
      do_work(filename)
   else:
      Logger.Info('Nothing to do')

   return 0

#--------------------------------------------------------------------------

if __name__ == '__main__' or __name__ == sys.argv[0]:

   try:
      sys.exit(main(sys.argv[1:]))
   except KeyboardInterrupt, e:
      print "[skel]  Interrupted!"

#--------------------------------------------------------------------------

"""
Revision History:

     Date     Who   Description
   --------   ---   ------------------------------------------------------------
   20031014   plh   Initial implementation
   20111101   plh   Add in Enums for modal behaviour
   20130220   plh   Reconstructed performiq module

Problems to fix:

To Do:

Issues:


"""
