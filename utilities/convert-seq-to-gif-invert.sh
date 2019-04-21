#!/bin/bash
ffmpeg -i tmp/%04d.png -r 60 -vf lutrgb="r=negval:g=negval:b=negval" animation.gif

