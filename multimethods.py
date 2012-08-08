# -*- coding: utf-8 -*-

''' Multimethods

An implementation of multimethods for Python, heavily influenced by
the Clojure programming language.

Copyright (C) 2010-2012 by Daniel Werner.

See the README file for information on usage and redistribution.
'''


class DefaultMethod(object):
    def __repr__(self):
        return '<DefaultMethod>'

Default = DefaultMethod()


class MultiMethod(object):
    def __init__(self, name, dispatchfn):
        if not callable(dispatchfn):
            raise TypeError('dispatchfn must be callable')

        self.dispatchfn = dispatchfn
        self.methods = {}
        self.name = name

    def __call__(self, *args, **kwds):
        dv = self.dispatchfn(*args, **kwds)

        if dv in self.methods:
            return self.methods[dv](*args, **kwds)

        if Default in self.methods:
            return self.methods[Default](*args, **kwds)

        raise Exception("No matching method on multimethod '%s' and "
                        "no default method defined" % self.name)

    def addmethod(self, func, dispatchval):
        self.methods[dispatchval] = func

    def removemethod(self, dispatchval):
        del self.methods[dispatchval]

    def method(self, dispatchval):
        ''' Decorates a function as a new method of this multimethod, to be
            invoked when the dispatch function returns `dispatchval`.

            The return value is the MultiMethod itself.
        '''

        def method_decorator(func):
            self.addmethod(func, dispatchval)
            # Return the multimethod itself
            return self

        return method_decorator

    def __repr__(self):
        return "<%s '%s'>" % (type(self).__name__, self.name)


__all__ = ['MultiMethod', 'Default']
