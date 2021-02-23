#!/usr/bin/env python3
#!/bin/bash
# tty1 is only the LCD if the server has no video card.
lcd=/dev/tty1
echo $1 > $lcd
echo $2 > $lcd
echo $3 > $lcd
#echo > $lcd
