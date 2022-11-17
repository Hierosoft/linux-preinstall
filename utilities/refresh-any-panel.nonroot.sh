
found_mate_panel="`ps aux | grep mate-panel | grep -v grep`"
if [ ! -z "$found_mate_panel" ]; then
    mate-panel --replace
fi
update-desktop-database
# /home/owner/.local/share/applications/xfce4-appfinder.desktop

found_cinnamon="`ps | grep cinnamon`"
# TODO: use a universal reloader (see code in )
if [ ! -z "$found_cinnamon" ]; then
    nohup cinnamon --replace & disown
fi


# See <https://askubuntu.com/a/722713>
# WARNING:
# The unity command causes DATA LOSS if any data is unsaved!
# (See Ace's comment on the answer above)
#unity_procs="`ps aux | grep unity | grep -v grep`"
#if [ ! -z "$unity_procs" ]; then
#    unity
#fi
