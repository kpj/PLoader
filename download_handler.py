import threading
import subprocess
import os, os.path
import utils
import time


settings = utils.load_settings();

class Download(object):
	def __init__(self, name, link_list, passwd = ""):
		self.name = name
		self.links = link_list
		self.passwd = passwd

		self.dw_dir = utils.set_dir(os.path.join(settings["download-dir"], self.name.replace(" ", "_")))
		self.log_dir = utils.set_dir(os.path.join(self.dw_dir, "logs"))

		self.saver = None

	def __str__(self):
		out = "\n"
		out += "%s (%i) - %s\n" % (self.name, len(self.links), self.passwd)
		for ele in self.links:
			out += "[%s] %s\n" % (ele["status"], ele["link"])
		out += "-> %s\n" % self.dw_dir
		return out

	def set_save_function(self, save_fun):
		self.saver = save_fun

	def get_status(self):
		suc = True
		for ele in self.links:
			if ele["status"] != "success":
				suc = False
		if suc:
			return "success"

		nots = True
		for ele in self.links:
			if ele["status"] != "not started":
				nots = False
		if nots:
			return "not started"

		return "loading"

	def download(self):
		def load():
			for ele in self.links:
				if ele["status"] == "success":
					continue

				link = ele["link"]
				if ele["filename"] == None:
					ele["filename"] = utils.get_filename(link)
				fname = ele["filename"]

				ele["status"] = "loading"

				self.loading = True
				proc = utils.exe(["plowdown", "-o", self.dw_dir, "--9kweu", settings["captcha-api-key"], link])

				poll = proc.poll()
				while poll == None:
					poll = proc.poll()
					print("> \"%s\" => \"%s\" - Loading" % (link, os.path.join(self.dw_dir, fname)))
					print("\033[1A", end="") # moves cursor one row up
					time.sleep(1)
				print("> \"%s\" => \"%s\" - Done ($? = %i)" % (link, os.path.join(self.dw_dir, fname), poll))
				self.loading = False

				if poll != 0:
					utils.write_to_file(os.path.join(self.log_dir, "stdout.log"), proc.stdout.read().decode("utf8"))
					utils.write_to_file(os.path.join(self.log_dir, "stderr.log"), proc.stderr.read().decode("utf8"))
					ele["status"] = "error"
				else:
					ele["status"] = "success"

				self.saver()

#		self.thread = threading.Thread(target = load)
#		self.thread.start()
		load()
