Recipe of the Day
=================

A website which shows a new recipe to try out every day.

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
