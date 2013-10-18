from commands import web_commands

import asyncore, shlex


class Client(asyncore.dispatcher_with_send):
	def __init__(self, sock):
		super().__init__(sock)

		self.callback = None

		self.reading_links = False
		self.download_obj = {"name": None}

	def handle_read(self):
		data = self.recv(8192)
		answ = "I don't know what to do..."
		if data:
			inp = data.decode(encoding='UTF-8').rstrip("\n")

			if self.reading_links:
				if self.download_obj["name"] == None:
#					print("Assuming name/password")
					s = shlex.split(inp)
					if len(s) == 0:
						answ = "Invalid statement"
						self.reading_links = False
					else:
						self.download_obj["name"] = s[0]
						if len(s) == 2:
							self.download_obj["passwd"] = s[1]
						else:
							self.download_obj["passwd"] = ""
						answ = 'Enter one link per line. Terminate with empty line'
				else:
					if len(inp) == 0:
#						print("Adding input")
						self.reading_links = False
						answ = self.callback({"download": self.download_obj})
						self.download_obj = {"name": None}
					else:
#						print("Assuming link")
						self.download_obj.setdefault("links", []).append(inp)
						answ = "Thanks"
			else:
				if inp == web_commands["add_links"]:
					answ = 'Enter: "<name> [passwd]"'
					self.reading_links = True
				elif inp == web_commands["status_request"]:
					s = shlex.split(inp)
					answ = self.callback({"status": s[1:]})

		self.send(("%s\n" % answ).encode(encoding='UTF-8'))

	def set_callback(self, callback):
		self.callback = callback

class Server(asyncore.dispatcher):
	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket()
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
