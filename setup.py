import setuptools
import sys
# - For the example on which this was based, see
#   https://github.com/poikilos/world_clock/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/nopackage/blob/main/setup.py
#   which is based on
#   https://github.com/poikilos/pypicolcd/blob/master/setup.py
# - For nose, see https://github.com/poikilos/mgep/blob/master/setup.py

# python_mr = sys.version_info.major
# versionedModule = {}
# versionedModule['urllib'] = 'urllib'
# if python_mr == 2:
#     versionedModule['urllib'] = 'urllib2'

install_requires = []

with open("requirements.txt", "r") as ins:
    for rawL in ins:
        line = rawL.strip()
        if len(line) < 1:
            continue
        install_requires.append(line)

description = '''The linuxpreinstall module has useful features
for system and file management. The larger linux-preinstall project has
many shell scripts for setting up GNU+Linux systems more quickly.
Features will be moved to Python as seems reasonable.'''
long_description = description
if os.path.isfile("readme.md"):
    with open("readme.md", "r") as fh:
        long_description = fh.read()

setuptools.setup(
    name='linuxpreinstall',
    version='0.5.0',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        ('License :: OSI Approved ::'
         ' GNU General Public License v3 or later (GPLv3+)'),
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Systems Administration',
    ],
    keywords=('python system management IT tools linux installation'
              ' package selection preloading preinstall'),
    url="https://github.com/poikilos/linux-preinstall",
    author="Jake Gustafson",
    author_email='7557867+poikilos@users.noreply.github.com',
    license='GPLv3+',
    # packages=setuptools.find_packages(),
    packages=['linuxpreinstall'],
    include_package_data=True,  # look for MANIFEST.in
    # scripts=['example'],
    # ^ Don't use scripts anymore (according to
    #   <https://packaging.python.org/en/latest/guides
    #   /distributing-packages-using-setuptools
    #   /?highlight=scripts#scripts>).
    entry_points={
        'console_scripts': [
            'cleanif=linuxpreinstall.cleanif:main',
            'findmime=linuxpreinstall.findmime:main',
            'unredirect_md=linuxpreinstall.unredirect:main',
            'selectoutput=linuxpreinstall.selectoutput:main',
            'whichicon=linuxpreinstall.whichicon:main',
            'ggrep=linuxpreinstall.ggrep:main',
            # 'cb-install-theme=linuxpreinstall.codeblocks.theme:main',  # WIP
            'backup-nginx-symlinks=linuxpreinstall.server.backup_nginx_symlinks:main',
            'sort-brisk-menu-favs=linuxpreinstall.mate.brisk_menu:main',
            # 'remove-blank-mate-items=linuxpreinstall.mate.panel:main',  # WIP
        ],
    },
    install_requires=install_requires,
    # versionedModule['urllib'],
    # ^ "ERROR: Could not find a version that satisfies the requirement
    #   urllib (from nopackage) (from versions: none)
    # ERROR: No matching distribution found for urllib"
    # (urllib imports fine in Python3 on Fedora 35 though
    # pip uninstall urllib and pip uninstall urllib2 do nothing)
    test_suite='nose.collector',
    tests_require=['nose', 'nose-cover3'],
    zip_safe=False,  # It can't run zipped due to needing data files.
)
