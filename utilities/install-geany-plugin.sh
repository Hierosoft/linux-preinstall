#!/bin/bash
# ^ bash since requires source
source $HOME/.config/linux-preinstall/globals.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $HOME/.config/linux-preinstall/globals.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi
source $LINUX_PREINSTALL/api.rc
if [ $? -ne 0 ]; then
    echo "ERROR: 'source $LINUX_PREINSTALL/api.rc' failed."
    echo "You must run linux-preinstall/setup.sh first."
    exit 1
fi



touch $POSTINSTALL
# ^ from api.rc

if [ -z "$plugin_name" ]; then
    plugin_name="$1"
fi
failed=false
if [ -z "$plugin_name" ]; then
    echo "You must specify a plugin name."
    echo "Attemping to list packages (this may take a while)..."
    failed=true
else
    $INSTALL_CMD geany-plugin-$plugin_name || failed=true
    if [ "$failed" = "@true" ]; then
        echo "geany-plugin-* is missing from the repo, you are not connected,"
        echo "you did not run this script as root,"
        echo "or the plugin $plugin_name doesn't exist."
    fi
fi
if [ "$failed" = "@true" ]; then
    # dnf list available geany-plugins-\*
    $PKG_SEARCH_CMD geany-plugin
    echo
    echo "You must specify one of the plugins listed above for this to work"
    echo "(excluding the geany-plugins- part)."
fi

done_flag_path=~/.config/linux-preinstall/flag_done_install-geany-plugin-postinstall

if [ ! -f "$done_flag_path" ]; then
    cat >> $POSTINSTALL <<END


## install-geany-plugin.sh $plugin_name

### Recommended plugins:
* addons: The addons plugin allows copying the full path of an
  open file to the clipboard.
   - How to use: Tools, Copy File Path
   - The addons plugin also adds several other features.
     See also
     <https://plugins.geany.org/addons.html#copy-file-path>.

Don't forget to enable the $plugin_name plugin in Geany:
Tools, Plugin Manager, then check the $plugin_name box.
END
    tail -n 14 $POSTINSTALL
    touch "$done_flag_path"
else
    echo "finished installing geany-plugins-$plugin_name"
fi
if [ "$failed" = "@true" ]; then
    exit 1
else
    exit 0
fi

if [ -f /usr/lib64/geany/$plugin_name.so ]; then
    if [ -f $HOME/.config/geany/geany.conf ]; then
	# TODO: enable automatically:
	#    [plugins]
	#    load_plugins=true
	#    custom_plugin_path=
	#    active_plugins=/usr/lib64/geany/$plugin_name.so;/usr/lib64/geany/filebrowser.so;/usr/lib64/geany/saveactions.so;
	echo "You must manually enable the plugin."
    else
	conf_src_dir="HOME/.config/geany"
	conf_src="HOME/.config/geany/geany.conf"
	if [ -f "$conf_src" ]; then
	    if [ ! -d "$HOME/.config/geany" ]; then
		mkdir -p "$HOME/.config/geany"
	    fi
	    # check for bracket after plugins:
	    if [ -z `sed -n '/\[plugins\]/,$p' geany/geany.conf | grep ]` ]; then
		cp "$conf_src" "$HOME/.config/geany/" || customDie "failed to cp HOME/.config/geany/geany.conf $HOME/.config/geany/"
		new_active_plugins_line="active_plugins=/usr/lib64/geany/$plugin_name.so;/usr/lib64/geany/filebrowser.so;/usr/lib64/geany/saveactions.so;"
		echo "$new_active_plugins_line" >> $HOME/.config/geany/geany.conf || customDie "failed to copy active_plugins setting to $HOME/.config/geany/geany.conf"
		echo "$HOME/.config/geany/geany.conf has been automatically patched with the line $new_active_plugins_line"
	    else
		echo "Failed to patch conf since the last section in $conf_src is not [plugins]"
		echo "You'll have to enable the plugin_manually or correct that."
		failed=true
	    fi
	else
	    customDie "$conf_src does not exist in `pwd`. You must run this script from the linux-preinstall/utilities directory."
	fi
    fi
else
    echo "/usr/lib64/geany/$plugin_name.so does not exist."
    echo "Since the .so file could not be detected, you must enable"
    echo "the plugin manually"
fi
echo
echo
if [ "$failed" = "@true" ]; then
    exit 1
else
    exit 0
fi
echo "Compiling..."
echo "NOTE: Installing from git automatically is not implemented."
echo
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exitcode=1
    if [ ! -z "$2" ]; then exitcode=$2; fi
    exit $exitcode
}
external_repos_path=~/Downloads/git
git_namespace=geany
this_repos_path="$external_repos_path"
plugins_extracted_name=geany-plugins
plugins_url=https://github.com/geany/$plugins_extracted_name.git
if [ ! -d "$this_repos_path" ]; then
    mkdir -p "$this_repos_path" || customDie "Cannot create $this_repos_path"
fi
cd "$this_repos_path" || customDie "Cannot cd $this_repos_path"

if [ ! -d geany-plugins ]; then
    git clone $plugins_url || customDie "Cannot git clone $plugins_url"
    cd $plugins_extracted_name || customDie "Cannot cd $plugins_extracted_name"
else
    cd $plugins_extracted_name || customDie "Cannot cd $plugins_extracted_name"
    git pull || customDie "Cannot git pull from `pwd`"
fi

./configure
make
#make install
echo "Installing plugins from git automatically is not implemented."
echo "You must copy the plugin from `pwd` to your plugins directory."
echo "You must also set custom_plugin_path to use .so plugin files from"
echo "a directory other than /usr/lib64/geany/ (or the directory under"
echo "your particular prefix)."
echo
echo
