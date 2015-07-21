Recipe of the Day
=================

A website which shows a new recipe to try out every day.

Licence
-------

This project currently has no licence, which means that it falls under
copyright law.

Provisioning
------------

## Required packages
* nginx
* Git
* Python 3
* pip
* virtualenv
* postgres (9.4 is latest at time of writing)

To get them on Debian:
	sudo apt-get install nginx git python3 python3-pip \
		postgresql-server-dev-9.4
	sudo pip3 install virtualenv

There are two template files in deploy\_tools that currently need editing by
hand. In the future this can be done by running the 'fab provision' command.
Currently you need to replace every instance of SITENAME in the files and
filenames with the domain name of the site

deploy\_tools/nginx.conf.template:
	move to /etc/nginx/sites-available/SITENAME
	update settings in /etc/nginx/sites-available/SITENAME
	make symlink in /etc/nginx/sites-enabled/ to the file


Installing
----------

Installation is handled by Fabric, which only works under Python 2, to install
run:
	sudo pip fabric

Tries to put everything under /var/www/sites/SITENAME/, has the following
subdirectories:
--- SITENAME
	--- source
	--- static
	--- virtualenv
