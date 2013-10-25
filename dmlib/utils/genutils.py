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


try:
   import hashlib
   md5 = hashlib
   md5.new = hashlib.md5
   sha1 = hashlib.sha1
except:
   import md5
   import sha1

from ConfigParser import SafeConfigParser

def revlist(l): l.reverse(); return l

class FakeObject(object):
   pass

class configFile(SafeConfigParser):

   def __init__(self, config):
      self.configfile = config
      SafeConfigParser.__init__(self)

   def readConfig(self):
      return self.read(self.configfile)

   def writeConfig(self):
      fd = open(self.configfile, "w")
      self.write(fd)
      fd.close()
      return True


   def getOptions(self, section):
      res = {}
      for opt in self.items(section):
         try:
            res[opt[0]] = opt[1]
         except:
            pass
      return res


class CircularList(list):
    """
    A list that wraps around instead of throwing an index error.
    
    Works like a regular list:
    >>> cl = CircularList([1,2,3])
    >>> cl
    [1, 2, 3]
    
    >>> cl[0]
    1
    
    >>> cl[-1]
    3
    
    >>> cl[2]
    3
    
    Except wraps around:
    >>> cl[3]
    1
    
    >>> cl[-4]
    3
    
    Slices work
    >>> cl[0:2]
    [1, 2]
    
    but only in range.
    """
    def __getitem__(self, key):
        
        # try normal list behavior
        try:
            return super(CircularList, self).__getitem__(key)
        except IndexError:
            pass
        # key can be either integer or slice object,
        # only implementing int now.
        try:
            index = int(key)
            index = index % self.__len__()
            return super(CircularList, self).__getitem__(index)
        except ValueError:
            raise TypeError


class CircularList2(list):
    
   def __init__(self, sequence):
      list.__init__(self, sequence)
      self.i = 0
            
   def set_index(self, i):
      if i not in range(len(self)):
         raise IndexError, 'Can\'t set index out of range'
      else:
         self.i = i
            
   def next(self, n=1):
      if self == []:
         return None
      if n < 0:
         return self.prev(abs(n))    
      if self.i not in range(len(self)):
         self.i = len(self) - 1 
      if self.i + n >= len(self):
         i = self.i
         self.set_index(0)
         return self.next(n - len(self) + i)
      else:
         self.set_index(self.i + n)
         return self[self.i]
            
   def prev(self, n=1):
      if self == []:
         return None
      if n < 0:
         return self.next(abs(n))
      if self.i not in range(len(self)):
         self.i = len(self) - 1 
      if self.i - n < 0:
         i = self.i
         self.set_index(len(self) - 1)
         return self.prev(n - i - 1)
      else:
         self.i -= n
         return self[self.i]


class SliceCircular(CircularList2):

   def getdata(self, howmany=1):
      if(howmany > len(self)):
         howmany=len(self)
      i=self.i
      distance=int((howmany-1)/2)
      ret=[]
      self.prev(distance+1)
      while howmany > 0:
         ret.append(self.next())
         howmany-=1
      self.i=i
      return ret


def invertWord(word):
   import struct
   return struct.pack('<2B', struct.unpack('<2B', str(word[:2]))[1], 
                             struct.unpack('<2B', str(word[:2]))[0])


def isIp(addr):
   ip=addr.split(".")
   if len(ip)==4:
      for n in ip:
         if not unicode(n).isnumeric() or int(n) <0 or int(n) > 255:
            return False
      return True
   return False


def is_number(s):
   try:
      float(s) # for int, long and float
   except ValueError:
      try:
         complex(s) # for complex
      except ValueError:
         return False
   except:
      return False
   return True


def isTrue(d):
   if str(d).lower() in ["1", "true", "yes", "si", "y"]:
      return True
   return False


def board_syspwd(cfgpwd):
   if len(cfgpwd)>4:
      return cfgpwd
   return 'domotika'

def devs_adminpwd(cfgpwd):
   if len(cfgpwd)>4:
      return cfgpwd
   return 'domotika'


def ip_match(mask, ip):
   if mask=='255.255.255.255' or mask=='0.0.0.0':
      return True
   else:
      return mask==ip

def hashPwd(pwd):
   if pwd and len(pwd)>3:
      s=sha1()
      s.update(pwd)
      return s.hexdigest()
   return False
   
