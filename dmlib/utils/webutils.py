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

from twisted.web import client, error, http
from twisted.internet import reactor, defer, task
from twisted.python import failure
from urlparse import urlunparse
from urllib import splithost, splittype
import gzip
import StringIO
import time
import base64, urlparse

def _parse(url, defaultPort=None):
    """
    Split the given URL into the scheme, host, port, and path.

    @type url: C{str}
    @param url: An URL to parse.

    @type defaultPort: C{int} or C{None}
    @param defaultPort: An alternate value to use as the port if the URL does
    not include one.

    @return: A four-tuple of the scheme, host, port, and path of the URL.  All
    of these are C{str} instances except for port, which is an C{int}.
    """
    url = url.strip()
    parsed = http.urlparse(url)
    scheme = parsed[0]
    path = urlunparse(('', '') + parsed[2:])

    if defaultPort is None:
        if scheme == 'https':
            defaultPort = 443
        else:
            defaultPort = 80

    host, port = parsed[1], defaultPort
    if ':' in host:
        host, port = host.split(':')
        try:
            port = int(port)
        except ValueError:
            port = defaultPort

    if path == '':
        path = '/'

    return scheme, host, port, path


class HTTPPageGetter(client.HTTPPageGetter):

   rectimeout = 15
   checkTimeout = False

   # XXX Serve per farlo diventare 1.1??
   #def sendCommand(self, command, path):
   #   self.transport.write('%s %s HTTP/1.1\r\n' % (command, path))

   def lineReceived(self, *args, **kwargs):
      self.lastrec = time.time()
      return client.HTTPPageGetter.lineReceived(self, *args, **kwargs)

   def rawDataReceived(self, *args, **kwargs):
      self.lastrec = time.time()
      return client.HTTPPageGetter.rawDataReceived(self, *args, **kwargs)

   def connectionMade(self, *args, **kwargs):
      self.lastrec = time.time()
      if self.checkTimeout:
         try:
            self.checkTimeout.stop()
         except:
            pass
      if self.factory.http_user:
         cred = '%s:%s' % (self.factory.http_user,
                           self.factory.http_password)
         auth = "Basic " + base64.encodestring(cred).replace('\012','')
         #self.sendHeader('Authorization', auth)
         self.factory.headers['Authorization'] = auth
      self.checkTimeout = task.LoopingCall(self.timeoutCheck)
      self.checkTimeout.start(1)
      return client.HTTPPageGetter.connectionMade(self, *args, **kwargs)


   def timeoutCheck(self):
      now = time.time()
      if int(now)-int(self.lastrec) > self.rectimeout:
         self.transport.loseConnection()

   def connectionLost(self, *args, **kwargs):
      if self.checkTimeout:
         try:
            self.checkTimeout.stop()
         except:
            pass
      try:
         return client.HTTPPageGetter.connectionLost(self, *args, **kwargs)
      except:
         pass

   def handleStatus_404(self):
      self.handleStatusDefault()
      self.factory.noPage(
            failure.Failure(
               error.Error(self.status,self.message,None)
            )
         )
      self.quietLoss = 1
      self.transport.loseConnection()


   def handleStatus_401(self):
      self.handleStatusDefault()
      self.factory.noPage(
            failure.Failure(
               error.Error(self.status,self.message,None)
            )
         )
      self.quietLoss = 0
      self.transport.loseConnection()


   def handleStatus_301(self):
      l = self.headers.get('location')
      if not l:
         self.handleStatusDefault()
         return
      url = l[0]
      if self.factory.path==url and self.factory.method=="POST":
         self.factory.method="GET"
      if self.followRedirect:
         scheme, host, port, path = \
            client. _parse(url, defaultPort=self.transport.getPeer().port)
         self.factory.setURL(url)
    
         if self.factory.scheme == 'https':
            from twisted.internet import ssl
            contextFactory = ssl.ClientContextFactory()
            self.factory.react = reactor.connectSSL(self.factory.host, self.factory.port, 
                               self.factory, contextFactory)
         else:
            if self.factory.proxy_host:
               if not self.factory.proxy_port:
                  proxy_port = 80
               self.factory.react = reactor.connectTCP(self.factory.proxy_host, self.factory.proxy_port, self.factory)
            else:
               self.factory.react = reactor.connectTCP(self.factory.host, self.factory.port, 
                                  self.factory)
      else:
         self.handleStatusDefault()
         self.factory.noPage(
            failure.Failure(
               error.PageRedirect(
                  self.status, self.message, location = url)))
      self.quietLoss = 1
      self.transport.loseConnection()

   handleStatus_302 = lambda self: self.handleStatus_301()



class HTTPPageGetterProgress(HTTPPageGetter):

   trasmittingPage = 0
   pageData = ""

   def handleStatus_200(self, partialContent=0):
      HTTPPageGetter.handleStatus_200(self)
      self.trasmittingPage = 1

   def handleStatus_206(self):
      self.handleStatus_200(partialContent=1)

   def handleResponsePart(self, data):
      self.pageData += data
      if self.trasmittingPage:
         try:
            self.factory.pagePart(data)
         except:
            pass

   def handleResponseEnd(self):
      if self.trasmittingPage:
         self.trasmittingPage = 0
         self.factory.page(self.pageData)
         self.factory.pageData = ""
      if self.failed:
         self.factory.noPage(
            failure.Failure(
               error.Error(
                  self.status, self.message, None)))
         self.transport.loseConnection()

