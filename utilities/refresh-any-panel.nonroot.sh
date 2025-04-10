
found_mate_panel="`ps aux | grep mate-panel | grep -v grep`"
if [ ! -z "$found_mate_panel" ]; then
    mate-panel --replace
    exit $?
fi
update-desktop-database
# $HOME/.local/share/applications/xfce4-appfinder.desktop

found_cinnamon="`ps x | grep cinnamon | grep -v grep`"
# x: all users
# TODO: use a universal reloader (see code in )
if [ ! -z "$found_cinnamon" ]; then
    # "r" doesn't work from terminal, so:
    # nohup cinnamon --replace & disown
    # Restart preserving open windows and running applications as per <https://askubuntu.com/a/523436>:
    pkill -HUP -f "cinnamon --replace"
    exit $?
fi
echo "Warning: The panel for your desktop environment was not detected. New icon(s) may not appear until GUI logout and login."
exit 1


# See <https://askubuntu.com/a/722713>
# WARNING:
# The unity command causes DATA LOSS if any data is unsaved!
# (See Ace's comment on the answer above)
#unity_procs="`ps aux | grep unity | grep -v grep`"
#if [ ! -z "$unity_procs" ]; then
#    unity
#fi
