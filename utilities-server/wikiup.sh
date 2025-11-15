#!/bin/bash -e
usage(){
    cat<<END
wikiup <mediawiki-version.a> <mediawiki-version.b>
END
}


src="$1"
dst="$2"
if [ -z "$src" ]; then
  >&2 echo "Error: no source"
  exit 1
fi
if [ -z "$dst" ]; then
  >&2 echo "Error: no destination"
  exit 1
fi

if [ -z "$WWW_DIR" ]; then
  WWW_DIR="public_html"
fi

if [ -e "$WWW_DIR" ]; then
  if [ ! -L "$WWW_DIR" ]; then
    >&2 echo "Error: public_html is not a symlink. This script assumes it is the symlink to the latest version. Otherwise set WWW_DIR to something else, and it will become a link to $dst."
  fi
fi


if [ ! -d "$src/images" ]; then
  >&2 echo "Error: already moved $src/images"
  exit 2
fi
if [ -d "$dst/images" ]; then
  if [ -d "$dst/images.1st" ]; then
    >&2 echo "Error: already backed up stock images $dst/images"
    exit 3
  else
    mv "$dst/images" "$dst/images.1st"
  fi
else
  echo "Error: no stock $dst/images"
  exit 4
fi

mv "$src/images" "$dst/"
echo "Moved $src/images to $dst/"
if [ "$dst/LocalSettings.php" ]; then
  if [ "$dst/LocalSettings.php.1st" ]; then
    echo "Error: $dst/LocalSettings.php.1st (backup of stock) already exists."
    exit 5
  else
    cp "$dst/LocalSettings.php" "$dst/LocalSettings.php.1st"
  fi
else
  >&2 echo "Error: No stock $dst/LocalSettings.php"
fi
cp "$src/LocalSettings.php" "$dst/"

if [ -e "$WWW_DIR" ]; then
  rm "$WWW_DIR"
  ln -s $dst "$WWW_DIR"
  echo "* Made $WWW_DIR a symlink to $dst."
fi

echo "* If you have set a custom $wgUploadDirectory (default is false), you must back move it from $src to $dst manually now."
echo "* After you have transferred any custom upload directory ($wgUploadDirectory), deleted file archives, and any custom skins, run the database upgrade script that is included in $dst with the correct php version such as via (replace php with the correct php version!):"
echo "  cd maintenance"
echo "  php7.3 update.php"
echo "* Extensions usually need to be upgraded at the same time as the MediaWiki core."
