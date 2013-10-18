import pickle, inspect, json
import os.path

from download_handler import Download
import utils


class LinkLoader(object):
	def __init__(self, path):
		self.path = utils.set_file(path)

		self.data = self.get_data()

	def get_data(self):
#		if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
#			return pickle.load(open(self.path, "rb"))
#		else:
#			return []
		data = []
		if os.path.isfile(self.path) and os.path.getsize(self.path) > 0:
			local = json.load(open(self.path, "r"))
			for d in local:
				dw = Download(d["name"], d["links"], d["passwd"])
				dw.set_save_function = self.save_data
				data.append(dw)
		return data

	def append_download(self, dw):
		if type([]) == type(dw):
			self.data.extend(dw)
		else:
			self.data.append(dw)

		self.save_data()

	def save_data(self):
#		pickle.dump(self.data, open(self.path, "wb"))
		obj = []
		for d in self.data:
			obj.append({
				"name": d.name,
				"links": d.links,
				"passwd": d.passwd
			})
		json.dump(obj, open(self.path, "w"))

	def create_download(self, name, link_list, passwd = ""):
		links = []
		for link in link_list:
			o = {}
			o["link"] = link
			o["status"] = "not started"
			o["filename"] = None
			links.append(o)
		dw = Download(name, links, passwd)
		dw.set_save_function(self.save_data)
		self.append_download(dw)

	def get_unstarted_download(self, index):
		i = 0
		for dw in self.data:
			if index > i:
				if dw.get_status() == "not started":
					i += 1
			else:
				if dw.get_status() == "not started":
					return dw
				i += 1
		return None

	def __str__(self):
		return "\n".join([str(dw) for dw in (self.data)])
