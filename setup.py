from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(name='ploader',
	version='0.4',
	description='a pure cli-based download manager',
	long_description=readme(),
	url='https://github.com/kpj/PLoader',
	author='kpj',
	author_email='kpjkpjkpjkpjkpjkpj@gmail.com',
	license='MIT',
	packages=['ploader'],
	zip_safe=False,
	test_suite='nose.collector',
	tests_require=['nose'],
	scripts=['bin/ploader'],
)
