import json
import os.path

from ploader.download_handler import Download
import ploader.utils as utils


class LinkLoader(object):
	def __init__(self, path):
		self.path = utils.set_file(path)

		self.data = [] # list of Download objects
		self.get_data() # already stores data in self.data

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
		i = 0
		for dw in self.data:
			if index > i:
				if dw.get_status() != "success":
					i += 1
			else:
				if dw.get_status() != "success":
					return dw
				i += 1
		return None

	def __str__(self):
		return "\n".join([str(dw) for dw in (self.data)])