from ploader.commands import interface_commands
from ploader.dlc_handler import dlc_to_links

import asyncore, socket, shlex
import select

import ploader.utils as utils


class Client(asyncore.dispatcher_with_send):
	def __init__(self, sock, callback):
		super().__init__(sock)
		self.sock = sock
		self.callback = callback
		self.cur_command = None

		self.command_string = "/".join(interface_commands)

		# send welcome
		self.send(("Welcome (try %s)\n" % self.command_string).encode(encoding='UTF-8'))

	def handle_read(self):
		data = self.recv(8192)
		answ = "I don't know what to do... (try %s)" % self.command_string

		if data:
			inp = data.decode(encoding='UTF-8').rstrip("\n")

			if self.cur_command == None:
				# looking for next command
				if inp in interface_commands.keys():
					self.cur_command = interface_commands[inp]()
			if self.cur_command != None:
				# executing current command
				next_state, info = self.cur_command.execute(inp)

				if next_state == "proceed":
					# go on
					answ = info
				elif next_state == "error":
					# abort current command
					answ = info
					self.cur_command = None
				elif next_state == "return":
					# successfully done with this command
					answ = self.callback({info: self.cur_command.execute(inp)})
					self.cur_command = None

		self.send(("%s\n" % answ).encode(encoding='UTF-8'))

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
		client = Client(sock, self.callback)

	def set_callback(self, callback):
		self.callback = callback