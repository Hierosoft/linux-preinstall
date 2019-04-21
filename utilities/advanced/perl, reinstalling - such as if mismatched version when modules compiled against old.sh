#!/bin/sh
echo ""
echo ""
echo "This collection of commands, in order, should reinstall the minimal (plus optional as mentioned in next paragraph) set of perl AUR packages in order to sync them with the installed version of perl (in order to fix build errors when trying to build AUR or other packages that depend on certain perl modules). Using -S --force could avoid many of the -R (remove) commands in this script, hence avoiding the need to remove dependent packages and possibly avoid ALL of the rm commands, however, reinstalling all of them is ideal if they are from AUR or otherwise built from source. If you get more errors beyond these packages, try removing and reinstalling the packages that are said by your package manager to be installed but which are broken--if any AUR build or other build fails, scroll up and see if you have an error about importing a perl module. For example, if says needs App::Cli, try pacman -S --force --noconfirm perl-app-cli [or yaourt if not found by pacman] or other package you find that starts with perl- and is named similarly to the class in the import error."
echo ""
echo "Be aware that source code for packages obtained via yaourt reside in folders named by package under /tmp/pamac-build-$USER/, so during this process, tmp may fill up, resulting in errors concerning not being able to copy files. In that case you may have to move the build folder to a new place such as $HOME/packagename then cd /tmp then ln -s $HOME/packagename where packagename is the name of the package that was too big."
echo ""
echo "Make sure you copy, paste & run these commands one by one, for if one fails, the rest is a waste of time. Some remove commands may be able to be combined. If any fail, remove any packages from the command that you don't use (are said to be missing) then try again--the problem in that case would be that the package is not found because it an optional package and you don't use it. Only after that command succeeds, try the next one."
echo "Be aware that the set of rm commands is from bijanbina on https://bbs.archlinux.org/viewtopic.php?id=213408 is destructive (even though he only used part of the initial list of commands) and probably not the best solution, but worked for me after I manually fixed all the breakages it caused."
exit 1
#When slic3r-git wouldn't build due to perl errors,
# I did the following rm commands and imagemagick install from https://bbs.archlinux.org/viewtopic.php?id=213408
# sudo rm -rf /usr/share/perl5/core_perl/*
# sudo rm -rf /usr/lib/perl5/site_perl/*
# sudo rm -rf /usr/share/perl5/site_perl/*
# sudo rm -rf /usr/lib/perl5/vendor_perl/*
# sudo rm -rf /usr/share/perl5/vendor_perl/*
sudo pacman -S --force perl imagemagick
#However after that I had different build errors, this time
# missing perl modules. After each was installed, another

#MUST run yaourt as sudoer, but NOT as root
yaourt -R perl-extutils-typemaps-default perl-extutils-makemaker-aur perl-extutils-xspp perl-extutils-cppguess perl-math-convexhull perl-math-convexhull-monotonechain perl-math-libm perl-math-planepath perl-module-build-withxspp perl-threads-aur perl-constant-defer
#An interesting note to slic3r developers (output from building perl-constant-defer):
# ==> Downloading perl-constant-defer PKGBUILD from AUR...
# x .SRCINFO
# x PKGBUILD
# swiftgeek commented on 2012-06-23 10:14			 
# A slic3r dependency
# Feel free to ask for adoption: i'm not maintaining this package unless it will be needed by slic3r
# Cheers

#Then resolve "Can't locate Test/Base.pm in @INC (you may need to install the Test::Base module)"
sudo pacman -R perl-test-base perl-spiffy perl-test-differences perl-text-diff perl-algorithm-diff
sudo pacman -S --noconfirm perl-test-base perl-spiffy perl-test-differences perl-text-diff perl-algorithm-diff
# but first remove that which depends on these:

yaourt -S --noconfirm perl-extutils-typemaps-default perl-extutils-makemaker-aur perl-extutils-xspp perl-extutils-cppguess perl-math-convexhull perl-math-convexhull-monotonechain perl-math-libm perl-math-planepath perl-module-build-withxspp perl-threads-aur perl-constant-defer
#NOTE: ignored the following issues:
# * t/03-xsstatic.t ........... skipped: Shared perl library
# * miniperl needed only for the miniperl core

