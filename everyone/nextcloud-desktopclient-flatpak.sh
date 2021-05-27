#!/bin/sh
sudo flatpak install -y flathub com.nextcloud.desktopclient.nextcloud
cat <<END

The nextcloud config appears as ~/.var/app/com.nextcloud.desktopclient.nextcloud/config/Nextcloud/nextcloud.cfg after the first run.
(The packaged version would be ~/.config/Nextcloud/nextcloud.cfg )

END
