#!/usr/bin/python
# -*- coding: utf-8 -*-
from signalpy import *
import signalpy.jslib
import os
package_dir = os.path.dirname(__file__)

__all__=['Application']

class Application():
    '''
    DicksonUI Application 
    handle all windows and Extentions
    eg:
    |    app=Application()
    '''
    def __init__(self, address=('',None)):
        self._forms = []
        self._counter = 0
        self.Icon = b'DicksonUI'
        self.app=app
        self.Hub=Hub
        self.server=Server(address)
        self.server.serve_forever()
        self.location =self.server.base_environ.get('SERVER_NAME')+self.server.base_environ.get('SERVER_PORT')
        app.routes['/']=self.mainhandler
        app.routes['/favicon.ico']=self.faviconhandler
        app.routes['/DicksonUI.js']=self.jslibhandler

    def mainhandler(self, environ, start_response):
        fn = self._forms[0].Name
        start_response('302 Object moved temporarily -- see URI list', [('Location', fn)])
        res=self.location + '/' + fn
        return res.encode()

    def faviconhandler(self, environ, start_response):
        start_response('200 OK', [])
        return[self.Icon]

    def jslibhandler(self, environ, start_response):
        path = os.path.join(package_dir, 'DicksonUI.js')
        start_response('200 OK', [])
        return[signalpy.jslib.data.encode()+open(path, mode='rb').read()]

    def add(self, bom):
        if bom.Name == None:
            self._counter += 1
            bom.Name='Window' + str(self._counter)
            self._forms.append(bom)
            bom.initialize(self)
        else:
            self._forms.append(bom)
            bom.initialize(self)

    def stop(self):
        self.server.shutdown()
        self.server.socket.close()
        self.server = None
        self=None

