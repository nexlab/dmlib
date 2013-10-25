###########################################################################
# Copyright (c) 2011-2013 Unixmedia S.r.l. <info@unixmedia.it>
# Copyright (c) 2011-2013 Franco (nextime) Lanza <franco@unixmedia.it>
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

import logging
import DMDomain as dmd

log = logging.getLogger( 'DMDomain' )


def isMatch(s):
   specials=['[',']','!','*','|']
   if len(s) > 32:
      return False
   for i in specials:
      if i in s:
         return False
   return True
   #return dmd.ValidateDomainString(s, dmd.DOMAIN_TYPE_MATCH, len(s))==s

# il primo e' passato dalla query 
# il secondo arriva dal db
def match(dmstr, dmchk):
   if ' ' in dmstr:
      dmstr=dmstr.split()
      if(len(dmstr)>1) and dmstr[1].lower() in ['rev', 'reversed']:
         log.debug("DMDOMAIN REVERSED")
         ret=dmd.DMDomainMatch(dmchk, dmstr[0], len(dmchk))
      else:
         log.debug("DMDOMAIN NOT REVERSED")
         ret=dmd.DMDomainMatch(dmstr[0], dmchk, len(dmstr[0]))
   else:
      ret=dmd.DMDomainMatch(dmstr, dmchk, len(dmstr))
   log.debug("DMDOMAIN check for %s, %s: %s" % (dmstr, dmchk, str(ret)))
   return ret
