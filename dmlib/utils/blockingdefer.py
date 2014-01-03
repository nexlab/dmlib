###########################################################################
# Copyright (c) 2011-2014 Unixmedia S.r.l. <info@unixmedia.it>
# Copyright (c) 2011-2014 Franco (nextime) Lanza <franco@unixmedia.it>
#
# Domotika System Controller Daemon "domotikad"  [http://trac.unixmedia.it]
#
# This file is part of domotikad.
#
# domotikad is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from twisted.internet import defer, reactor, threads
import time


class BlockingDefer(object):

   result = None
   errors = None
   done = None
   timeout = False

   def run(self, d, timeout=10):
      start = time.time()
      d.addCallbacks(self.callbackDone, self.callbackError)
      while not self.done:
         if int(time.time()-start) > timeout:
            self.timeout =  True
            self.done =  True
         reactor.iterate(0.05)
         time.sleep(.05)
      if self.timeout:
         raise "Timeout Error"
      else:
         if not self.errors:
            return self.result
         else:
            raise self.errors

   def callbackError(self, err=True):
      self.errors = err
      self.done = True

   def callbackDone(self, result):
      self.result = result
      self.done = True


def blockingDeferred(d, timeout=5):
   bd=BlockingDefer()
   ret=bd.run(d, timeout)
   del bd
   return ret
   
