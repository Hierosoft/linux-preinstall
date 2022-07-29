# Keyring
A keyring generally is required and not automatic except in KDE for some reason :(.

Avoid the annoying gnome-keyring popup that appears the first time you load every program in every session :(. This problem doesn't happen with KDE but for years GNOME has ignored it (See also [GHOME is deeply flawed](https://poikilos.org/2021/04/21/gnome-is-deeply-flawed/)).

One possible solution is to remove the gnome-keyring package, but other packages reinstall it:
- :( Brave Browser
- :( Nextcloud client

## Avoid the keyring issue in specific programs
- Brave Browser: Add the `--password-store=basic` option such as, if you have the binary named /usr/bin/brave-browser-stable, override the system's icon via:

```
cd linux-preinstall && \
  mkdir -p ~/.local/share/applications && \
  cp AlwaysAdd/HOME/.local/share/applications/brave-browser.desktop \
    ~/.local/share/applications/
```
The icon was modified in the following ways:
- For more compatibility (so it works with either brave-browser-stable or other binaries), it requires the /usr/bin/brave-browser alias.
  - If it doesn't load, ensure the alternatives are set in your OS:
    `update-alternatives --config brave-browser`
- Note that to fix the shortcut (such as was already done in the one above), there is not just one `Exec=` line. Each must be fixed such as in the following subsections in the icon for the Ubuntu 20.04 package of 102.1.39.111:
  - `[Desktop Entry]`
  - `[Desktop Action new-window]`
  - `[Desktop Action new-private-window]`
