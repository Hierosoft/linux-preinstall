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
sudo systemctl restart nginx
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
    echo0()
    echo0("You must run the following sets of command manually"
          " (can be piped as standard output):")
    echo0()
    services = []
    if which("apache2") is not None:
        services.append("apache2")
        echo0("apache2={}".format(which("apache2")))
    if which("nginx") is not None:
        services.append("nginx")
        echo0("nginx={}".format(which("nginx")))
    # ^ won't work since only for root (in /usr/sbin/)
    #
    # echo0("remove_parts={}".format(remove_parts))
    print(" ".join(remove_parts)+" "+" ".join(groups['versioned_modules']))
    new_versioned_modules = []
    for name in groups['versioned_modules']:
        parts = split_package_parts(name)
        if len(parts) != 3:
            raise ValueError(
                'len(parts) for versioned_modules must be 3'
                ' such as ["php", "8.0", "fpm"]'
            )
        new_name = parts[0] + new_version
        # if len(parts) > 2:
        new_name += "-" + parts[2]
        new_versioned_modules.append(new_name)
    install_cmd = " ".join(install_parts)
    print(install_cmd+" php"+new_version)
    print(install_cmd+" "+" ".join(new_versioned_modules))
    if "apache2" in services:
        print(apache_pre_commands.format(
            old_version_names=" ".join(groups['versions']),
            new_version=new_version,
            new_modules=" ".join(groups['versioned_modules'])
        ))
    print(sys_commands.format(
        new_version=new_version,
    ))
    if "nginx" in services:
        print(nginx_post_commands)


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
