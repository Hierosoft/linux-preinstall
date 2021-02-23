#!/bin/sh
sudo apt update
sudo apt install nfs-kernel-server

sudo ufw allow from 192.168.1.0/24 to any port nfs
# TODO: line above results in:
#WARN: Rule changed after normalization
#Rule added

# /25 would allow a range of 127 addresses.
# (See https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#IPv4_CIDR_blocks
# as cited by A.B. on Jul 9 '15 at 17:36 and Fabby on Jul 10 '15 at 10:09 on
# <https://askubuntu.com/questions/646424/ufw-allow-range-of-ip-addresees>)

cat <<END

Usage:
    hostnamectl set-hostname poikilos.home.local
    # where poikilos.home.local is the name you want for the server
    sudo nano /etc/exports
    # then add a line such as: /tank/cloud 192.168.1.0/24(rw,sync,no_subtree_check)
    # where 192.168.1.0/24 is your subnet to allow to access the server.
    #
    # > rw: This option gives the client computer both read and write access to the volume.
    # > sync: This option forces NFS to write changes to disk before replying. This results in a more stable and consistent environment since the reply reflects the actual state of the remote volume. However, it also reduces the speed of file operations.
    # > no_subtree_check: This option prevents subtree checking, which is a process where the host must check whether the file is actually still available in the exported tree for every request. This can cause many problems when a file is renamed while the client has it opened. In almost all cases, it is better to disable subtree checking.
    # > no_root_squash: By default, NFS translates requests from a root user remotely into a non-privileged user on the server. This was intended as security feature to prevent a root account on the client from using the file system of the host as root. no_root_squash disables this behavior for certain shares.
    # -<https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-18-04> accessed 2020-10-23

    # After adding lines to /etc/exports, run:
    # sudo systemctl restart nfs-kernel-server

Configure Fedora clients:
# See <https://www.server-world.info/en/note?os=Fedora_31&p=nfs&f=2>:
sudo dnf -y install nfs-utils
sudo hostnamectl set-hostname pgs.home.local
# where pgs.home.local is the name of the client you are configuring

sudo nano /etc/idmapd.conf

# edit the Domain line to: Domain = home.local

- I also set the following:
# server information (REQUIRED)
# LDAP_server = ldap-server.local.domain.edu
LDAP_server = poikilos.home.local

# the default search base (REQUIRED)
# LDAP_base = dc=local,dc=domain,dc=edu
LDAP_base = dc=home,dc=local


sudo nano /etc/fstab
# To allow non-root users to mount the share, add something like the following:
192.168.1.5:/tank/cloud                   /nfs/cloud              nfs     rw,noatime,user,noauto 0 0
# then users can run: mount /nfs/cloud
END
