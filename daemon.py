from link_loader import LinkLoader
from server import Server
from commands import web_commands
import utils

import asyncore, threading, time


def main():
	settings = utils.load_settings()

	link_handler = LinkLoader("link_list.ploader")

	def handle_net_input(data):
		answ = "Thank you"

#		print("Received: " + str(data))
		if "download" in data.keys():
			cur = data["download"]
			link_handler.create_download(cur["name"], cur["links"], cur["passwd"])
			answ = "Added links"
		if "status" in data.keys():
			cur = data["status"]
			answ = str(link_handler)

		return answ

	server = Server('0.0.0.0', settings["port"])
	server.set_callback(handle_net_input)

	server = threading.Thread(target = asyncore.loop)
	server.start()
	print("Server running")

	while True:
		next_dw = link_handler.get_unstarted_download(0)
		if next_dw != None:
			next_dw.download()
			next_dw.unpack()
		else:
			time.sleep(10)


if __name__ == "__main__":
	main()
