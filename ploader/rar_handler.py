import os.path

import rarfile


rarfile.NEED_COMMENTS = 0
rarfile.UNICODE_COMMENTS = 1
rarfile.PATH_SEP = '/'

class RAR(object):
	def __init__(self, path, passwd=None):
		self._path = path
		try:
			self._file = rarfile.RarFile(self._path)
			self._passwd = passwd
			self._first_volume = True
			self._have_all_files = True
		except rarfile.NeedFirstVolume:
			self._first_volume = False
			self._have_all_files = True
		except FileNotFoundError:
			self._have_all_files = False

	def is_first_vol(self):
		return self._first_volume

	def all_files_present(self):
		return self._have_all_files

	def extract(self):
		self._file.extractall(path=os.path.dirname(self._path), pwd=self._passwd)

	def list_content(self):
		for f in self._file.infolist():
			print(f.filename, f.file_size, f.volume, f.flags)


def is_rar(fn):
	return rarfile.is_rarfile(fn)
