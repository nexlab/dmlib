#!/usr/bin/env python
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

import time
import sys, random                   
import struct
from dmcrypt import AES256
import constants as C
import logging
from utils import pwgen
import copy
import socket
log = logging.getLogger( 'IKAProtocol' )

IKAP_ARGDICT={
   'ip': None,
   'io_type': None,
   'io_subtype': None,
   'act_ret': None,
   'arg_data': None,
   'unused': None,
   'OPT_TYPE': None,
   'OPT_DATA': None,
   'raw': None 
}

def getDefaultDict():
   return copy.deepcopy(IKAP_ARGDICT)

def dictToIkapArg(rd, localip=False):
   d=getDefaultDict()
   d.update(rd)
   try:
      data=False
      if d['OPT_DATA']:
         data=["\x00"]*(20-(9-len(d['OPT_DATA'])))
         data[11:len(data)]=list(struct.pack('<'+str(len(d['OPT_DATA']))+'B', *d['OPT_DATA']))
      if d['OPT_TYPE']:
         if not data: data=["\x00"]*11
         data[10]=struct.pack('<B', d['OPT_TYPE'])
      if d['arg_data']:
         if not data: data=["\x00"]*9
         data[7:9]=list(struct.pack('<H', d['arg_data']))
      if d['act_ret']:
         if not data: data=["\x00"]*7
         data[6]=struct.pack('<B', d['arg_ret'])
      if d['io_subtype']:
         if not data: data=["\x00"]*6
         data[5]=struct.pack('<B', d['io_subtype'])
      if d['io_type']:
         if not data: data=["\x00"]*5
         data[4]=struct.pack('<B', d['io_type'])
      if localip:
         d['ip']=localip
      if d['ip']:
         if not data: data=["\x00"]*4
         data[0:4]=list(socket.inet_aton(d['ip']))
   except:
      return ''
         

   return "".join(data).ljust(20, "\x00")

def ikapArgtoDict(data):
   d=getDefaultDict()
   if len(data)>=4:
      d['ip']=socket.inet_ntoa(data[0:4])
   if len(data)>=5:
      d['io_type']=struct.unpack("<B", data[4])[0]
   if len(data)>=6:
      d['io_subtype']=struct.unpack("<B", data[5])[0]
   if len(data)>=7:
      d['act_ret']=struct.unpack("<B", data[6])[0]
   if len(data)>=9:
      d['arg_data']=struct.unpack("<H", data[7:9])[0]
   #if len(data)>=10:
   #   pass
   if len(data)>=20:
      d['OPT_TYPE']=struct.unpack("<B", data[10])[0]
      opt_data=".".join([socket.inet_ntoa(data[11:15]),
                         socket.inet_ntoa(data[15:19]),
                         str(struct.unpack("<B", data[19])[0])]).split(".")
      d['OPT_DATA']=map(int, opt_data)
   d['raw']=data
   return d


def calcIPCheckSum(data):
    s = 0
    for i in range(0, len(data)):
        c = s+data[i]
        s = (c & 0xffff) + (c >> 16)
    return ~s & 0xffff

#DEFKEY=(0xdeadbeef, 0xcafebabe, 0xdefec8ed, 0xbaadf00d)
#DEFKEY="deadbeefcafebabedefec8edbaadf00dca8b49745393d660b7b55dbb29523971"
DEFKEY="\xde\xad\xbe\xef\xca\xfe\xba\xbe\xde\xfe\xc8\xed\xba\xad\xf0\x0d\xca\x8b\x49\x74\x53\x93\xd6\x60\xb7\xb5\x5d\xbb\x29\x52\x39\x71"
DEFIV=pwgen.generateIV128(DEFKEY)

CONST={}
CONST_MSG={}
CONST_ACT={}
CONST_CTX={}
CONST_ENC={}
for co in dir(C):
   if type(eval('C.'+co)).__name__=='int':
      if co.startswith('IKAP_MSG'):
         CONST_MSG[eval('C.'+co)]=co
      elif co.startswith('IKAP_ACT'):
         CONST_ACT[eval('C.'+co)]=co
      elif co.startswith('IKAP_CTX'):
         CONST_CTX[eval('C.'+co)]=co
      elif co.startswith('IKAP_ENC'):
         CONST_ENC[eval('C.'+co)]=co
      else:
         CONST[eval('C.'+co)]=co




