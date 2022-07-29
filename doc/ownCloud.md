# ownCloud

I recommend Nextcloud instead of ownCloud due to Nextcloud's
community-driven approach (priority on stability and compatibility with
other products rather than buzzword features).

Tested on Fedora 25:

owncloud client (below) as per https://software.opensuse.org/download/package?project=isv:ownCloud:desktop&package=owncloud-client (package in fedora/rpmfusion didn't work--client didn't open after successful config--one below worked and picked up that saved login instantly)
```
sudo dnf config-manager --add-repo http://download.opensuse.org/repositories/isv:ownCloud:desktop/Fedora_25/isv:ownCloud:desktop.repo
sudo dnf install owncloud-client
```
