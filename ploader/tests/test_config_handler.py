from unittest import TestCase
import os

from ploader.tests.environment_handler import *

import ploader.utils as utils


class TestExistingConfig(TestCase):
	def setUp(self):
		handle_cwd()

		self.config = './ploader.yaml'
		utils.set_config_path(self.config)

		create_case_config(self.config)

	def tearDown(self):
		os.remove(self.config)

	def test_normal_loading(self):
		settings = utils.load_config()

		self.assertEqual(settings['port'], 42424)
		self.assertEqual(settings['download-dir'], 'somewhere')
		self.assertEqual(settings['captcha-api-key'], 'foo')
		self.assertTrue(settings['multithreading'])

class TestNonexistentConfig(TestCase):
	def setUp(self):
		handle_cwd()

		self.config = 'candybar.ploader'
		utils.set_config_path(self.config)

	def tearDown(self):
		os.remove(self.config)

	def test_default_loading(self):
		settings = utils.load_config()

		self.assertEqual(settings['port'], 50505)
		self.assertEqual(settings['download-dir'], 'downloads')
		self.assertEqual(settings['captcha-api-key'], 'xyz')
		self.assertFalse(settings['multithreading'])