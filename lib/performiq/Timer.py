
from datetime import datetime

#==========================================================================

class Timer:
    t_reference = None

    #----------------------------------------------------------------------

    @classmethod
    def init(cls):
       return float(cls.get_reference_time(init=True)) * 0.001

    #----------------------------------------------------------------------

    @classmethod
    def time(cls):
       return float(cls.get_reference_time()) * 0.001

    #----------------------------------------------------------------------

    @classmethod
    def get_reference_time(cls, init=False):
       t_now  = datetime.now()

       if (init):
          cls.t_reference   = t_now
          t                 = 0
       else:
          t_delta           = t_now - cls.t_reference
          t                 = ((t_delta.seconds * 1000000) + t_delta.microseconds)/1000.0

       return t

    #----------------------------------------------------------------------

#==========================================================================

