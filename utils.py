import subprocess, os, yaml


def exe(cmd):
	if type(cmd) != type([]):
		cmd = shlex.split(cmd)
	return subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)

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
	(stdout, stderr) = exe(["plowprobe", link]).communicate()
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
port: 8080"""
		fd = open(config, "w")
		fd.write(basic_conf)
		fd.close()
		raise Exception("No config file present, created one for you :-)")
