import shlex

from ploader.dlc_handler import dlc_to_links
import ploader.utils as utils


class Command(object):
	def execute(self, data=None):
		# handle data
		pass

class CommandAdd(Command):
	"""Handles the addition of new links
	"""
	def __init__(self):
		self.type = None
		self.name = None
		self.passwd = None
		self.links = []

		self.state = "start"

	def execute(self, data=None):
		"""Handles usage of command, returns (next, answer)
			(next == proceed -> do next step
			next == error -> abort execution
			next == return -> call callback with this argument (special case: hereby answer is type given to callback)
			answer is sent back to user (exception: see next == return))
		"""
		if self.state == "start":
			self.state = "get_options"
			return 'proceed', 'Enter: "<type:links/dlc> <name> [passwd]"'
		elif self.state == "get_options":
			res = self.parse_options(data)
			self.state = "parse_links"
			return 'proceed' if res else 'error', 'Enter one link per line. Terminate with empty line' if res else 'Invalid statement'
		elif self.state == "parse_links":
			res = self.add_links(data)
			if type(res) == type(42):
				return 'proceed', res
			else:
				self.state = "get_obj"
				return 'return', 'download'
		elif self.state == "get_obj":
			"""Attention: returns only one value
			"""
			return self.get_obj()

	def parse_options(self, inp):
		"""Returns true if it received valid input and false otherwise
		"""
		parts = shlex.split(inp)
		if len(parts) < 2 or len(parts) > 3 or (parts[0] != "links" and parts[0] != "dlc"):
			return False

		self.type = parts[0]
		self.name = parts[1]
		self.passwd = parts[2] if len(parts) == 3 else None

		return True

	def add_links(self, inp):
		"""Returns true (evaluating expression) on nonemtpy and false on empty input
		"""
		if len(inp) == 0:
			return False

		parsed_input = utils.clean_links(inp)
		if self.type == "links":
			for link in parsed_input:
				self.links.append(link)
		else: # == dlc
			for link in parsed_input:
				dlc_links = dlc_to_links(link)
				if dlc_links != None:
					self.links.extend(dlc_links)

		return len(parsed_input)

	def get_obj(self):
		"""Returns final object used somewhere else
		"""
		return {
			'type': self.type,
			'name': self.name,
			'passwd': '' if self.passwd == None else self.passwd,
			'links': self.links
		}

class CommandStats(Command):
	def __init__(self):
		self.state = "start"

	def execute(self, data=None):
		if self.state == "start":
			self.state = "get_obj"
			return "return", "status"
		elif self.state == "get_obj":
			return shlex.split(data)


interface_commands = {
	"add": CommandAdd,
	"stats": CommandStats
}