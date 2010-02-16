# -*- coding: utf-8 -*-

''' Multimethods

A multimethod implementation for Python, inspired by Clojure's multimethod
support. Thanks to Rich Hickey for proving how useful they are. :-)

Example:

from multimethods import MultiMethod, method, Default

>>> def sign_dispatch(x, y):
        if y > 0: return 1
        elif y == 0: return 0
        return 'bar'

>>> sign = MultiMethod('sign', sign_dispatch)

>>> @method(1)
    def sign__pos(x, y):
    print "y was positive"

>>> @method(0)
    def sign__zero(x, y):
        print "y was zero"

>>> @method(Default)
    def sign__def(x, y):
        print "y was something else"

>>> sign(1, 1)
y was positive

>>> sign(1, 99)
y was positive

>>> sign(1, 0)
y was zero

>>> sign(1, -12)
y was something else

>>> sign('foo', None)
y was something else
'''

__author__ = 'Daniel Werner'

from decorator import decorator

class DefaultMethod(object):
    def __repr__(self):
        return '<DefaultMethod>'


Default = DefaultMethod()

class MultiMethod(object):
    instances = {}

    def __init__(self, name, dispatchfn):
        if not callable(dispatchfn):
            raise TypeError('dispatchfn must be callable')

        if name in self.__class__.instances:
            raise Exception("Multimethod named %s already exists, "
                            "redeclaring it would wreak havoc" % name)

        self.dispatchfn = dispatchfn
        self.methods = {}
        self.__name__ = name
        self.__class__.instances[name] = self

    def __call__(self, *args, **kwds):
        dv = self.dispatchfn(*args, **kwds)

        if dv in self.methods:
            return self.methods[dv](*args, **kwds)

        if Default in self.methods:
            return self.methods[Default](*args, **kwds)

        raise ValueError("No matching method on %s and no default "
                         "method defined" % self.__name__)

    def addmethod(self, func, dispatchval):
        self.methods[dispatchval] = func
        func.multimethod = self

    def getmethod(self, dispatchval):
        return self.methods[dispatchval]

    def removemethod(self, dispatchval):
        del self.methods[dispatchval].multimethod
        del self.methods[dispatchval]

    def methods(self):
        return self.methods

    def __repr__(self):
        return "<MultiMethod '%s'>" % self.__name__


def method(dispatchval):
    def method_decorator(func):
        '''Decorator which registers a function as a new method of a like-named multimethod,
        keyed by dispatchval.

        The multimethod is determined by taking the method's name up to the last occurence
        of '__', e.g. function foo_bar__zig will become a method on the foo_bar multimethod.'''

        if '__' not in func.__name__:
            raise ValueError("Method name must contain '__' to separate multimethod name from suffix")

        mm_name = func.__name__.rsplit('__', 1)[0]
        try:
            multim = MultiMethod.instances[mm_name]
        except KeyError:
            raise KeyError("Multimethod '%s' not found; it must exist before methods can be added")

        multim.addmethod(func, dispatchval)

        return func

    return method_decorator

__all__ = ['MultiMethod', 'method', 'Default']
