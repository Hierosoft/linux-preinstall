#!/usr/bin/env python3
'''
Discover PHP modules installed on an apt-based GNU/Linux distro.

Script(s) based on this module may eventually be able to replace:
- linux-preinstall/server/optional/php-set-version.nginx.deb.sh
- linux-preinstall/server/optional/php-set-version.apache.ubuntu.sh
'''
from __future__ import print_function
import sys
import os
# See https://stackoverflow.com/a/29444060
apt_help = '''

The apt module could not be imported. First try:
    sudo apt install -y python{}-apt
    # or
    # sudo apt install -y python-apt
'''.format(sys.version_info.major)

'''
try:
    import apt
except ImportError:
    print(apt_help)
    # raise
    sys.exit(1)
# ^ ModuleNotFoundError in Python3 is a subclass of
#   ImportError from 2 and compatible with 2&3
'''
# ^ use get_installed (cross-distro) from linuxpreinstall instead.

from linuxpreinstall import(
    echo0,
    echo1,
    echo2,
    get_installed,
    split_package_parts,
    is_decimal,
    which,
    install_parts,
    remove_parts,
)


def get_php_package_groups():
    '''
    Split packages including the term "php" into named sets. For
    info on dependency managers supported, see get_installed in
    linuxpreinstall.

    Returns:
    A dictionary of lists where each list is a type of php package:
    - 'unversioned_modules' such as php-cgi
    - 'versioned_modules' such as php7.4-cgi
    - 'versions' such as php7.4
    - 'other_versioned' such as libapache2-mod-php7.4
    - 'other' such as 'php'
    '''
    packaged_mod_names = []
    # packaged_names = []
    # cache = apt.Cache()
    # for mypkg in cache:
        # name = mypkg.name
        # if cache[name].is_installed:
        # packaged_names.append(name)
    packaged_names = get_installed()
    # echo0("names:")
    for raw_name in packaged_names:
        name = raw_name.split("/")[0]
        # The rest of the name (using apt command not module) is
        #   something like:
        #   /stable,stable,now 4.4.19+dfsg-2+deb11u1 all [installed,automatic]
        if "php" in name:
            packaged_mod_names.append(name)
            # echo0("- {}".format(name))

    groups = {}
    groups['unversioned_modules'] = []
    groups['versioned_modules'] = []
    groups['versions'] = []
    groups['other'] = []
    groups['other_versioned'] = []

    # echo0("All php packages: ({})".format(len(packaged_mod_names)))
    for name in packaged_mod_names:
        # echo0("- "+name)
        parts = split_package_parts(name)
        if len(parts) == 1:
            groups['other'].append(name)
        elif len(parts) == 2:
            if parts[0] == "libapache2-mod-php" and is_decimal(parts[1]):
                groups['other_versioned'].append(name)
            elif parts[0] == "php" and is_decimal(parts[1]):
                groups['versions'].append(name)
            else:
                groups['unversioned_modules'].append(name)
        else:
            groups['versioned_modules'].append(name)
    for key, group in groups.items():
        group = sorted(group)

    return groups

# See <https://tecadmin.net/switch-between-multiple-php-version-on-debian/>
apache_pre_commands = '''
sudo a2dismod {old_version_names}
sudo a2enmod php{new_version}
sudo a2enmod {new_modules}
sudo service apache2 restart
'''
# ^ old_version_names must be like: php7.4 php5.6

sys_commands = '''
sudo update-alternatives --set php /usr/bin/php{new_version}
sudo update-alternatives --set phar /usr/bin/phar{new_version}
sudo update-alternatives --set phar.phar /usr/bin/phar.phar{new_version}
sudo update-alternatives --set phpize /usr/bin/phpize{new_version}
sudo update-alternatives --set php-config /usr/bin/php-config{new_version}
'''
nginx_post_commands = '''
echo "You should set your website conf files to use php{new_version}-fpm rather than an old version. The remove commands of this script are optional, and should be skipped if some site(s) require an old version of PHP."
sudo systemctl enable php{new_version}-fpm
sudo systemctl restart nginx
if [ ! -e /run/php/php{new_version}-fpm.sock ]; then echo "Error: missing /run/php/php{new_version}-fpm.sock"; fi
'''
# ^ /run/php/php7.4-fpm.sock (or other version) is neither a file nor a directory, and only exists when the service above is running.
# ^ still got 'FastCGI sent in stderr: "PHP message: PHP Fatal error:'
#   '  Uncaught Error: Class \'OCA\DAV\Connector\Sabre\ExceptionLoggerPlugin\''
#   ' not found in /var/www/nextcloud/remote.php:61'
#   so as per <https://github.com/nextcloud/server/issues/5043> install:
#   php7.4-memcache
#   - However, some people said to comment the following, where my
#     config.php uses redis:
#     'memcache.local' => '\\OC\\Memcache\\Redis'
#     'memcache.locking' => '\\OC\\Memcache\\Redis'
#     Therefore, instead of commenting them install:
#     php7.4-redis

