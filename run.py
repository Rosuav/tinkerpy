# Set up the import hook and then import app
from importlib.machinery import SourceFileLoader, FileFinder
import sys

class TestLoader(SourceFileLoader):
	def get_data(self, fn):
		if not fn.endswith(".py"): return super().get_data(fn)
		with open(fn) as f: data = f.read()
		# Make whatever changes you need here
		return data

sys.path_hooks.insert(0, FileFinder.path_hook((TestLoader, [".py"])))
sys.path_importer_cache.clear()

import app
