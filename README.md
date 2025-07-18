TinkerPy
========

A structure for tinkering with syntax proposals.

The goal of this is less to propose a specific syntax, and more to be a
template for ANY syntax proposal. Take a copy of this project, change the
alterations being done, and start playing with the code.

Syntax proposals are MUCH easier to discuss when you can play with them than
when you have to discuss everything abstractly!

How to use
----------

Take a copy of template.py and modify it to your needs. The central function
is xfrm(), which receives a stream of tokens (one at a time) and returns the
token unchanged, or a modified token.

    return tok._replace(...) # Return a token like the original but altered

Create your own test program, and have the modified runner import that instead
of app. Voila! You have a tweaked Python to play with.

TIP: Destroy the `__pycache__` directory every time you make changes. This
will ensure that the latest version of your import hook is in fact running.

Limitations
-----------

As this still uses the original tokenizer, there are a number of limitations.
You cannot create new string prefixes - z"spam" is a name followed by a string,
not a string with an unrecognized prefix. You also cannot fundamentally change
the way that tokens are detected.

With the template as given, only a single token can be returned for any given
token. This could be changed by instead having xfrm() yield zero or more tokens
for each token it is given.
