import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import json

def dlc_to_links(url):
	data = urllib.parse.urlencode({"pro_links": url, "modo_links": "text", "modo_recursivo": "on", "link_cache": "on"})
	data = data.encode('utf-8')
	request = urllib.request.Request("http://linkdecrypter.com/")

	request.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
	request.add_header("cookie", "PHPSESSID=7p88jo0pkaek7vf6qei550ops4")

	f = urllib.request.urlopen(request, data)

	request2 = urllib.request.Request("http://linkdecrypter.com/")
	request2.add_header("cookie", "PHPSESSID=7p88jo0pkaek7vf6qei550ops4")
	f2 = urllib.request.urlopen(request2)

	soup = BeautifulSoup(f2.read().decode('utf-8'))

	textarea = soup.find("textarea", {"class": "caja_des"})

	if textarea != None:
		return textarea.getText().split("\n")
	else:
		return None
