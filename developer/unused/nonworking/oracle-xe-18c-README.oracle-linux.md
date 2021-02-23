# Oracle XE 18c
(on Oracle Linux NetApps_VM)

## Known Issues
* Won't authenticate--with neither local sqlplus nor SQL Developer
  - Try using the copy of oracle database (11c as of 2019-05-24) preinstalled with the Oracle Linux
    NetApps_VM instead

## Not Tried yet
* ```bash
# Step below is guessed based on https://yum.oracle.com/faq.html
wget -O /etc/pki/rpm-gpg/RPM-GPG-KEY-oracle http://yum.oracle.com/RPM-GPG-KEY-oracle-ol6
```
