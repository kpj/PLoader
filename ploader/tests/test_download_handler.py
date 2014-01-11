import unittest
from unittest import TestCase

import os

from ploader.tests.environment_handler import *

from ploader.link_loader import LinkLoader
from ploader.download_handler import Download


@unittest.skip('HTTP servers are mean :-/')
class TestDownloadStateful(TestCase):
	def setUp(self):
		handle_cwd()

		self.port = 9888

		self.httpd = create_http_server(self.port)

		self.filename = 'nonexistent.ploader'
		self.link_loader = LinkLoader(self.filename)

	def tearDown(self):
		self.httpd.shutdown()

		os.remove(self.filename)

	def test_download_unrar_nopw(self):
		self.link_loader.create_download(
			'NoPasswordNeeded',
			['http://localhost:' + str(self.port) + '/NoPasswd.rar']
		)
		dw = self.link_loader.get_unstarted_download()

		# download
		dw.download()

		# unrar
		dw.unpack()

		self.assertCountEqual(os.listdir('downloads/NoPasswordNeeded'), ['NoPasswd.rar', 'happy.file', 'logs'])

	def test_download_unrar_withpw(self):
		self.link_loader.create_download(
			'IndeedPasswordNeeded',
			['http://localhost:' + str(self.port) + '/WithPasswd.rar'],
			'supersecret'
		)
		dw = self.link_loader.get_unstarted_download()

		# download
		dw.download()

		# unrar
		dw.unpack()

		self.assertCountEqual(os.listdir('downloads/IndeedPasswordNeeded'), ['WithPasswd.rar', 'unhappy.file', 'logs'])

class TestDownloadStateless(TestCase):
	def setUp(self):
		handle_cwd()

	def test_get_status(self):
		# incomplete list arguments

		links = [{'status': 'not started'}, {'status': 'not started'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'not started')

		links = [{'status': 'loading'}, {'status': 'not started'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'loading')

		links = [{'status': 'success'}, {'status': 'not started'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'loading')

		links = [{'status': 'loading'}, {'status': 'loading'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'loading')

		links = [{'status': 'success'}, {'status': 'loading'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'loading')

		links = [{'status': 'success'}, {'status': 'success'}]
		dw = Download('foo', links, 'bar')
		self.assertEqual(dw.get_status(), 'success')