#Removes the following so reinstall:
sudo pacman -S perl-params-validate perl-moo perl-module-implementation perl-import-into perl-module-runtime perl-module-build perl-inc-latest
yaourt -R perl-math-geometry-voronoi perl-math-clipper
#First reinstall the broken dependencies before reinstalling the above packages:
# (perl-libwww perl-math-clipper perl-module-implementation depend on try-tiny)
# (icoutils depends on perl-libwww)
# (playonlinux depends on icoutils)
# (perl-params-validate depends on perl-module-implementation)
sudo pacman -R perl-test-deep perl-try-tiny perl-libwww perl-math-clipper perl-module-implementation icoutils playonlinux perl-params-validate
sudo pacman -S --noconfirm perl-test-deep perl-try-tiny perl-libwww perl-module-implementation icoutils playonlinux perl-params-validate
#First reinstall broken dependences required by perl-math-geometry-voronoi
sudo pacman -R perl-class-accessor
sudo pacman -S perl-class-accessor
yaourt -S --noconfirm perl-math-geometry-voronoi perl-math-clipper
#Can't locate object method "new" via package "ExtUtils::Typemaps::Default" (perhaps you forgot to load "ExtUtils::Typemaps::Default"?)
sudo pacman -S --force perl-devel-checklib
#Can't update Antergos due to:
# Could not get file information for
# usr/lib/perl5/vendor_pearl/
#  auto/Error/
#  Error.pm
#  DBI.pm
#  DBD.pm
#  Win32
#  auto/DBI/
#  dbixs_rev.pl
# so:
#NOTE: perl-wx comes up using win32 keyword so used that to try to cover Win32 error
sudo pacman -S --force perl-dbi perl-error 
yaourt -S --force perl-wx
#and the following even though they weren't installed:
sudo pacman -S --force perl-dbd-mysql perl-dbd-sqlite

#Now reinstall some more stuff uncovered by slic3r build errors ("Devel::GlobalDestruction" "Sub::Quote" "Encode::Locale"):
# (perl-http-cookies is required by perl-http-message)
# (perl-http-daemon is required by perl-http-message)
# (perl-http-negotiate is required by perl-http-message)
# 
sudo pacman -R perl-http-message perl-http-negotiate perl-http-daemon perl-http-cookies icoutils playonlinux perl-libwww
#NOTE: xfdesktop (Xfce) depends on exo, so have to remove Xfce
# (perl-moo is required by perl-devel-globaldestruction)
# (perl-devel-globaldestruction is required by perl-sub-exporter-progressive, and both are required by slic3r)
# (perl-libwww is required by perl-encode-locale and perl-http-message)
# (perl-http-message is required by perl-encode-locale)
sudo pacman -R perl-devel-globaldestruction perl-moo perl-sub-exporter-progressive perl-sub-quote perl-encode-locale 
sudo pacman -S --noconfirm perl-libwww
sudo pacman -S --noconfirm perl-devel-globaldestruction perl-moo perl-sub-exporter-progressive perl-sub-quote perl-encode-locale
sudo pacman -S --noconfirm icoutils playonlinux
#INTERESTING NOTE TO slic3r developers: "Only use Sub::Exporter if you need it" is description of perl-sub-exporter-progressive package
#(below provides IO:Scalar)
sudo pacman -R perl-io-stringy
sudo pacman -S --noconfirm perl-io-stringy

#Then build succeeds, but can't run.
# Run command (in application menu icon) is: env LC_ALL=C slic3r.pl --gui
# which doesn't work yet and reveals more breakages: "Can't locate Wx.pm", "Can't locate URI.pm"
#don't remove it, otherwise perl-wx-opengl will get uninstalled too so instead use -S
#yaourt -R perl-wx
# however, package wasn't installed, even by the slic3r-git package
#perl-alien-wxwidgets says "LWP::Protocol::https is not installed" so:
yaourt -S --noconfirm perl-lwp-protocol-https
#perl-wx says Alien:wxWidgets is missing, so:
yaourt -S --noconfirm perl-alien-wxwidgets
yaourt -S --noconfirm perl-wx
#Slic3r says "Can't locate OpenGL.pm" so:
yaourt -S --noconfirm perl-opengl
#Slic3r says "Base class package "Wx::GLCanvas" is empty" so:
yaourt -S --noconfirm perl-wx-glcanvas

#sudo pacman -R perl-http-message perl-http-negotiate perl-http-daemon perl-http-cookies icoutils playonlinux perl-libwww
#required by perl-uri: perl-libwww perl-http-message perl-www-robotrules

SLIC3R_ENABLE=false
if [ -f /usr/bin/vendor_perl/slic3r.pl ]; then
SLIC3R_ENABLE=true
fi
if SLIC3R_ENABLE ; then
yaourt -R slic3r-git
fi
#sudo pacman -R perl-uri perl-libwww perl-http-message perl-www-robotrules exo icoutils playonlinux perl-http-cookies perl-http-daemon perl-http-negotiate perl-uri exo perl-www-robotrules
sudo pacman -S --force perl-uri

if SLIC3R_ENABLE ; then
yaourt -S --noconfirm slic3r-git
fi
#Compiles successfully
# but running: env LC_ALL=C slic3r.pl --gui  # still fails:
#16:13:58: Warning: Mismatch between the program and library build versions detected.
#The library used 3.0 (wchar_t,compiler with C++ ABI 1010,wx containers,compatible with 2.8),
#and your program used 3.0 (wchar_t,compiler with C++ ABI 1011,wx containers,compatible with 2.8).
#No protocol specified
#16:13:58: Error: Unable to initialize GTK+, is DISPLAY set properly?
#Failed to initialize wxWidgets at /usr/share/perl5/vendor_perl/Slic3r/GUI.pm line 7.
#Compilation failed in require at /usr/share/perl5/vendor_perl/Slic3r/GUI.pm line 7.
#BEGIN failed--compilation aborted at /usr/share/perl5/vendor_perl/Slic3r/GUI.pm line 7.
#Compilation failed in require at (eval 152) line 1.

