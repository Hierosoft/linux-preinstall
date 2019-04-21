#as per http://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu
sudo apt-get update
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev \
  libsdl1.2-dev libtheora-dev libtool libva-dev libvdpau-dev libvorbis-dev libxcb1-dev libxcb-shm0-dev \
  libxcb-xfixes0-dev pkg-config texinfo zlib1g-dev
#Note: Server users can omit the ffplay and x11grab dependencies: libsdl1.2-dev libva-dev libvdpau-dev libxcb1-dev libxcb-shm0-dev libxcb-xfixes0-dev. 
mkdir ~/ffmpeg_sources

sudo apt-get install yasm
# Otherwise you can compile:
#cd ~/ffmpeg_sources
#wget http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
#tar xzvf yasm-1.3.0.tar.gz
#cd yasm-1.3.0
#./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"
#make
#make install
#make distclean

# Requires ffmpeg to be configured with --enable-gpl --enable-libx264:
sudo apt-get install libx264-dev
# Otherwise you can compile:
#cd ~/ffmpeg_sources
#wget http://download.videolan.org/pub/x264/snapshots/last_x264.tar.bz2
#tar xjvf last_x264.tar.bz2
#cd x264-snapshot*
#PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static
#PATH="$HOME/bin:$PATH" make
#make install
#make distclean

#libx265:
sudo apt-get install cmake mercurial
cd ~/ffmpeg_sources
hg clone https://bitbucket.org/multicoreware/x265
cd ~/ffmpeg_sources/x265/build/linux
PATH="$HOME/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make
make install
make distclean


#Requires ffmpeg to be configured with --enable-libfdk-aac (and --enable-nonfree if you also included --enable-gpl):
cd ~/ffmpeg_sources
wget -O fdk-aac.tar.gz https://github.com/mstorsjo/fdk-aac/tarball/master
tar xzvf fdk-aac.tar.gz
cd mstorsjo-fdk-aac*
autoreconf -fiv
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make
make install
make distclean
cd ~/ffmpeg_sources

#Requires ffmpeg to be configured with --enable-libmp3lame:
sudo apt-get install libmp3lame-dev
# Otherwise you can compile:
#sudo apt-get install nasm
#cd ~/ffmpeg_sources
#wget http://downloads.sourceforge.net/project/lame/lame/3.99/lame-3.99.5.tar.gz
#tar xzvf lame-3.99.5.tar.gz
#cd lame-3.99.5
#./configure --prefix="$HOME/ffmpeg_build" --enable-nasm --disable-shared
#make
#make install
#make distclean

#Requires ffmpeg to be configured with --enable-libopus:
sudo apt-get install libopus-dev
#cd ~/ffmpeg_sources
#wget http://downloads.xiph.org/releases/opus/opus-1.1.tar.gz
#tar xzvf opus-1.1.tar.gz
#cd opus-1.1
#./configure --prefix="$HOME/ffmpeg_build" --disable-shared
#make
#make install
#make clean

#Requires ffmpeg to be configured with --enable-libvpx:
cd ~/ffmpeg_sources
wget http://storage.googleapis.com/downloads.webmproject.org/releases/webm/libvpx-1.5.0.tar.bz2
tar xjvf libvpx-1.5.0.tar.bz2
cd libvpx-1.5.0
PATH="$HOME/bin:$PATH" ./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests
PATH="$HOME/bin:$PATH" make
make install
#TODO: find out why says "nothing to be done for install"
#"I added the next line" -expertmm:
make install-srcs
make install-libs
make clean




#--enable-gpl --enable-libx264 --enable-nonfree --enable-libfdk-aac --enable-libmp3lame --enable-libopus --enable-libvpx
cd ~/ffmpeg_sources
wget http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
echo "This may take a while..."
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree
PATH="$HOME/bin:$PATH" make
make install
make distclean
hash -r

#usage:
sudo mkdir /mnt/iso
sudo chown owner /mnt/iso
sudo chgrp owner /mnt/iso
#sudo mount -o loop -t iso9660 ~/SuessificationOfAMND_The.iso /mnt/iso
##cat /mnt/iso/video_ts/*.VOB | /home/owner/bin/ffmpeg -i - dvd.mpg
##ffmpeg -i input.vob -c:v copy -target ntsc-dvd dvd.mpg
#Ensure that audio is converted in case source is DVD with weird audio encoding:
#cat /mnt/iso/video_ts/*.vob | ~/bin/ffmpeg -i - -c:v copy -target ntsc-dvd ~/dvd.mpg
