Recipe of the Day (ROTD)
========================

A website which shows a new recipe to try out every day.

Licence
-------

ROTD is currently licensed under the GNU Affero General Public License, version
3. This means that ROTD is free software that you can redistribute and/or
modify it under the terms of the AGPLv3 license.

ROTD is distributed in the hope that it will be useful, but WITHOUT ANY
WARANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See The GNU Affero General Public License for more details.

A full copy of the licence can be found in the COPYING file. If not, see
<http://www.gnu.org/licenses/>

### Contributors
Xeryus Stokkel (contact <at> xeryus <dot> nl)


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
```
sudo apt-get install nginx git python3 python3-pip postgresql-server-dev-9.4
sudo pip3 install virtualenv
```
These commands are also run by the `fab requirements` command. Provisioning
itself is done through the `fab provision` command. This will not only
configure the website but also deploy the source code and start the relevant
services.

Installing
----------

Installation is handled by Fabric, which only works under Python 2, to install
run:
```
sudo pip fabric
```

The `fab provision` command deploys the website and starts the relevant
services. It puts everything under /var/www/sites/SITENAME/, which has the
following subdirectories:
```
--- SITENAME
	--- source
	--- static
	--- virtualenv
```

Updating
--------

Updating the website is done through the `fab deploy` and
`fab update_settings` commands. The deploy command updates the code on the
server but it doesn't restart services, this needs to be manually by running:
`sudo systemctl service gunicorn-SITENAME restart` where SITENAME needs to be
replaced by the domain of the website.

The `fab update_settings` command updates the EnvironmentFile that holds all
the settings for the website. Currently, when additional settings are added
you will need to re-enter all the settings.

Adding settings
---------------
When adding settings that have to be configured through the EnvironmentFile
then fabfile.py needs to be updated so that it also knows about the new
setting. There are three places that need updating:
* `settings_map` in `_settings_prompt()` needs to have an extra tuple
  containing the fabric env variable and the EnvironmentFile variable.
* A prompt for the setting needs to be added to `_settings_prompt()`.
* `_deploy_settings_file()` needs an extra 'sed' command to replace the new
  variable in the EnvironmentFile.
