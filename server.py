from commands import web_commands
from dlc_handler import dlc_to_links

import asyncore, socket, shlex
import select


class Client(asyncore.dispatcher_with_send):
	def __init__(self, sock):
		super().__init__(sock)
		self.sock = sock

		self.poll = select.poll()
		self.stream = None

		self.callback = None

		self.reading_links = False
		self.download_obj = {"name": None}

		self.watching_process = False

	def handle_read(self):
		data = self.recv(8192)
		answ = "I don't know what to do... (try add/stats/watch)"
		if data:
			inp = data.decode(encoding='UTF-8').rstrip("\n")

			if self.reading_links:
				# link input mode enabled
				if self.download_obj["name"] == None:
					# setting meta info
					s = shlex.split(inp)
					answ = "Invalid statement"
					if len(s) == 0:
						self.reading_links = False
					else:
						self.download_obj["type"] = s[0]
						if len(s) > 1:
							self.download_obj["name"] = s[1]
							if len(s) == 3:
								self.download_obj["passwd"] = s[2]
							else:
								self.download_obj["passwd"] = ""
							answ = 'Enter one link per line. Terminate with empty line'

							self.download_obj["links"] = []
						else:
							self.reading_links = False
				else:
					# actually adding links
					if len(inp) == 0:
						# terminate link-addition
						self.reading_links = False
						answ = self.callback({"download": self.download_obj})
						self.download_obj = {"name": None}
					else:
						# add given link
						answ = "Thanks"
						if self.download_obj["type"] == "links":
							self.download_obj.setdefault("links", []).append(inp)
						elif self.download_obj["type"] == "dlc":
							dlc_links = dlc_to_links(inp)
							if dlc_links != None:
								self.download_obj.setdefault("links", []).extend(dlc_links)
						else:
							answ = "Invalid link type given"
			elif self.watching_process:
				answ = "Under construction"
				print("Polling")
				for fn, event in self.poll.poll():
					print(fn, event)
				print("Done")
				self.watching_process = False
			else:
				if inp == web_commands["add_links"]:
					answ = 'Enter: "<type:links/dlc> <name> [passwd]"'
					self.reading_links = True
				elif inp == web_commands["status_request"]:
					s = shlex.split(inp)
					answ = self.callback({"status": s[1:]})
				elif inp == web_commands["transmit_stdout_stderr"]:
					if self.stream != None:
						self.watching_process = True
						answ = "Commencing stream"
						self.poll.register(self.stream)
						self.poll.register(self.sock)
					else:
						answ = "No stream set"

		self.send(("%s\n" % answ).encode(encoding='UTF-8'))

	def set_callback(self, callback):
		self.callback = callback

	def set_stream(self, stream):
		self.stream = stream

class Server(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)

		self.callback = None

	def handle_accepted(self, sock, addr):
		print('Incoming connection from %s' % repr(addr))
		client = Client(sock)
		client.set_callback(self.callback)

	def set_callback(self, callback):
		self.callback = callback

#server = Server('localhost', 8080)
#asyncore.loop()
