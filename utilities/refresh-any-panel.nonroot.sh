
mate_panels="`ps aux | grep mate-panel | grep -v grep`"
if [ ! -z "$mate_panels" ]; then
    mate-panel --replace
fi
update-desktop-database
# /home/owner/.local/share/applications/xfce4-appfinder.desktop


# See <https://askubuntu.com/a/722713>
# WARNING:
# The unity command causes DATA LOSS if any data is unsaved!
# (See Ace's comment on the answer above)
#unity_procs="`ps aux | grep unity | grep -v grep`"
#if [ ! -z "$unity_procs" ]; then
#    unity
#fi
