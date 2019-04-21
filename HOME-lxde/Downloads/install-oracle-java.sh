#!/bin/sh

#Edited by Entricular, Maluniu, Snow Wolf, Nubiognu and 9 others. "How to Install Oracle Java JDK on Ubuntu Linux." Wikihow. <http://www.wikihow.com/Install-Oracle-Java-JDK-on-Ubuntu-Linux> 22 Apr, 2014.
cd ~/Downloads
sudo apt-get purge openjdk-\*
#Download the latest version from http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
#and save to Downloads, since wget does not work for some reason
#wget http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-i586.tar.gz
sudo mkdir /usr/local/java
sudo cp -r jdk*i586.* /usr/local/java/
sudo cd /usr/local/java
sudo rm -Rvf jdk*
sudo tar xvzf jdk-*i586.*
cd jdk*

#The rest will only work if you know the Java path. To get it, you could now do:
#ls -d */

#The following must also be appended to /etc/profile, but echo does not work since variables are used.
JAVA_HOME=/usr/local/java/jdk1.8.0_05
PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
export JAVA_HOME
export PATH

#this command notifies the system that Oracle Java JRE is available for use:
sudo update-alternatives --install "/usr/bin/java" "java" "/usr/local/java/jdk1.8.0_05/bin/java" 1
#this command notifies the system that Oracle Java JDK is available for use:
sudo update-alternatives --install "/usr/bin/javac" "javac" "/usr/local/java/jdk1.8.0_05/bin/javac" 1
#this command notifies the system that Oracle Java Web start is available for use:
sudo update-alternatives --install "/usr/bin/javaws" "javaws" "/usr/local/java/jdk1.8.0_05/bin/javaws" 1

#this command will set the java runtime environment for the system:
sudo update-alternatives --set java /usr/local/java/jdk1.8.0_05/bin/java
#this command will set the javac compiler for the system:
sudo update-alternatives --set javac /usr/local/java/jdk1.8.0_05/bin/javac
#this command will set Java Web start for the system:
sudo update-alternatives --set javaws /usr/local/java/jdk1.8.0_05/bin/javaws

javac -version
#--should display something like:
#java version "1.8.0_05"
#Java(TM) SE Runtime Environment (build 1.8.0_05-b13)
#Java HotSpot(TM) Client VM (build 25.5-b02, mixed mode)
#--64-bit version should display something like:
#java version "1.7.0_51"
#Java(TM) SE Runtime Environment (build 1.7.0_51-b13)
#Java HotSpot(TM) 64-Bit Server VM (build 24.51-b03, mixed mode)

#restart is needed so system-wide PATH reloads (java works in other windows)!