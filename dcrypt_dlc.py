import mechanize, sys, json


if len(sys.argv) != 2:
	print "Usage: %s <dlc url>" % sys.argv[0]
	sys.exit(1)

_url = "http://dcrypt.it/"

br = mechanize.Browser()
response = br.open(_url)

br.form = list(br.forms())[0]
for control in br.form.controls:
  if control.type == "text":
    control.value = sys.argv[1]

response = br.submit()
res = json.loads(response.read())

links = []
if "success" in res.keys():
	print "Links decrypted"
	links = res["success"]["links"][1:]
else:
	print res