sury_commands = '''
# NOTE: As of 2022-10-30, Debian buster only goes up to PHP 7.3, so use sury.
# Get new key and run dist-upgrade as per <https://i-mscp.net/thread/20595-packages-sury-org-new-signing-key/>:
apt-key del 95BD4743
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
apt update
apt-get dist-upgrade -y

'''

# apt on Debian buster says (on trying to install php8.1-json--but
#   not when installing 7.4 [<=7.4 required for Nextcloud 20.0.14]):
json_issue_note = '''
Package php8.1-json is a virtual package provided by:
  php8.1-phpdbg 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
  php8.1-fpm 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
  php8.1-cli 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
  php8.1-cgi 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
  libphp8.1-embed 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
  libapache2-mod-php8.1 8.1.12-1+0~20221028.28+debian10~1.gbpc35f51
You should explicitly select one to install.
'''

def main():
    groups = get_php_package_groups()
    for key, group in groups.items():
        echo0("{}: ({})".format(key, len(group)))
        for mod in group:
            # echo0("- {}".format(split_package_parts(mod)))
            echo0("- {}".format(mod))
    del group
    if len(sys.argv) < 2:
        echo0("Specify a version to get php version switch commands.")
        return 0
    new_version = None
    arg = sys.argv[1]
    # parts = split_package_parts(arg)
    version_parts = []
    # if len(parts) == 2:
    version_parts = arg.split(".") # parts[1].split('.')
    if len(version_parts) == 2:
        if len(version_parts[1].strip()) == 0:
            version_parts = version_parts[:1]
        if len(version_parts[0].strip()) == 0:
            version_parts = version_parts[1:]
    if len(version_parts) != 2:
        echo0("The format of the param must be like: 8.0")
        return 1
    new_version = arg
    # echo0("version_parts: {}".format(version_parts))

    services = []
    if which("apache2") is not None:
        services.append("apache2")
        echo0("apache2={}".format(which("apache2")))
    if which("nginx") is not None:
        services.append("nginx")
        echo0("nginx={}".format(which("nginx")))
    # ^ won't work since only for root (in /usr/sbin/)

    echo0()
    echo0("You must run the following sets of command manually"
          " (can be piped as standard output):")
    echo0()
    #
    # echo0("remove_parts={}".format(remove_parts))
    remove_modules = []
    for name in groups['versioned_modules']:
        parts = split_package_parts(name)
        if len(parts) != 3:
            raise ValueError(
                'len(parts) for versioned_modules must be 3'
                ' such as ["php", "8.0", "fpm"]'
            )
        parts = split_package_parts(name)
        if parts[1] != new_version:
            # Only uninstall packages not for new_version.
            remove_modules.append(name)
    del name
    print(" ".join(remove_parts)+" "+" ".join(remove_modules))
    new_versioned_modules = []

    for name in groups['versioned_modules']:
        parts = split_package_parts(name)
        new_name = parts[0] + new_version
        # if len(parts) > 2:
        new_name += "-" + parts[2]
        if float(new_version) >= 8.0:
            if parts[2] in ["json", "openssl"]:
                # It is a virtual package in php 8.0.
                # See the json_issue_note global.
                continue
        if parts[2] == "libxml":
            print('echo "Warning: You are installing the libxml module. Ensure libxml2 >=2.7.0 is installed as required by Nextcloud if you plan to use Nextcloud."')
        new_versioned_modules.append(new_name)
    install_cmd = " ".join(install_parts)
    del name

    if install_cmd.startswith("apt"):
        print(sury_commands)

    print(install_cmd+" php"+new_version)
    print(install_cmd+" "+" ".join(new_versioned_modules))
    print(install_cmd+" "+" ".join(groups['unversioned_modules']))
    remove_versions = []
    for name in groups['versions']:
        parts = split_package_parts(name)
        if parts[1] != new_version:
            # Only remove php versions other than new_version.
            remove_versions.append(name)
    del name
    if "apache2" in services:
        print(apache_pre_commands.format(
            old_version_names=" ".join(remove_versions),
            new_version=new_version,
            new_modules=" ".join(groups['versioned_modules'])
        ))
    print(sys_commands.format(
        new_version=new_version,
    ))
    if "nginx" in services:
        print(nginx_post_commands.format(
            new_version=new_version,
        ))

    print('echo "Run ./server/nextcloud-checkup.py in linux-preinstall if you are using Nextcloud to ensure required and recommended packages are installed."')
    print('echo "Nextcloud 23 can\'t handle PHP > 8.0"')
    print('echo "Nextcloud 24 is the first major Nextcloud release to work with PHP8.1"')
    echo0("")
    if len(services) < 1:
        echo0("Error: Neither the apache2 nor nginx command was detected."
              " Ensure apache2 or nginx are installed and that you are"
              " running this script as root. Otherwise, run commands"
              " before or after the commands above as necessary to"
              " restart the appropriate service and disable and enable"
              " the modules listed above.")
        exit(1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
