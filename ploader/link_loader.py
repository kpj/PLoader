import json
import os.path
import threading

from ploader.download_handler import Download
import ploader.utils as utils


class LinkLoader(object):
	def __init__(self, path):
		self.path = utils.set_file(path)

		self.data = [] # list of Download objects
		self.get_data() # already stores data in self.data

		self.parallel_download_num = 0

		self.settings = utils.load_config()

	def get_data(self):
		data = []
		if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
			local = json.load(open(self.path, "r"))
			for d in local:
				self.create_download(d["name"], d["links"], d["passwd"])
		return self.data

	def append_download(self, dw):
		if type(dw) == type([]):
			self.data.extend(dw)
		else:
			self.data.append(dw)

		self.save_data()

	def save_data(self):
		obj = []
		for d in self.data:
			obj.append({
				"name": d.name,
				"links": d.links,
				"passwd": d.passwd
			})
		json.dump(obj, open(self.path, "w"))

	def parse_link_list(self, link_list):
		"""Converts simple list of links into appropriate list of containers (if needed)
		"""
		if len(link_list) == 0 or type(link_list[0]) == type({}):
			return link_list

		links = []
		for link in link_list:
			o = {}
			o["link"] = link
			o["status"] = "not started"
			o["filename"] = None
			links.append(o)
		return links

	def create_download(self, name, link_list, passwd=""):
		links = self.parse_link_list(link_list)

		dw = Download(name, links, passwd)
		dw.set_save_function(self.save_data)

		self.append_download(dw)

	def get_unstarted_download(self, index=0):
		def is_qualified(dw):
			return dw.get_status() != "success" and not dw.acquired

		i = 0
		for dw in self.data:
			if index > i:
				if is_qualified(dw):
					i += 1
			else:
				if is_qualified(dw):
					dw.acquired = True
					return dw
				i += 1
		return None

	def try_download(self):
		"""Tries to initiate a download if capacities are left
		"""
		if self.parallel_download_num < self.settings["parallel-download-num"]:
			# allowed to add new download threads
			next_dw = self.get_unstarted_download()
			if next_dw:
				utils.start_thread(next_dw.execute, self.on_download_finish)

				self.parallel_download_num += 1

	def on_download_finish(self):
		"""Callback for download operations
		"""
		self.parallel_download_num -= 1

		# don't forget other downloads
		self.try_download()

	def __str__(self):
		return "\n".join([str(dw) for dw in (self.data)])
