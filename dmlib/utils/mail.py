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

import smtplib
from email import MIMEText, MIMEMultipart

from OpenSSL.SSL import SSLv3_METHOD

from twisted.internet import reactor
from twisted.mail.smtp import ESMTPSenderFactory
from twisted.internet.ssl import ClientContextFactory
from twisted.internet.defer import Deferred
import logging
from cStringIO import StringIO

log = logging.getLogger( 'SkylivedCore' )

# XXX: ATTENZIONE: la libreria email e' molto cambiata in python 2.5, verifica
# e rendi il tutto compatibile!


def sendmail(
   authenticationUsername, authenticationSecret,
   fromAddress, toAddress,
   messageFile,
   smtpHost, smtpPort=25, requiredAuth=False
   ):
   """
   @param authenticationUsername: The username with which to authenticate.
   @param authenticationSecret: The password with which to authenticate.
   @param fromAddress: The SMTP reverse path (ie, MAIL FROM)
   @param toAddress: The SMTP forward path (ie, RCPT TO)
   @param messageFile: A file-like object containing the headers and body of
   the message to send.
   @param smtpHost: The MX host to which to connect.
   @param smtpPort: The port number to which to connect.

   @return: A Deferred which will be called back when the message has been
   sent or which will errback if it cannot be sent.
   """

   # Create a context factory which only allows SSLv3 and does not verify
   # the peer's certificate.
   contextFactory = ClientContextFactory()
   contextFactory.method = SSLv3_METHOD

   resultDeferred = Deferred()

   senderFactory = ESMTPSenderFactory(
       authenticationUsername,
       authenticationSecret,
       fromAddress,
       toAddress,
       messageFile,
       resultDeferred,
       contextFactory=contextFactory,
       requireAuthentication=requiredAuth)

   reactor.connectTCP(smtpHost, smtpPort, senderFactory)

   return resultDeferred


def cbSentMessage(result):
   """
   Called when the message has been sent.

   Report success to the user and then stop the reactor.
   """
   log.info("Message sent "+str(result))



def ebSentMessage(err):
   """
   Called if the message cannot be sent.

   Report the failure to the user and then stop the reactor.
   """
   log.info("Error sending message "+str(err))


class GenericEmail:

   def __init__(self, server="127.0.0.1"):
      self.Subject = "This is a default subject"
      self.From = "me"
      self.To = "you"
      self.Reply = "you"
      self.Cc = False
      self.server = server
      self.serverport = 25
      self.username = 'test@mail.com'
      self.password = 'passwd'
      self.msg=MIMEText.MIMEText("Default message")

   def SetTo(self, to):
      self.To=to
      #self.Reply=to

   def SetCc(self, cc):
      self.Cc=cc

   def SetSubject(self, subject):
      self.Subject=subject

   def SetFrom(self, From):
      self.From=From
      self.Reply=From

   def SetReply(self, reply):
      self.Reply=reply

   def Send(self):
      msg=self.msg
      msg['Subject'] = self.Subject
      msg['From'] = self.From
      self._from = self.From
      if "<" in self.From:
         self._from = ""
         start=False
         for c in self.From:
            if start and c=='>':
               start=False
            if start:
               self._from += c
            if c == '<':
               start=True

      msg['To'] = self.To
      msg['Reply-To'] = self.Reply  
      if self.Cc:
         msg['Cc'] = self.Cc
      #s=smtplib.SMTP(self.server)
      #s.connect()
      #s.sendmail(self.From, [self.To], msg.as_string())
      #s.close()
      toAddress = self.To
      if self.Cc:
         try:
            toAddress.append(self.Cc)
         except:
            toAddress = [self.To, self.Cc]
      result = sendmail(
         self.username,
         self.password,
         self._from,
         toAddress,
         StringIO(msg.as_string()),
         self.server,
         self.serverport)
      result.addCallbacks(cbSentMessage, ebSentMessage)


class TextEmail(GenericEmail):

   def SetMsg(self, msg):
      self.msg=MIMEText.MIMEText(msg)


class HTMLEmail(GenericEmail):

   def __init__(self, *args, **kwargs):
      GenericEmail.__init__(self, *args, **kwargs)
      self.msg=MIMEMultipart.MIMEMultipart('alternative')
      self._txtmsg = MIMEText.MIMEText('default txt', 'plain')
      self._htmlmsg = MIMEText.MIMEText('<html><body>default html</body></html>', 'html')

   def SetTextMsg(self, msg):
      self._txtmsg = MIMEText.MIMEText(msg, 'plain')

   def SetHtmlMsg(self, msg):
      self._htmlmsg = MIMEText.MIMEText(msg, 'html')

   def Send(self):
      self.msg.attach(self._htmlmsg)
      self.msg.attach(self._txtmsg)
      return GenericEmail.Send(self)

