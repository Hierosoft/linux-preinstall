#!/bin/sh

# DEPRECATED
# * see git-instaweb in developer.sh instead.

# region even more unecessarily complicated stuff
# see "region local git website without database" instead
## for region nonworking, see instead:
## https://wiki.archlinux.org/index.php/gitweb
#dnf -y install httpd git gitweb
#if [ ! -f /etc/gitweb.conf.1st ]; then
    #if [ -f /etc/gitweb.conf ]; then
        #cp /etc/gitweb.conf /etc/gitweb.conf.1st
    #fi
#fi
#cat > /etc/gitweb.conf <<EOF
#our \$projectroot = "/home/owner/localrepos";
#EOF
#chown -R owner:www-data /home/owner/localrepos
#if [ ! -d /etc/httpd/conf.d/git.conf ]; then
#cat > /etc/httpd/conf.d/git.conf <<EOF
#DocumentRoot /var/www/git
#ServerName git.`hostname`

#Allow from all
#AllowOverride all
#Order allow,deny
#Options ExecCGI

#SetHandler cgi-script

#DirectoryIndex gitweb.cgi
#SetEnv  GITWEB_CONFIG  /etc/gitweb.conf
#EOF
#fi

#cat > /etc/httpd/conf.d/git.conf <<EOF
#Alias /gitweb "/usr/share/gitweb"
#<Directory "/usr/share/gitweb">
    #DirectoryIndex gitweb.cgi
    #Options ExecCGI
    #Require all granted
    #<Files gitweb.cgi>
    #SetHandler cgi-script
    #</Files>
    #SetEnv  GITWEB_CONFIG  /etc/gitweb.conf
#</Directory>
#EOF
#systemctl enable httpd
#systemctl restart httpd


## description is added by make-localhost-git-Bucket_Game.sh
## * then:
##   cd ~/localrepos/*
##   git-instaweb
## * make-localhost-no-network-repo-linux-minetest-kit.sh
# endregion even more unecessarily complicated stuff

# region nonworking
# see "region local git website without database" instead.
# dnf -y install docker docker-compose
# systemctl enable docker
# systemctl start docker

# see https://www.turnkeylinux.org/docs/docker
# dnf -y install mysql
#docker pull gitea/gitea
#docker run -i -t -d gitea/gitea
# if [ ! -d /root/gitea ]; then
#mkdir /root/gitea

#docker_gitea_USER_UID=`id -u g2345098itea`
#docker_gitea_USER_GID=`id -g g2345098itea`
#docker_gitea_DB_TYPE=postgres
#docker_gitea_DB_HOST=db:5432
#docker_gitea_DB_NAME=gi234598457tea
#docker_gitea_DB_USER=g2345098itea
#docker_gitea_DB_PASSWD=got3A123490872394087

# primarily based on <https://docs.gitea.io/en-us/install-with-docker/>,
# secondarily, <https://www.turnkeylinux.org/docs/docker>:
#cat > /root/gitea/inithooks.conf <<EOF
#export USER_UID=$docker_gitea_USER_UID
#export USER_GID=$docker_gitea_USER_GID
#export DB_TYPE=$docker_gitea_DB_TYPE
#export DB_HOST=$docker_gitea_DB_HOST
#export DB_NAME=$docker_gitea_DB_NAME
#export DB_USER=$docker_gitea_DB_USER
#export DB_PASSWD=$docker_gitea_DB_PASSWD
#export APP_EMAIL=owner@localhost
#export APP_DOMAIN=localhost
#export HUB_APIKEY=SKIP
#export SEC_UPDATES=FORCE
#EOF

## based on <https://www.turnkeylinux.org/docs/docker>:
##cat > /root/gitea/inithooks.conf <<EOF
##export ROOT_PASS=secretrootpass
##export DB_PASS=secretmysqlpass
##export APP_PASS=secretadminwppass
##export APP_EMAIL=admin@example.com
##export APP_DOMAIN=www.example.com
##export HUB_APIKEY=SKIP
##export SEC_UPDATES=FORCE
##EOF

##cat > /root/gitea/Dockerfile <<EOF
##FROM gitea/gitea
##ADD inithooks.conf /etc/inithooks.conf
##EOF
##docker build -t gitea /root/gitea
##cd /root
##docker run -i -t -d gitea
##yes | cp -f docker-compose.yml /root/
##cd /root
##docker-compose up -d
##echo "Listing services..."
##docker-compose ps

## The following should work, but some more steps are needed (not turnkey).
## See https://docs.gitea.io/en-us/install-with-docker/
##dnf -y install postgresql
##adduser g2345098itea
##echo got3A123490872394087 | passwd g2345098itea --stdin
##yes | cp -f docker-gitea.sql /tmp/
##chown postgres:postgres /tmp/docker-gitea.sql
##pushd /tmp
##sudo -u postgres psql --file=/tmp/docker-gitea.sql
##popd

# [regarding docker-compose.yml] "To bind the integrated openSSH daemon
# and the webserver on a different port, adjust the port section. It’s
# common to just change the host port and keep the ports within the
# container like they are" (docs.gitea.io).
# fi
#endregion nonworking
