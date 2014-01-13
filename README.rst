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


Links
-----
PyPi Homepage: https://pypi.python.org/pypi/ploader

Travis CI: https://travis-ci.org/kpj/PLoader

AUR: https://aur.archlinux.org/packages/python-ploader-git/
