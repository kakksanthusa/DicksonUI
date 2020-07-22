#!/usr/bin/python
# -*- coding: utf-8 -*-

# - * -coding: utf - 8 - * -

  # #Form.py#

import json
import os


def read_json(request_headers, request_file):
    n_bytes = int(request_headers['content-length'])
    content_bytes = request_file.read(n_bytes)
    content_string = content_bytes.decode('ascii')
    return json.loads(content_string)


class Form:

    def __init__(self):
        self.script = ''
        self.control_counter = 0
        self.event_handlers = {}
        self._name = None
        self.eval_id = 0
        self.eval_list = {}

    @property
    def Name(self):
        return self._name

    @Name.setter
    def Name(self, name):
        self.run('document.title="'+str(name)+'";')
        self._name = name

    def Add(self, control):
        a = control.initialize(str(self.control_counter), self)
        self.run(a + 'document.body.appendChild(Control);')
        self.control_counter += 1
        control.child_handler()

    def eventHandlers(self):

        def append(self, Id, handler):
            self.event_handlers[Id] = handler
            return self.event_handlers

    def EventHandler(self, s):
        data = read_json(s.headers, s.rfile)
        s.send_response(200)
        s.end_headers()
        for event_handler in self.event_handlers:
            if event_handler == data['handler']:
                event_handlers[event_handler](data)

    def RequestHandler(self, s):
        if s.command == 'GET':
            if s.path.endswith('/command'):
                self.CommandHandler(s)
        if s.command == 'POST':
            if s.path.endswith('/event'):
                self.EventHandler(s)
            if s.path.endswith('/data'):
                self.DataHandler(s)

    def evaluate(self, script):
        self.run('sd={};sd.data=' + script + 'sd.target='
                 + str(self.eval_id) + ';notify_data(sd);')
        myid = self.eval_id
        self.eval_id += 1
        self.eval_list[myid] = ''
        while self.eval_list[myid] == '':
            pass
        else:
            rdata = self.eval_list[myid]
            del self.eval_list[myid]
            return rdata

    def run(self, script):
        self.script += script

    def CommandHandler(self, s):
        try:
            while self.script == '':
                pass
            else:
                s.send_response(200)
                s.send_no_cache_headers()
                s.end_headers()
                s.write_bytes(self.script + 'obey_forever();')
                self.script = ''
        except:

            # The client stopped listening while we were waiting.

            pass

    def DataHandler(self, s):
        data = read_json(s.headers, s.rfile)
        s.send_response(200)
        s.end_headers()
        myid = int(data['target'])
        self.eval_list[myid] = data['data']

    def Main(self):
        """ Subclasses of Form class *must* declare a main function"""

        raise NotImplementedError("Forms must implement 'Main()' function."
                                  )
