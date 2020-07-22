from .fakeattr import fakeattr
from .Control import *
class maincontrol(Control):
    def __init__(self,name):
        self.id=name
        self._hosted = False  # Is added to Form
        self.script = ''  # Javascript code (Used before added to Form)
        self.Controls = []
    def initialize(self, parent):
        self.parent=parent
        self._hosted = True
        self._run = parent._run
        return self.script
    def run(self, message, evaluate=False):
        """This will change script(Javascript) """
        if self._hosted:  # check if control is added to Form
            if evaluate:
                return self._run('document.'+self.id+'.' + message,True)
            else:
                self._run('document.'+self.id+'.' + message)
        else:
            if evaluate:
                raise Exception("Cannot evaluate before run Application.")
            self.script += 'document.'+self.id+'.'
            self.script += message
    def appendChild(self, child):
        if self._hosted:
            self._run(child.initialize(self.parent)+'document.'+self.id+'.'
                                +'appendChild(Control);')
            child.child_handler()
        else:
            self.Controls.append(child)

class document(object):
    def __init__(self):
        self.script=''
        self.body=maincontrol('body')
        self.head=maincontrol('head')
        self.controls_id_index=0

    def initialize(self, parent):
        self.parent=parent
        self._run = parent.run
        self._hosted = True
        self._run(self.body.initialize(self))
        self.body.child_handler()
        self._run(self.head.initialize(self))
        self.head.child_handler()
        
    def __getattr__(self, name):
        d=self.__dict__.get(name)
        if d:
            return d
        return fakeattr(self.run, name)

    def run(self, script, e):
        if self._hosted:
            if e:
                return self._run('document.'+script,e)
            else:
                self._run('document.'+script)
        else:
            if e:
                raise Exception("Cannot evaluate before run Application.")
            else:
                self.script += 'document.'
                self.script += message

    def __setattr__(self, name, attr):
        if name in ['script','body','head','parent','_run','_hosted','controls_id_index']:
            self.__dict__[name]=attr
        else:
            if isinstance(attr,str):
                attr='"'+attr.replace('"','\\'+'"').replace('\'','\\'+'\'').replace('\n','\\'+'n')+'"'
            self.run('document.'+name+'='+str(attr)+';')
    
    def createElement(self, TagName):
        return Control(str(TagName))

    def getElementById(self, Id):
        fake_element=self.createElement('fake')
        fake_element.id=Id
        fake_element.initialize(self)
        return fake_element
    
    def getElementById(self, Id):
        fake_element=self.createElement('fake')
        fake_element.id=Id
        fake_element.initialize(self)
        return fake_element
    
    def register(self,identifier, function):
        self.parent.register(identifier, function)
