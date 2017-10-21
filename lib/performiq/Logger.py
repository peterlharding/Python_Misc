
import os
import sys
import logging

from datetime import datetime

#==========================================================================

class MyFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)[0:23]
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s

#==========================================================================

class Logger:
    logger = None
    debug  = False

    #----------------------------------------------------------------------

    @classmethod
    def Info(cls, msg):
        global debug_level, verbose_flg

        if not cls.logger:
            cls.Init()

        cls.logger.info(' ' + msg)

        if cls.debug: sys.stderr.write("[%s::INFO]  %s\n" % (cls.name, msg))

    #----------------------------------------------------------------------

    @classmethod
    def Error(cls, msg):
        global debug_level, verbose_flg

        if not cls.logger:
            cls.Init()

        cls.logger.error(msg)

        if cls.debug: sys.stderr.write("[%s::ERROR]  %s\n" % (cls.name, msg))

    #----------------------------------------------------------------------

    @classmethod
    def Warning(cls, msg):
        global debug_level, verbose_flg

        if not cls.logger:
            cls.Init()

        cls.logger.warning('*****' + msg + '*****')

        if cls.debug: sys.stderr.write("[%s::WARNING]  %s\n" % (cls.name, msg))

    #----------------------------------------------------------------------

    @classmethod
    def Init(cls, name='logger', dir=None, debug=False):
        cls.debug = debug
        cls.name  = name
        cls.pid   = os.getpid()

        if cls.debug: sys.stderr.write("[%s::Init] PID is %d\n" % (cls.name, cls.pid))

        if dir:
            cls.log_file = '%s/%s.log' % (dir, name)
        else:
            cls.log_file = '%s.log' % (name, )

        try:
            cls.logger  = logging.getLogger(name)
            cls.hdlr    = logging.FileHandler(cls.log_file)
            cls.fmtr    = MyFormatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d,%H:%M:%S.%f')

            cls.hdlr.setFormatter(cls.fmtr)
            cls.logger.addHandler(cls.hdlr)
            cls.logger.setLevel(logging.INFO)

            cls.logger.info("===== Started processing %s" % ('=' * 20))
 
            cls.count = 0
        except IOError, msg:
            sys.stderr.write(cls.log_file + ': cannot open: ' + `msg` + '\n')
            sys.exit(1)

#==========================================================================