class IkaPacketHeader(struct.Struct):

   epoch=0
   msgtype=C.IKAP_MSG_ACTION
   ctx=C.IKAP_CTX_USER
   act=C.IKAP_ACT_DEBUG
   srclen=0
   dstlen=0
   arglen=0
   version=0
   enctype=0
   cfg=0
   chksum=0
   key=[0,0,0,0]

   def __init__(self, hdr=None):
      struct.Struct.__init__(self, '<LBHBBBBBBBHLLLL')
      self.unpacked=None

   def setHdr(self):
      self.data=self.tobytes()
      self.unpacked=self.unpack(self.data)
      self.hdr=list(self.unpacked)

   def formatHeader(self, data):
      self.unpacked=self.unpack(data)
      self.hdr=list(self.unpacked)
      self.data=data
      self.epoch, self.msgtype, self.ctx, self.act, self.srclen, self.dstlen, \
      self.arglen, self.version, self.enctype, self.cfg, self.chksum, self.key[0], self.key[1],  \
      self.key[2], self.key[3] = self.hdr

   def tobytes(self):
      return struct.pack('<LBHBBBBBBBHLLLL', self.epoch, self.msgtype, self.ctx, self.act, self.srclen, self.dstlen, \
            self.arglen, self.version, self.enctype, self.cfg, self.chksum, self.key[0], self.key[1],  \
            self.key[2], self.key[3])


   def calculateCheckSum(self):
      #print "%r" % self.data
      cleanchk=struct.pack('<LBHBBBBBBBHLLLL', self.epoch, self.msgtype, self.ctx, self.act, self.srclen, self.dstlen, \
            self.arglen, self.version, self.enctype, self.cfg, 0x0000, self.key[0], self.key[1],  \
            self.key[2], self.key[3])
      d=list(struct.unpack('<16H', cleanchk))
      #print d
      return calcIPCheckSum(d)


   def __repr__(self):
      return str({'original': str(self.hdr),
                  'epoch:': self.epoch,
                  'msgtype': CONST_MSG[self.msgtype],
                  'ctx': CONST_CTX[self.ctx],
                  'act': CONST_ACT[self.act],
                  #'act': self.act,
                  'srclen':self.srclen,
                  'dstlen':self.dstlen,
                  'arglen':self.arglen,
                  'version':self.version,
                  'enctype':CONST_ENC[self.enctype],
                  'cfg': bin(self.cfg),
                  'chksum': hex(self.chksum),
                  'key': [hex(self.key[0])[:-1], hex(self.key[1])[:-1], hex(self.key[2])[:-1], hex(self.key[3])[:-1]]
                 })
      #return str(self.hdr)



class IkaPacket(object):

   hdr=None
   src="Q.USER"
   dst="*"
   arg=""
   epoch=None
   enctype=C.IKAP_ENC_AES256
   memkey=DEFKEY

   def __init__(self, hdr=None):
      if not hdr:
         self.hdr=IkaPacketHeader()
         self.hdr.enctype=C.IKAP_ENC_AES256
         self.hdr.epoch=int(time.time())
         self.calculateChecksum()
         self.setDst(self.dst)
         self.setSrc(self.src)
         self.setArg(self.arg)
         self.setEncType(self.enctype)
      self.epoch=self.hdr.epoch



   def __repr__(self):
      self.hdr.setHdr()
      hdr=self.hdr.__repr__()
      return 'HEADER: '+hdr+"\nSOURCE: "+self.src+"\nDST: "+self.dst+"\nEPOCH :"+str(self.epoch)


   def calculateChecksum(self):
      self.hdr.chksum=self.hdr.calculateCheckSum()

   def setDst(self, dst):
      self.dst=dst
      self.hdr.dstlen=len(dst)
      self.calculateChecksum()

   def setSrc(self, src):
      self.src=src
      self.hdr.srclen=len(src)
      self.calculateChecksum()

   def setArg(self, arg):
      self.arg=arg
      self.hdr.arglen=len(arg)
      self.calculateChecksum()

   def updateTime(self):
      self.hdr.epoch=int(time.time())
      self.epoch=self.hdr.epoch
      self.calculateChecksum()

   def setMsgType(self, msgType):
      self.hdr.msgtype=msgType

   def setCtx(self, ctx):
      self.hdr.ctx=ctx
      self.calculateChecksum()

   def setAct(self, act):
      self.hdr.act=act
      self.calculateChecksum()

   def setEncType(self, enc):
      self.hdr.enctype=enc
      self.calculateChecksum()

   def setMemkey(self, memkey):
      self.memkey=memkey

   def generateKey(self):
      self.hdr.key = struct.unpack('<4L', pwgen.GenerateHexKey(16))
      self.calculateChecksum()

   def _aes(self):
      # XXX Gestire differenti encryption
      aeshdr=AES256(struct.unpack('<8L', DEFKEY), struct.unpack('<4L', DEFIV))

      aesdata=AES256(struct.unpack('<8L', DEFKEY), struct.unpack('<4L', DEFIV))
      aesdata.iv=self.hdr.key

      aeshdr.setCleanData(self.hdr.tobytes())

      totdatalen=self.hdr.srclen+self.hdr.dstlen+self.hdr.arglen
      totdata=self.src+self.dst+self.arg
      totdata=list(ord(c) for c in totdata)

      totdata=struct.pack('<%dB' % totdatalen, *totdata)+struct.pack('<L', self.epoch)
      totdatalen=len(totdata)
      if(len(totdata)%16):
         totdatalen=len(totdata)+16-(len(totdata)%16)
         totdata=totdata.ljust(totdatalen, "\0") # XXX Magari qui usare dei random bytes!
      aesdata.setCleanData(totdata)
      return aeshdr, aesdata


   def cleanpacket(self):
      aeshdr, aesdata = self._aes()
      return aeshdr.cleandata+aesdata.cleandata

   def encryptPacket(self):
      aeshdr, aesdata = self._aes()
      return aeshdr.encdata+aesdata.encdata

    
   def prepare(self):
      self.generateKey()
      self.updateTime()

   def toSend(self):
      self.prepare()
      return struct.pack("<B", C.IKAP_STARTBYTE)+self.encryptPacket()
