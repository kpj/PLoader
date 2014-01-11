import http.server, threading, socketserver
import os


def create_config():
	conf_cont = """
download-dir: downloads
captcha-api-key: xyz
port: 50505"""
	with open('config.yaml', 'w') as fd:
		fd.write(conf_cont)

def create_http_server(port):
	httpd = socketserver.TCPServer(("0.0.0.0", port), http.server.SimpleHTTPRequestHandler)
	thread = threading.Thread(target = httpd.serve_forever)
	thread.daemon = True
	thread.start()
	return httpd

def handle_cwd(path='ploader/tests/cwd'):
	# looks like a workaround, is ...errr... a suitable solution...
	# background: this function is called many times, but I only want to go here if necessary
	try:
		os.chdir(path)
	except FileNotFoundError:
		pass