import subprocess, os, os.path, yaml, shlex, re, urllib.parse, shutil, urllib.request


def exe(cmd):
	if type(cmd) != type([]):
		cmd = shlex.split(cmd)
	return subprocess.Popen(cmd)
def exe_pipes(cmd):
	if type(cmd) != type([]):
		cmd = shlex.split(cmd)
	return subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
def exe_flos(cmd, fout, ferr):
	if type(cmd) != type([]):
		cmd = shlex.split(cmd)
	out = open(fout, "w") #io.StringIO()
	err = open(ferr, "w") #io.StringIO()
	return subprocess.Popen(cmd, stdout = out, stderr = err), out, err

def dw_file_to(url, path, callback):
	"""Saves file from url to path
	"""
	#with urllib.request.urlopen(url) as response, open(path, 'wb') as out_file:
	#	shutil.copyfileobj(response, out_file)
	urllib.request.urlretrieve(url, path, callback)

def set_dir(directory, create=True):
	if os.path.isdir(directory):
		return directory
	else:
		if create:
			os.makedirs(directory)
			return directory
		else:
			raise Exception("Tried to assign invalid directory: \"%s\"" % directory)

def set_file(f, create=True):
	if os.path.isfile(f):
		return f
	else:
		if create:
			open(f, 'wb').close()
			return f
		else:
			Exception("Tried to assign invalid file: \"%s\"" % f)

def write_to_file(path, content):
	fd = open(path, "w")
	fd.write(content)
	fd.close()

def get_filename(link):
	(stdout, stderr) = exe_pipes(["plowprobe", link]).communicate()
	if len(stdout) > 2:
		return stdout.decode("utf8").split("\n")[0][2:]
	return "unknown"

def load_settings():
	config = "config.yaml"
	if os.path.isfile(config):
		return yaml.load(open(config, "r"))
	else:
		basic_conf = """download-dir: downloads
captcha-api-key: xyz
port: 50505"""
		fd = open(config, "w")
		fd.write(basic_conf)
		fd.close()
		raise Exception("No config file present, created one for you :-)")

def clean_links(raw_data):
	return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_data)

def url_to_filename(url):
	res = urllib.parse.urlparse(url)
	return os.path.basename(res.path)

def sizeof_fmt(num):
    for x in ['bytes','KB','MB','GB']:
        if num < 1024.0:
            return "%3.1f%s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')