#see https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=840287
# * rebuild wxwidgets3.0 against GCC/libc updates
sudo pacman -S --force wxgtk
#Running slic3r still fails with "Can't locate HTTP/Date.pm" so:
sudo pacman -S --force --noconfirm perl-http-date
#Running slic3r still fails with "Can't locate OpenGL.pm"
# the package wasn't installed, not even by installing slic3r-git.

sudo pacman -S --force --noconfirm freeglut glu glew
# otherwise installing perl-opengl results in:
#run as `perl Makefile.PL help` to show user options
#$verbose set to 0 - enable by running as `perl Makefile.PL verbose`
#In order to test your GPU's capabilities, run this make under an X11 shell
#No protocol specified
#freeglut (./glversion): failed to open display ':0.0'
#make: *** [Makefile:24: glversion.txt] Error 1
#get_extensions: no extensions found in utils/glversion.txt
#OS unsupported

yaourt -S --force --noconfirm perl-opengl
#installed without --noconfirm, and edited /.../perl Makefile.PL line to add verbose at the end of the line, but that didn't reveal much (diff shown below):
#$verbose set to 1
#...
#found libs:
#    GL = 'GL'
#    GLU = 'GLU'
#    GLUT = 'glut'
#Testing for OpenGL Extensions
#Testing GLUT version
#...
#glversion: cd utils;make -f Makefile GLUT_LIB=glut GLUT_DEF=HAVE_GLUT  clean;make -f Makefile GLUT_LIB=glut GLUT_DEF=HAVE_GLUT 
#...
#rm -f glversion.txt
#rm -f glversion
#rm -f glversion.o
#cc -I/usr/include -I/usr/X11R6/include -I/usr/local/include -I/usr/openwin/include -DHAVE_GLUT -c glversion.c
#cc glversion.o -L/usr/lib -L/usr/X11R6/lib -L/usr/local/lib -L/usr/openwin/lib -L/usr/lib/xorg/modules -L/usr/X11R6/lib/modules -L/usr/lib/xorg/modules/extensions -L/usr/X11R6/lib/modules/extensions -lGL -lglut -lGLU -lXi -lXmu -lXext -lX11 -lm -o glversion
#chmod u+x glversion
#./glversion > glversion.txt

#NOTE: that glversion script uses freeglut to get version as shown by other output near that command's result
sudo pacman -S --force --noconfirm nvidia-utils
#didn't help.
sudo pacman -S --force --noconfirm freeglut
yaourt -S --force --noconfirm perl-opengl
yaourt -S --noconfirm slic3r-git
#try: env LC_ALL=C slic3r.pl --gui
#asks for (was not installed even after installing slic3r-git):
yaourt -S --force --noconfirm perl-wx-glcanvas


#Still get:
#warning on slic3r-git reinstall (which downgraded slic3r):

#WARNING: '/usr/lib/perl5/site_perl' contains data from at least 1 packages which will NOT be used by the installed perl #interpreter.
# -> Run the following command to get a list of affected packages: pacman -Qqo '/usr/lib/perl5/site_perl'
#result:
#hivex
#WARNING: '/usr/lib/perl5/vendor_perl' contains data from at least 18 packages which will NOT be used by the installed perl #interpreter.
# -> Run the following command to get a list of affected packages: pacman -Qqo '/usr/lib/perl5/vendor_perl'
#result:
#perl-constant-defer
#perl-extutils-cppguess
#perl-extutils-makemaker-aur
#perl-extutils-typemaps-default
#perl-extutils-xspp
#perl-math-clipper
#perl-math-convexhull
#perl-math-convexhull-monotonechain
#perl-math-geometry-voronoi
#perl-math-libm
#perl-math-planepath
#perl-module-build-withxspp
#perl-parse-registry
#perl-threads-aur

#so:
yaourt -R hivex
#sudo pacman -R perl-constant-defer perl-extutils-cppguess perl-extutils-makemaker-aur perl-extutils-typemaps-default perl-extutils-xspp perl-math-clipper perl-math-convexhull perl-math-convexhull-monotonechain perl-math-geometry-voronoi perl-math-libm perl-math-planepath perl-module-build-withxspp perl-parse-registry perl-threads-aur
#HOWEVER, above fails since regripper-git requires perl-parse-registry
# and slic3r requires most other things
#The problem may be that both pacman and AUR versions are marked as installed
#so instead:
sudo pacman -R regripper-git
sudo pacman -R slic3r-git perl-constant-defer perl-extutils-cppguess perl-extutils-makemaker-aur perl-extutils-typemaps-default perl-extutils-xspp perl-math-clipper perl-math-convexhull perl-math-convexhull-monotonechain perl-math-geometry-voronoi perl-math-libm perl-math-planepath perl-module-build-withxspp perl-threads-aur
yaourt -S --noconfirm slic3r-git
