from unittest import TestCase

import os, json, shutil

from ploader.tests.environment_handler import *

from ploader.link_loader import LinkLoader
from ploader.download_handler import Download


class TestLinkLoaderNonexistentPloaderFile(TestCase):
	def setUp(self):
		handle_cwd()

		self.filename = 'nonexistent.ploader'

		self.link_loader = LinkLoader(self.filename)

	def tearDown(self):
		os.remove(self.filename)

	def test_local_data_parser(self):
		# on empty file
		self.assertEqual(self.link_loader.data, [])

	def test_append_download(self):
		# TODO: little hack to reduce amount of work
		self.link_loader.append_download(Download('42', []))
		self.assertEqual(len(self.link_loader.data), 1)

		self.link_loader.append_download([Download('42', [])])
		self.assertEqual(len(self.link_loader.data), 2)

		self.link_loader.append_download([Download('23', []), Download('42', [])])
		self.assertEqual(len(self.link_loader.data), 4)

class TestLinkLoaderSpecialPloaderFile(TestCase):
	def setUp(self):
		handle_cwd()

		# sample content
		content = '[{"name": "foo", "links": [{"link": "http://path.to.file/my_file.rar", "status": "success"}], "passwd": "bar"}, {"name": "bla", "links": [{"link": "http://foo.bar.baz/other_stuff.avi", "filename": null, "status": "not started"}, {"link": "http://foo.bar.baz/other_stuff2.avi", "filename": null, "status": "not started"}], "passwd": "blub"}]'
		self.filename = 'special.ploader'
		with open(self.filename, 'w') as fd:
			fd.write(content)

		self.link_loader = LinkLoader(self.filename)

	def tearDown(self):
		os.remove(self.filename)
		shutil.rmtree('downloads')

	def test_get_unstarted_download(self):
		sample_dw = Download(
			'bla',
			[{"link": "http://foo.bar.baz/other_stuff.avi", "filename": "", "status": "not started"}, {"link": "http://foo.bar.baz/other_stuff2.avi", "filename": "", "status": "not started"}],
			'blub'
		)

		# TODO: find better way to compare objects
		self.assertEqual(
			repr(self.link_loader.get_unstarted_download()),
			repr(sample_dw)
		)

class TestLinkLoader(TestCase):
	def setUp(self):
		self.maxDiff = None

		handle_cwd()

		# sample content
		content = '[{"links": [{"status": "not started", "link": "http://path.to.file/my_file.rar"}], "name": "foo", "passwd": "bar"}]'
		self.filename = 'test.ploader'
		with open(self.filename, 'w') as fd:
			fd.write(content)

		self.link_loader = LinkLoader(self.filename)

	def tearDown(self):
		os.remove(self.filename)
		shutil.rmtree('downloads')

	def test_local_data_parser(self):
		# on existing file
		for download in self.link_loader.data:
			self.assertEqual(download.name, 'foo')
			self.assertEqual(download.passwd, 'bar')

			for link in download.links:
				self.assertEqual(link['link'], 'http://path.to.file/my_file.rar')

	def test_create_download(self):
		self.link_loader.create_download('bla', ['http://foo.bar.baz/other_stuff.avi', 'http://foo.bar.baz/other_stuff2.avi'], 'blub')

		download = self.link_loader.data[0]
		self.assertEqual(download.name, 'foo')
		self.assertEqual(download.passwd, 'bar')
		for link in download.links:
			self.assertEqual(link['link'], 'http://path.to.file/my_file.rar')

		download = self.link_loader.data[1]
		self.assertEqual(download.name, 'bla')
		self.assertEqual(download.passwd, 'blub')
		link = download.links[0]
		self.assertEqual(link['link'], 'http://foo.bar.baz/other_stuff.avi')
		link = download.links[1]
		self.assertEqual(link['link'], 'http://foo.bar.baz/other_stuff2.avi')

	def test_link_list_parser(self):
		# must be converted
		link_list = ['http://foo.bar.baz', 'http://www.google.com/']
		links = self.link_loader.parse_link_list(link_list)

		entry = links[0]
		self.assertEqual(entry['link'], 'http://foo.bar.baz')
		self.assertEqual(entry['status'], 'not started')
		self.assertIsNone(entry['filename'])

		entry = links[1]
		self.assertEqual(entry['link'], 'http://www.google.com/')
		self.assertEqual(entry['status'], 'not started')
		self.assertIsNone(entry['filename'])

		# no links available
		link_list = []
		links = self.link_loader.parse_link_list(link_list)

		self.assertEqual(links, [])

		# must not be converted
		link_list = [{'link': 'http://foo.bar.baz', 'status': 'not started', 'filename': None}]
		links = self.link_loader.parse_link_list(link_list)

		self.assertEqual(link_list, links)

	def test_save_data(self):
		self.link_loader.create_download('bla', ['http://foo.bar.baz/other_stuff.avi', 'http://foo.bar.baz/other_stuff2.avi'], 'blub')

		with open(self.filename, 'r') as fd:
			content = json.loads(fd.read())

		self.assertEqual(content, json.loads('[{"name": "foo", "links": [{"link": "http://path.to.file/my_file.rar", "status": "not started"}], "passwd": "bar"}, {"name": "bla", "links": [{"link": "http://foo.bar.baz/other_stuff.avi", "filename": null, "status": "not started"}, {"link": "http://foo.bar.baz/other_stuff2.avi", "filename": null, "status": "not started"}], "passwd": "blub"}]'))