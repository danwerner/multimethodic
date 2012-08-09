multimethodic - Multimethods for Python
======================================

This module adds multimethod support to the Python programming language. In
contrast to other multiple dispatch implementations, this one doesn't strictly
dispatch on argument types, but on a user-provided dispatch function that can
differ for each multimethod. This design is inspired the Clojure programming
language's multimethod implementation.


What are multimethods?
----------------------

Multimethods provide a mechanism to dispatch function execution to different
implementations of this function. It works similarly to the well-known concept
of "instance methods" in OO languages like Python, which in a call to
obj.method() would look up a member called "method" in obj's class.

However, multimethod methods are NOT neccessarily associated with a single
class. Instead, they belong to a `MultiMethod` instance. Calls on the MultiMethod
will be dispatched to its corresponding methods using a custom, user-defined
dispatch function.

The dispatch function can be any callable. Once a MultiMethod is called, the
dispatch function will receive the exact arguments the MultiMethod call
received, and is expected to return a value that will be dispatched on. This
return value is then used to select a 'method', which is basically just
a function that has been associated with this multimethod and dispatch value
using the multimethod's `@method` decorator.

Note that in the dispatch function lies the real power of this whole concept.
For example, you can use it to dispatch on the type of the arguments like in
Java/C, on their exact values, or whether they evaluate to True in a boolean
context. If the arguments are dictionaries, you can dispatch on whether they
contain certain keys. Or, if you want to go really wild, you could even send
these arguments over the network to a remote service and let that decide which
method to call.

Of course, not every possible application of multimethods is actually useful,
but your creativity is the only limit to what you can do.


How to use multimethods
-----------------------

To use multimethods, a `MultiMethod` instance must be created first. Each
MultiMethod instance takes a name and a dispatch function, as discussed above.

Methods are associated with MultiMethods by decorating a function using the
`@method` decorator, which is an attribute of the multimethod itself. This
decorator registers the function for a dispatch value so that whenever the
MultiMethod is called and its dispatch function returns this value, the
decorated function will be selected.

Okay, that was dry enough. Let's put this concept to work with a small example:


Example: Dispatch on Argument Type
----------------------------------

Without multimethods, naively implementing a function that has two different
behaviours based on a the types of the arguments could look like this::

  def combine(x, y):
      if isinstance(x, int) and isinstance(y, int):
          return x * y
      elif isinstance(x, basestring) and isinstance(y, basestring):
          return x + '&' + y
      else:
          return '???'

However, this is ugly and becomes unwieldy fast as we add more elif cases for
additional types. Fortunately, implementing dispatch on function arguments'
types is easy using multimethodic. Let's implement a multimethod version of
`combine()` with exactly the same signature.

First, we have to define a dispatch function. It will take the same arguments
as the multimethod, and return a value which is then used to select the correct
method implementation::

    def dispatch_combine(x, y):
        return (type(x), type(y))

Thus, we are going to dispatch on a tuple of types, namely the types of our
arguments. The next step is to instantiate the MultiMethod itself::

    from multimethodic import MultiMethod, Default
    
    combine = MultiMethod('combine', dispatch_combine)

A multimethod by itself does almost nothing. It is dependent on being given
methods in order to implement its functionality for different dispatch values.
Let's define methods for all-integer and all-string cases as above::

    @combine.method((int, int))
    def combine(x, y):
        return x * y
    
    @combine.method((str, str))
    def combine(x, y):
        return x + '&' + y
    
    @combine.method(Default)
    def combine(x, y):
        return '???'

The behaviour for ints and strings is straightforward::

    >>> combine(21, 2)
    42
    >>> combine('foo', 'bar')
    'foo&bar'

However, notice the last method definition above. Instead of specifying a tuple
of types, we have given it the special `multimethodic.Default` object. This is
a marker which simply tells the multimethod: "In case we don't have a method
implementation for some dispatch value, just use this method instead." Let's
test it::

  >>> combine(21, 'bar')
  '???'

Default methods are completely optional, you are free not to provide one at
all. An `Exception` will be raised for unknown dispatch values instead.

Now would be a good time to show that the dispatch function's signature doesn't
have to match its methods' signature bit-by-bit. Let's make the dispatch
function more generic::

    def dispatch_on_arg_type(*args):
        return tuple(type(x) for x in args)

This version will support all possible (non-variadic, non-keyword) signatures
at no additional cost, and makes it easy to re-use the dispatch function for
other multimethods with different numbers of arguments.


Caveat
******

A small stumbling block remains when dispatching on argument type: Comparing
dispatch values is done via `==`, not via `isinstance()`. This is best explained
using the string-concatenating `combine()` implementation from above::

    @combine.method((basestring, basestring))
    def combine(x, y):
        return x + '&' + y
    
    combine('foo', 'bar')   # BREAKS!

This fails because `type('foo')` returns `str`, not `basestring`. I haven't yet
found a way to allow this to work, short of checking all dispatch values for
`isinstance`-ness in linear time or adding special cases to the code. If you have
an idea how to implement this, great -- please contact me or, better yet, send a
pull request :-)

At any rate, dispatching on argument type is not the end of the story.


Example: Poor man's pattern matching
------------------------------------

What follows is a horribly inefficient algorithm to determine a list's length.
It is often used as an example to teach basic recursion, and also shows how edge
cases can be modeled using simple pattern matching.

::

    from multimethodic import MultiMethod, method, Default

    identity = lambda x: x
    len2 = MultiMethod('len2', identity)

    @len2.method([])
    def len2(l):
        return 0

    @len2.method(Default)
    def len2(l):
        return 1 + len2(l[1:])


Example: Special procedures for special customers
-------------------------------------------------

Here's a slightly more involved example. Let's say ACME Corporation has
standard billing procedures that apply to most of its customers, but some of
the bigger customers receive wildly different conditions. How do we express
this in code without resorting to heaps of `if` statements?

::

    from multimethodic import MultiMethod, method, Default

    def sum_amounts(purchase):
        return sum(product.price for product in purchase)

    def get_customer(purchase):
        return purchase.customer.company_name

    calc_total = MultiMethod('calc_total', get_customer)
    method = calc_total.method

    @method(Default)
    def calc_total(purchase):
        # Normal customer pricing
        return sum_amounts(purchase)

    @method("Wile E.")
    def calc_total(purchase):
        # Always gets 20% off
        return sum_amounts(purchase) * 0.8

    @method("Wolfram & Hart")
    def calc_total(purchase):
        # Has already paid an annual flat fee in advance; also receives
        # a token of enduring friendship with every order
        purchase.append(champagne)
        return 0.0


Author & License
----------------

This work has been created by and is copyrighted by Daniel Werner. All rights
reserved, and that kind of stuff. You may freely use this work under the terms
of the simplified (2-clause) version of the BSD license, a copy of which is
included in this distribution.


Credits & Thanks
----------------

While this Python module is new, the idea of multimethods is definitely not.
Common Lisp has its generic functions, which only dispatch on type (and eql).
There has also been a prior Python implementation by Guido van Rossum, which is
even more limited.

This module however is really a near-faithful implementation of multimethods as
found in the Clojure programming language (http://clojure.org), sans beautiful
macro-based syntax. I'd like to give credit to the principal author of
Clojure, Rich Hickey, for coming up with the idea to generalize multimethods to
use a custom dispatch function, and for publishing his implementation for the
world to use (and port to different languages). Thanks, Rich!

Thanks to Matthew von Rocketstein for providing me with a setup.py, and to Eric
Shull for raising the issue of proper namespacing and implementing a solution.
