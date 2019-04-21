#!/bin/sh
# echo "This script must be run interactively, since the installer doesn't use the -y switch on apt."
# echo "Installing Phabricator..."
echo "Installing kanboard"
echo "  (not to be confused with github.com/kiswa/TaskBoard, which is not well maintained and undergoing an AngularJS to Angular 6 rewrite on its re-write branch;"
# echo "(see https://secure.phabricator.com/book/phabricator/article/installation_guide/)"
echo "   installing kanboard.org github.com/kanboard/kanboard--see <https://docs.kanboard.org/en/latest/admin_guide/installation.html>)..."
dest_path=/var/www/html/kanboard
sudo mkdir -p "$dest_path"
if [ ! -d "$dest_path" ]; then echo "ERROR: Nothing done since cannot create '$dest_path'"; fi
sudo chown -R www-data:www-data "$dest_path"
if [ ! -d "$HOME/Download/git" ]; then mkdir -p "$HOME/Download/git"; fi
cd "$HOME/Download/git"
if [ ! -d "$HOME/Download/git/kanboard" ]; then
    git clone https://github.com/kanboard/kanboard.git
else
    cd kanboard
    git pull
    cd ..
fi
if [ -d "$HOME/Download/git/kanboard" ]; then
    sudo -u www-data rsync -rt "$HOME/Download/git/kanboard/" "$dest_path"
else
    echo "ERROR: nothing done since can't create '$HOME/Download/git/kanboard'"
fi
# wget -O install_ubuntu.sh https://p.phcdn.net/file/download/@secure/tuh46upvolxiaz2b63ga/PHID-FILE-k5adrmjuqbjqolgvnfmv/install_ubuntu.sh || exit 1
# cd "$dest_path" || exit 1
# bash ~/install_ubuntu.sh
# above command will echo:
# https://secure.phabricator.com/book/phabricator/article/configuration_guide/
# Next step is "Configuring Apache webserver".
# Why NOT Phabricator: "You can either install Phabricator on a subdomain (like phabricator.example.com) or an entire domain, but you can not install it in some subdirectory of an existing website"

echo "* Check if the directory data is writeable by the web server user"
echo "* With your browser go to http://yourpersonalserver/kanboard"
echo "* The default login and password is admin/admin"
echo "* Don’t forget to change your password!"
