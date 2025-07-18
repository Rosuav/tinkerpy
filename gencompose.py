# Parse a Compose sequence file and generate a dictionary of tokens
# If this were actually a proposal for Python, there would need to be a concrete
# list that is supported on all platform identically, but for now I'm just lifting
# from the one on my Debian X11 en_US setup.

# First, parse the X11 keysymdefs. If this file doesn't exist on your system, try
# installing the source/dev package for X11 (on Debian/Ubuntu, that's x11proto-core-dev)
# or searching include file paths elsewhere.
import re
keys = {}
with open("/usr/include/X11/keysymdef.h") as f:
	for line in f:
		# Note: The regex here is lifted from keysymdef.h itself (there are three
		# regexen listed but they only differ *after* the part we care about).
		m = re.match(r"^^\#define XK_([a-zA-Z_0-9]+)\s+0x([0-9a-f]+)", line)
		if not m: continue
		if m.group(2) == "ffffff": continue # Ignore the VoidSymbol, which isn't a valid character
		keysym = int(m.group(2), 16)
		if keysym > 0x01000000: keysym -= 0x01000000
		# If it is lower, the keysym may represent a character, but also may not.
		# We assume that the ones that aren't valid characters won't be used in a
		# Compose sequence, so it's fine to have them show up here. For example,
		# XK_Page_Down is 0xff56; if you had a sequence <Multi_key> <Page_Down> <Q>
		# to create a character, we would accept "\[\uff56Q]" to create that. But
		# that seems unlikely ever to be an issue in practice.
		keys["<" + m.group(1) + ">"] = chr(keysym)

def generate(source, target):
	with open(source) as src, open(target, "w") as targ:
		print("# Generated from", source, "via gencompose.py", file=targ)
		print("# Do not edit manually.", file=targ)
		print("charmap = {", file=targ)
		for line in src:
			line = line.strip()
			if not line: continue
			events, colon, result = line.partition(":")
			if not colon: continue
			events = events.split()
			if events[0] != "<Multi_key>": continue # Only parse the ones that start with Compose (not dead key sequences)
			try:
				seq = "".join(keys[event] for event in events[1:])
			except LookupError:
				# print("Unrecognized key seq", events)
				# A bunch of sequences include other sequences, identified by Unicode codepoint.
				# Leave them out I guess?
				continue
			# The result may consist of a string, a key sequence, or both
			# We only want the string. Note that there may be a commen after the
			# result, but there might also be a hash in the quoted portion.
			if m := re.match('^[^#]*("[^"]+")', result):
				print("\t%r: %s," % (seq, m.group(1)), file=targ)
		print("}", file=targ)

generate("/usr/share/X11/locale/en_US.UTF-8/Compose", "compose.py")
