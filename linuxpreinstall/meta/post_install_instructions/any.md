The following are the reasons for the bluetooth packages selected by linux-preinstall:
- Notes on bluez-tools, bluez-hid2hci, blueman:
  - blueman pulls in: bluez-obexd (others didn't install anything additional)
  - rfkill is not removeable. It was never manually installed (dnf history list rfkill says: "No transaction which manipulates package 'rfkill' was found.") and it can't be removed without removing systemd.
  - Doing the above causes KDE to prompt for privs after login for both blueman and RfKill (separate prompt for each)
  - Doing the above also results in two bluetooth symbol icons on the task tray (one blurry blue blueman one, plus one themed one)
