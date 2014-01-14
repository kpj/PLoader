PLoader
=======
.. image:: https://api.travis-ci.org/kpj/PLoader.png?branch=master

CLI download manager written in python. It serves as a front-end to plowshare (especially plowdown) which handles the actual download.


Installation
------------
Using pip
+++++++++

  $ pip install ploader
  
Using pacman (archlinux)
++++++++++++++++++++++++

  $ yaourt -S python-ploader-git
  
or

  $ mkdir PLoader && cd PLoader/
  
  $ wget https://raw.github.com/kpj/PLoader/master/aur/PKGBUILD
  
  $ makepkg
  
  $ sudo pacman -U python-ploader-git-*-any.pkg.tar.xz

Usage
-----
Start server on 192.168.2.1, assume it listens on port 50505 (specified in ~/.ploader.conf)

  $ ploader
  
To connect from the same machine, execute

  $ nc localhost 50505
  
or, to connect from a different machine, execute

  $ nc 192.168.2.1 50505
  
A welcome message will show up and display the available commands

Bug Reports
-----------
Please submit any bugs you find to https://github.com/kpj/PLoader/issues.

Links
-----
Github: https://github.com/kpj/PLoader

PyPi Homepage: https://pypi.python.org/pypi/ploader

Travis CI: https://travis-ci.org/kpj/PLoader

AUR: https://aur.archlinux.org/packages/python-ploader-git/