class HTTPPageGetterProgressStream(HTTPPageGetterProgress):

   def handleResponsePart(self, data):
      #self.pageData += data
      if self.trasmittingPage:
         try:
            self.factory.pagePart(data)
         except:
            pass



class HTTPClientFactory(client.HTTPClientFactory):
    protocol = HTTPPageGetter
    def __init__(self, url, method='GET', postdata=None, headers=None,
               agent="Domotika Client (http://www.unixmedia.it)", timeout=0, cookies=None,
               followRedirect=1, proxy_host = None, proxy_port = 80, headerscb=None):
       if proxy_host:
          self.has_proxy = True
       else:
          self.has_proxy = False
       self.proxy_host = proxy_host
       self.proxy_port = proxy_port
       self.myurl = url
       self.headerscb = headerscb
       client.HTTPClientFactory.__init__(self, url, method, postdata, headers,
                                         agent, timeout, cookies,
                                         followRedirect)

    def setURL(self, url):
       client.HTTPClientFactory.setURL(self, url)
       if self.has_proxy:
          self.path = url

    def page(self, page):
       encoding = self.response_headers.get("content-encoding")
       if encoding:
          io = StringIO.StringIO(page)
          fp = gzip.GzipFile(fileobj = io)
          page = fp.read()
          fp.close()
       #client.HTTPClientFactory.page(self, page)
       if self.waiting:
          self.waiting=0
          res=page
          if self.uniqueid:
             res=(page, self.uniqueid)
          self.deferred.callback(res)


    def gotHeaders(self, headers):
       if self.headerscb and callable(self.headerscb):
          self.headerscb(headers)
       return client.HTTPClientFactory.gotHeaders(self, headers)


class HTTPClientFactoryProgress(HTTPClientFactory):

   protocol = HTTPPageGetterProgress

   def __init__(self, url, progresscall=False, headerscb=None, *args, **kwargs):
      self.progresscall = progresscall
      HTTPClientFactory.__init__(self, url, headerscb=headerscb, *args, **kwargs)

   def gotHeaders(self, headers):
      if self.status == '200':
         if headers.has_key('content-length'):
            self.totalLength = int(headers['content-length'][0])
         else:
            self.totalLength= 0
         self.currentLength = 0.0
      return HTTPClientFactory.gotHeaders(self, headers)
       
   def pagePart(self, data):
      if self.status=='200':
         self.currentLength += len(data)
         if self.totalLength and int(self.totalLength) > 0:
            percent = "%d/%dK" % (self.currentLength/1000, 
                                 self.totalLength/1000)
            if self.totalLength:
               percent += "- %i%%" % (
                     (self.currentLength/self.totalLength)*100)
         else:
            self.totalLength = 0
         if callable(self.progresscall):
            try:
               if self.uniqueid:
                  self.progresscall(data, self.currentLength, self.totalLength, self.uniqueid)
               else:
                  self.progresscall(data, self.currentLength, self.totalLength)
            except:
               pass
         else:
            print 'PERCENT: ', percent

class HTTPClientFactoryProgressStream(HTTPClientFactoryProgress):

   protocol = HTTPPageGetterProgressStream


def getPage(url, progress=False, stream=False, proxy_host = None, proxy_port = None, headers=None,
            contextFactory = None, uniqueid = False, http_user=None, http_password=None, headerscb=None, *args, **kwargs):

   parsed = urlparse.urlsplit(url)
   if not http_user:
      http_user = parsed.username
   if not http_password:
      http_password = parsed.password

   if parsed.username:
      if parsed.username and not parsed.password:
         url = url.replace(parsed.scheme+"://"+parsed.username+"@", parsed.scheme+"://")
      else:
         url = url.replace(parsed.scheme+"://"+parsed.username+":"+parsed.password+"@", parsed.scheme+"://")
   scheme, host, port, path = _parse(url)

   if not progress:
      factory = HTTPClientFactory(url, proxy_host = proxy_host, proxy_port = proxy_port, headerscb = headerscb, headers = headers,  *args, **kwargs)
   else:
      if stream:
         factory = HTTPClientFactoryProgressStream(url, progresscall = progress,
               proxy_host = proxy_host, proxy_port = proxy_port, headerscb = headerscb, headers = headers, *args, **kwargs)
         if callable(stream):
            factory.pagePart = stream
      else:
         factory = HTTPClientFactoryProgress(url, progresscall = progress, 
               proxy_host = proxy_host, proxy_port = proxy_port, headerscb = headerscb, headers = headers, *args, **kwargs)

   factory.http_user = http_user
   factory.http_password = http_password
   factory.uniqueid=uniqueid

   if scheme == 'https':
      from twisted.internet import ssl
      if contextFactory is None:
         contextFactory = ssl.ClientContextFactory()
      reac = reactor.connectSSL(host, port, factory, contextFactory)
   else:
     if proxy_host:
        if not proxy_port:
           proxy_port = 80
        reac = reactor.connectTCP(proxy_host, proxy_port, factory)
     else:
        reac = reactor.connectTCP(host, port, factory)
   factory.react = reac
   if not stream:
      return factory.deferred
   else:
      return factory, factory.deferred
