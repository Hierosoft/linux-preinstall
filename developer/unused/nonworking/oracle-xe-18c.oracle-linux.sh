#!/usr/bin/sh
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

yum remove -y oracle-xe
#the following is done automatically on Oracle Linux:
#curl -o oracle-database-preinstall-18c-1.0-1.el7.x86_64.rpm https://yum.oracle.com/repo/OracleLinux/OL7/latest/x86_64/getPackage/oracle-database-preinstall-18c-1.0-1.el7.x86_64.rpm
#yum -y localinstall oracle-database-preinstall-18c-1.0-1.el7.x86_64.rpm
#References
#“Database Express Edition Installation Guide for Linux.” Oracle Help Center, https://docs.oracle.com/en/database/oracle/oracle-database/18/xeinl/procedure-installing-oracle-database-xe.html. Accessed 26 May 2019.


#dl_name="oracle-database-preinstall-18c-1.0-1.el7.x86_64.rpm"
dl_name="oracle-database-xe-18c-1.0-1.x86_64.rpm"
dl_path="$HOME/Downloads/$dl_name"
installed_config_bin="/etc/init.d/oracle-xe-18c"
if [ -d "$HOME/Downloads" ]; then
    mkdir -p "$HOME/Downloads"
fi
cd "$HOME/Downloads"

#This won't work--authentication is needed:
#if [ ! -f "$dl_path" ]; then
#    wget -O "$dl_path" http://download.oracle.com/otn/linux/oracle18c/xe/$dl_name
#fi

manual_url="https://www.oracle.com/technetwork/database/database-technologies/express-edition/downloads/index.html"
try_path=/home/oracle/Downloads/$dl_name
try_msg="or '$try_path'"
if [ -f "$try_path" ]; then
    try_msg=" or '$dl_path'"
    dl_path="$try_path"
fi
if [ ! -f "$dl_path" ]; then
    customDie "This script requires $dl_path such as from $manual"
fi
manual_msg="'$dl_name' could not be installed. Try downloading manually from $manual_url using an Oracle account (create a free account there if necessary) and overwrite '$dl_path'$try_msg, then run this script again."
yum -y localinstall $dl_path || customDie "$manual_msg"
echo Done
if [ ! -f "$installed_config_bin" ]; then
    echo "Missing '$installed_config_bin'"
    customDie "$manual_msg"
fi
echo "Waiting for service"
sleep 10
$installed_config_bin configure || echo "Try running '$installed_config_bin configure' again ('Listener setup' may fail the first time)."
#...says: Listener configuration failed. Check log '/opt/oracle/cfgtoollogs/netca/netca_configure_out.log' for more details.
#The log contains:
#No valid IP Address returned for the host ol7.
#Check the trace file for details: /opt/oracle/cfgtoollogs/netca/#trace_OraHomeXE-1905268PM0208.log

echo "See also /etc/sysconfig/oracle—xe–18c.conf"

