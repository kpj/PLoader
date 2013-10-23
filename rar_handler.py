import os.path

import rarfile


rarfile.NEED_COMMENTS = 0
rarfile.UNICODE_COMMENTS = 1
rarfile.PATH_SEP = '/'

class RAR(object):
	def __init__(self, path, passwd=None):
		self.path = path
		try:
			self.file = rarfile.RarFile(self.path)
			self.passwd = passwd
			self.first_volume = True
		except rarfile.NeedFirstVolume:
			self.first_volume = False

	def extract(self):
		self.file.extractall(path=os.path.dirname(self.path), pwd=self.passwd)

	def list_content(self):
		for f in self.file.infolist():
			print(f.filename, f.file_size, f.volume, f.flags)
