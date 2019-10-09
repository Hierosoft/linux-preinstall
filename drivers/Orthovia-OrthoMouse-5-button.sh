xmodmap -e "pointer = 1 4 3 7 9 5 8 2"
# > The numbers are not random, as each entry corresponds to a function.
# > You should first consider that the first position corresponds to the
# > left-click, the second to the middle click, the third to the right
# > click, fourth and fifth to up and down scrolling etc. So, if your
# > middle click isn't working, you should use the middle click
# > outputted number from “xev” on the second position in the xmodmap
# > command. If you are left handed, you may swap keys 3 and 1 to
# > correspond to invert right-left clicking etc. By typing:
# > xmodmap -pp
# (Toulas, n.d.)

nohup xev &
sleep 4
killall xev
CAT <<END
xev seems to toggle functionality on and off somehow, but never
detects the presses for scroll buttons nor thumb (middle) button.

Current Status: OrthoMouse middle click is intermittent on Fedora 30.

END

# References
# Toulas, B. (n.d.). How to map your mouse on Linux. Retrieved September 3, 2019, from HowtoForge website: https://www.howtoforge.com/tutorial/map-mouse-on-linux/
