#!/bin/sh
sudo apt-get update
sudo apt-get install phpmyadmin
sudo echo Include /etc/phpmyadmin/apache.conf >> /etc/apache2/apache2.conf
sudo service apache2 restart

