#!/bin/sh

#formerly:
#(below installs no JavaFX, and no java-latest-openjdk-devel technically)
#dnf install -y
#    java-1.8.0-openjdk-devel \
#    java-1.8.0-openjdk \
#    ;

#~2019 java-openjdk-* was renamed to java-latest-openjdk-*

dnf install  \
    java-latest-openjdk-devel \
    java-latest-openjdk \
    javafx-devel \
    javafx \
    ;
# as of Fedora 29, javafx-devel and javafx are version 8, though
# java-latest-openjdk* are 12. SQL Developer doesn't detect JavaFX.

# javafx: equivalent to openjfx
# javafx-devel: equivalent to openjfx-devel
