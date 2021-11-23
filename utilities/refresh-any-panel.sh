update-desktop-database

# Answers below are from the following question:
# <https://askubuntu.com/questions/722708/how-do-i-refresh-the-icon-cache>.

# See <https://askubuntu.com/a/722721>
# 
# edited Sep 18 '16 at 18:24
# by fossfreedom
# answered Jan 19 '16 at 0:04
# by Timo Kluck:
update-icon-caches /usr/share/icons/*

# Geekly's reply to the answer above says the following is still required for Dolphin:
rm ~/.cache/icon-cache.kcache
# TODO: restart dolphin here

# See Brandan Long's answer <https://askubuntu.com/a/884758>:
sudo touch /usr/share/icons/hicolor ~/.local/share/icons/hicolor
gtk-update-icon-cache

