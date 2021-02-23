#!/usr/bin/env python3
import os
import sys
import subprocess
#os.system("php -m > /tmp/php-m.txt")
requested_ver = None
if len(sys.argv) < 2:
    requested_ver = os.environ.get("requested_ver")
    if requested_ver is None:
        print("You must specify a php version such as 7.3.")
        exit(1)
    else:
        print("Using requested_ver from environment: {}"
              "".format(requested_ver))
else:
    requested_ver = sys.argv[1]
php_modules = []
phpX_modules = []

oc_requires = ['phpX.X-cli', 'phpX.X-common', 'phpX.X-mbstring',
               'phpX.X-gd', 'php-imagick', 'phpX.X-intl', 'phpX.X-bz2',
               'phpX.X-xml', 'phpX.X-mysql', 'phpX.X-zip',
               'phpX.X-dev', 'phpX.X-curl', 'phpX.X-fpm',
               'php-dompdf', 'php-apcu', 'redis-server',
               'php-redis', 'php-smbclient', 'phpX.X-ldap']
# ^ as per Vincent_Stans on <https://help.nextcloud.com/t/
# upgrade-to-18-01-and-php-7-3-has-broken-installation/71913>
oc_mods = {}
for i in range(len(oc_requires)):
    v = oc_requires[i]
    parts = v.split("-")
    v = v.replace("X.X", requested_ver)
    oc_requires[i] = v
    if len(parts) == 2:
        oc_mods[parts[1]] = False  # oc_requires[i]
    else:
        # print("got plain requirement: {}".format(parts))
        oc_mods[v] = False  # oc_mods[v]

print("Nextcloud requires: {}".format(oc_mods.keys()))

def parse_modules(proc):
    ret = []
    for line_original in proc.stdout.readlines():
        line = line_original.decode().strip()
        if line == "":
            continue
        try:
            if (line[0] == "[") and (line[-1] == "]"):
                continue
        except IndexError:
            print("Can't parse \"{}\"".format(line))
        ret.append(line.strip())
    return ret


print("")

proc = subprocess.Popen(["php", "-m"],
                        stdout=subprocess.PIPE)
php_modules = parse_modules(proc)

procX = subprocess.Popen(["php"+requested_ver, "-m"],
                         stdout=subprocess.PIPE)
phpX_modules = parse_modules(procX)

print("You have php:")
print(php_modules)
print("AND php{}:".format(requested_ver))
print(phpX_modules)
goods = {}

print("")
print("* checking Nextcloud requirements...")
print("")

for r in oc_mods.keys():
    goods[r] = False

for r in (php_modules):
    # vr = "php{}-{}".format("", r)
    if (goods.get(r) is not None):
        goods[r] = True
        print("{}: {}".format(r, True))

for r in (phpX_modules):
    # vr = "php{}-{}".format(requested_ver, r)
    if (goods.get(r) is not None):
        goods[r] = requested_ver
        print("{}: {}".format(r, requested_ver))

print("")
for r,v in goods.items():
    if v is False:
        print("{}: {}".format(r, v))

print("Some things may say they are missing in Debian when they are not. This may be fixed in a future version of this script.")
print("Running php-set-version... and nextcloud-deps-more.sh should install all dependencies. Follow instructions they output for more information.")
print("")
