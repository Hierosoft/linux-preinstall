#!/bin/bash
cat <<END
> https://github.com/daniruiz/skeuos-gtk/archive/master.zip
>
> Generate ANY Color theme!
>
>     Download the `master.zip` package and extract it.
>     Inside it run:
>
>
> ./generate-color-theme.sh VARIANT_NAME HIGHLIGHT_HEX_COLOR HIGHLIGHT_TEXT_HEX_COLOR
>
>
> Example:
>
> ./generate-color-theme.sh FOOBAR '#123456' '#987654'

-<https://www.gnome-look.org/p/1441725/>

WARNING: It has the dumb up arrow for open and down arrow for save like Flat Remix Dark (which seems to be a direct rip of it that requires instead of includes the metacity theme) though.
- See [Open, Save, and Save All buttons seem ambiguous (up is open, down is save)](https://github.com/daniruiz/skeuos-gtk/issues/31)
-Poikilos

END

