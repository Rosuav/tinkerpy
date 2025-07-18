# To design your own tinkerer, copy this file and change the xfrm function.
# See detailed notes in README.md for more information.
from importlib.machinery import SourceFileLoader, FileFinder
import sys
import tokenize

def xfrm(tok, state):
	"""Given a token, return that token or a transformed version.

	The given state dict will be retained for all transformations of a single
	file, and will be distinct for different files.
	"""
	# Make your changes here
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
