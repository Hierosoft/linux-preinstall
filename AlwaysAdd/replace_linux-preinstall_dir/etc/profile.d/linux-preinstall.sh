for DIR in \
    /opt/git/linux-preinstall/utilities-developer \
    /opt/git/linux-preinstall/utilities-server \
    /opt/git/linux-preinstall/utilities
do
    if [  -d $DIR ]; then
        PATH=$DIR:$PATH
    fi
done
