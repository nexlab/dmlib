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

from zope.interface import implements
from twisted.internet import defer
import formal 
from formal import iformal

REGEX_IP_ADDRESS=('b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).)'
      '{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)b')

REGEX_EMAIL="^[a-zA-Z0-9]+([\._\-a-zA-Z0-9]+)*@[a-zA-Z0-9]+([._\-a-zA-Z0-9]+[\.][a-zA-Z]{2,5})+$"

REGEX_URI=("(http|https|mail|telnet|ftp|imap|irc|file):\/\/[a-z0-9]+"
   "([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}((:[0-9]{1,5})?\/.*)?$")


class GenericValidator(object):

   def __init__(self, errmsg=u'Cannot validate'):
      self.errmsg = errmsg

   def check(self, value):
      return False

   def validate(self, field, value):
      if not self.check(value):
         raise formal.FieldValidationError(self.errmsg)


class GenericWordListValidator(GenericValidator):

   def __init__(self, wordlist=[], errmsg=u'Word not in list'):
      self.wordlist = wordlist
      GenericValidator.__init__(self, errmsg)

   def check(self, value):
      if value in self.wordlist:
         return True
      else:
         return False


class YesNoValidator(GenericWordListValidator):

   def __init__(self, errmsg=u'Only yes or not are valid values'):
      GenericWordListValidator.__init__(self, ['yes', 'no'], errmsg)


class AcceptPolicy(GenericWordListValidator):
   def __init__(self, errmsg=u'You must accept our terms of usage!'):
      GenericWordListValidator.__init__(self, ['yes'], errmsg)
