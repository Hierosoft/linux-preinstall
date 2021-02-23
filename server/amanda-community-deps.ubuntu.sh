#!/bin/bash
# See https://www.zmanda.com/assets/pdf/Amanda_Community_Setup_15_minutes.pdf
# The steps in this file are modified from the above to suit Ubuntu.
apt update
# yum install wget

# DEPENDENCIES FOR AMANDA BACKUP SERVER
apt install -y wget
# server deps (client deps are the same):
# yum install glib* xinetd perl-Data-Dumper perl-Encode-Locale perl-JSON perl-URI-Escape perl-XML-Simple

apt install -y xinetd perl
# on Ubuntu, perl comes with some of the addons:

customDie() {
    code=1
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    if [ ! -z $2 ]; then
        code=$2
    fi
    exit $code
}

checkpmod() {
    name=$1
    package=$2
    perl -e "use $name"
    if [ $? -eq 0 ]; then
        if [ ! -z "$package" ]; then
            echo "Checking for perl $name...found (installed $package)"
        else
            echo "Checking for perl $name...found (using perl)"
        fi
    else
        if [ ! -z "$package" ]; then
            echo "Checking for perl $name...missing (there is no $package available from selected repositories)"
        else
            echo "Checking for perl $name...missing (not included with perl)"
        fi
        exit 1
    fi
}

installpmod() {
    name=$1
    package=$2
    perl -e "use $name"
    if [ $? -eq 0 ]; then
        echo "Checking for perl $name...found (via perl such as $package)"
    else
        apt install -y $package
        checkpmod $name $package
    fi
}

checkpmod Data::Dumper
checkpmod Encode::Locale
checkpmod URI::Escape
installpmod JSON libjson-perl
installpmod XML::Simple libxml-simple-perl

service xinetd reload || customDie "You must correct the preceding errors with xinetd before trying to run '$0' again. See https://www.zmanda.com/assets/pdf/Amanda_Community_Setup_15_minutes.pdf section 3.2 (\"ADDITIONAL CHECKS FOR AMANDA BACKUP SERVER\")"

echo "This script only gets the dependencies. See https://www.zmanda.com/assets/pdf/Amanda_Community_Setup_15_minutes.pdf to continue the installation manually."
