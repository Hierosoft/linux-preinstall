#!/bin/sh
echo "This script assumes that www-data is a supplimentary group of the apache user, such as on Ubuntu"
#sudo usermod -g www-data ftpuser
sudo usermod -a -G www-data ftpuser
sudo usermod -a -G www-data owner
sudo chown -R ftpuser /var/www/html
sudo chgrp -R www-data /var/www/html
sudo chmod -R g+w /var/www/html
echo "The following users are in the www-data group (you should see your username and ftpuser below):"
grep www-data /etc/group
#-G is (--groups)
#lowercase -g (--gid) and no -a (--append)

