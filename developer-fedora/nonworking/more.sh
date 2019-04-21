#!/bin/bash
echo "Skipping butterflow since it doesn't work with opencv3"
# pip2 install --global-option="-I/usr/include/ffmpeg" https://github.com/dthpham/butterflow/archive/master.zip
# above fails with error:
#Complete output from command /usr/bin/python2 -u -c "import setuptools, tokenize;__file__='/tmp/pip-req-build-XPxl6K/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" -I/usr/include/ffmpeg install --record /tmp/pip-record-zMaKn1/install-record.txt --single-version-externally-managed --compile:
#    usage: -c [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
#       or: -c --help [cmd1 cmd2 ...]
#       or: -c --help-commands
#       or: -c cmd --help
#
#    error: option -I not recognized
#
#    ----------------------------------------
#Command "/usr/bin/python2 -u -c "import setuptools, tokenize;__file__='/tmp/pip-req-build-XPxl6K/setup.py';f=getattr(tokenize, 'open', open)(__file__);code=f.read().replace('\r\n', '\n');f.close();exec(compile(code, __file__, 'exec'))" -I/usr/include/ffmpeg install --record /tmp/pip-record-zMaKn1/install-record.txt --single-version-externally-managed --compile" failed with error code 1 in /tmp/pip-req-build-XPxl6K/
#mkdir -p ~/Downloads/git/
cd ~/Downloads/git/
#wget https://github.com/opencv/opencv/archive/2.4.13.6.tar.gz
#tar xf 2.4.13.6.tar.gz
## tried (doesn't work due to differences)
#export CPPFLAGS="-I$HOME/Downloads/git/opencv-2.4.13.6/include -I$HOME/Downloads/git/opencv-2.4.13.6/modules/ocl/include -I/usr/include/ffmpeg"
## but it still doesn't have ocl (except in modules dir) so:
#cd $USER/Downloads/git/opencv-2.4.13.6
#mkdir build
#cd build
## add -DOPENCV_GENERATE_PKGCONFIG=ON for "projects that use OpenCV" "not using CMake" (see <https://docs.opencv.org/trunk/d7/d9f/tutorial_linux_install.html>)
#cmake -D CMAKE_BUILD_TYPE=Release -DOPENCV_GENERATE_PKGCONFIG=ON -D CMAKE_INSTALL_PREFIX=/usr/local ..
#make -j$(nproc)
## sudo make install
#pip2 install https://github.com/dthpham/butterflow/archive/master.zip
# get RELEASE since compiling doesn't work (see my issue at <https://github.com/dthpham/butterflow/issues/104>)
# ignore commented WINDOWS release:
#dl_name=butterflow-0.2.3.7z
#extracted_name=butterflow-0.2.3

#wget -O $dl_name https://github.com/dthpham/butterflow/releases/download/v0.2.3/$dl_name
#if [ -f $dl_name ]; then
    #if [ -f "`command -v 7z`" ]; then
        #7z x butterflow-0.2.3.7z
        #if [ -d "$extracted_name" ]; then
            #cd "$extracted_name"

        #else
            #echo "ERROR: can't install $dl_name since failed to extract $extracted_name directory"
        #fi
    #else
        #echo "ERROR: can't install $dl_name since missing 7z"
    #fi
#else
    #echo "ERROR: can't download $dl_name"
#fi
wget -O $dl_name https://github.com/dthpham/butterflow/releases/download/v0.2.3/$dl_name
if [ -f $dl_name ]; then
    if [ -f "`command -v 7z`" ]; then
        7z x butterflow-0.2.3.7z
        if [ -d "$extracted_name" ]; then
            cd "$extracted_name"

        else
            echo "ERROR: can't install $dl_name since failed to extract $extracted_name directory"
        fi
    else
        echo "ERROR: can't install $dl_name since missing 7z"
    fi
else
    echo "ERROR: can't download $dl_name"
fi
