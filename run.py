# Set up the import hook and then import app
from importlib.machinery import SourceFileLoader, FileFinder
import sys
import tokenize
from compose import charmap

def xfrm(tok, state):
	"""Given a token, return that token or a transformed version.

	The given state dict will be retained for all transformations of a single
	file, and will be distinct for different files.
	"""
	if tok.type == tokenize.STRING:
		if "\\[" in tok.string:
			was, now = tok.string, ""
			while was:
				before, delim, after = was.partition("\\[")
				now += before
				if not delim: break
				char, delim, was = after.partition("]")
				if not delim: raise SyntaxError("Unterminated \\[...] character escape")
				# Since it's otherwise impossible to include the string delimiter inside an escape,
				# provide some rudimentary backslash parsing.
				if "\\" in char:
					steps = iter(char)
					char = ""
					for c in steps:
						if c == "\\":
							c = next(steps)
							if c not in "\\\"'": 
								raise SyntaxError("Unrecognized backslash escape \\%s" % c)
							# The only supported backslash escapes inside \[...] are themselves,
							# ie "\[a\"]" is the same as '\[a"]' as if the backslash were not there.
						char += c
				try: now += charmap[char]
				except LookupError: raise SyntaxError("Unrecognized character escape \\[%s]" % char) from None
			return tok._replace(string=now)
	return tok

class TestLoader(SourceFileLoader):
	def get_data(self, fn):
		if not fn.endswith(".py"): return super().get_data(fn)
		with open(fn) as f:
			state = {}
			return tokenize.untokenize(xfrm(tok, state) for tok in tokenize.generate_tokens(f.readline))

sys.path_hooks.insert(0, FileFinder.path_hook((TestLoader, [".py"])))
sys.path_importer_cache.clear()

import app
