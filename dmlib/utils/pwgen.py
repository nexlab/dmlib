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

from random import Random

lefthand="789yuiophjklbnmYUIOPHJKLBNM"
righthand="123456qwertyasdfgzxcvQWERTYASDFGZXCV"
allchars=lefthand+righthand


def GeneratePwd(leng=8, alt=False):
   rng = Random()
   pwd=""
   for i in range(leng):
      if not alt:
         pwd+=rng.choice(allchars)
      else:
         if i%2:
            pwd+=rng.choice(lefthand)
         else:
            pwd+=rng.choice(righthand)
   return pwd

def GenerateHexKey(leng=8):
   import struct
   rng = Random()
   pwd=[]
   for i in range(leng):
      pwd.append(rng.randint(0, 255))
   return struct.pack('<%dB' % leng, *pwd)

def generateIV128(pwdhash):
   from genutils import invertWord
   import struct
   res=""
   i=0
   while(i<16):
      a=struct.unpack('<H',invertWord(pwdhash[i:i+2]))[0]
      b=struct.unpack('<H',pwdhash[i+16:i+16+2])[0]
      res+=struct.pack('<H', a^b)
      i+=2
   return res
      
