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

    results = {}
    results['unversioned_modules'] = []
    results['versioned_modules'] = []
    results['versions'] = []
    results['other'] = []

    # echo0("All php packages: ({})".format(len(packaged_mod_names)))
    for name in packaged_mod_names:
        # echo0("- "+name)
        parts = split_package_parts(name)
        if len(parts) == 1:
            results['other'].append(name)
        elif len(parts) == 2:
            if parts[0] == "php" and is_decimal(parts[1]):
                results['versions'].append(name)
            else:
                results['unversioned_modules'].append(name)
        else:
            results['versioned_modules'].append(name)

    return results

# See <https://tecadmin.net/switch-between-multiple-php-version-on-debian/>
apache_pre_commands = '''
sudo a2dismod {old_version_names}
sudo a2enmod php{new_version}
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

    return 0


if __name__ == "__main__":
    sys.exit(main())
