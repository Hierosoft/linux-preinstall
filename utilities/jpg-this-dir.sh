#!/bin/sh

customDie() {
cat <<END
ERROR:
  $@
END
exit 1
}

usage() {
cat > ~/jpg-this-dir.txt <<END

You must specify a directory or file.
- If directory: This script will convert all png files in the directory
  to jpg, then the png files will be moved to a directory called "png"
- If file: the above steps will be taken on the directory that contains
  the file.


END
open ~/jpg-this-dir.txt
}


if [ -z "$1" ]; then
    usage
    exit 1
fi
parentdir=""
if [ ! -d "$1" ]; then
    if [ ! -f "$1" ]; then
        usage
        exit 1
    else
        parentDir="$(dirname "$1")"
    fi
else
    parentDir="$1"
fi
if [ ! -d "$parentDir/png" ]; then
    mkdir "$parentDir/png" || customDie "Cannot create png directory"
fi

# see https://superuser.com/questions/71028/batch-converting-png-to-jpg-in-linux
# ls -1 *.png | xargs -n 1 bash -c 'convert "$0" "${0%.*}.jpg"' # this is good too
convert_count=0
convert_failed_count=0
mv_count=0
mv_failed_count=0
echo "Converting (moving only successfully converted files)..."
echo "#!/bin/sh" > ~/jpg-this-dir.txt
echo "# `date`" > ~/jpg-this-dir.txt
cd "$parentDir" || customDie "cd $parentDir  # FAILED"
for i in *.png
do
    failed=false
    convert "$i" "${i%.*}.jpg" || failed=true
    if [ "@$failed" = "@true" ]; then
        echo "convert \"$i\" \"${i%.*}.jpg\"" >> ~/jpg-this-dir.txt
        echo "#       ^ failed" >> ~/jpg-this-dir.txt
        convert_failed_count=$((convert_failed_count+1))
    else
        echo "# convert \"$i\" \"${i%.*}.jpg\"" >> ~/jpg-this-dir.txt
        echo "# # ${i%.*}.jpg successful"
        convert_count=$((convert_count+1))
        failed=false
        mv -f "$parentDir/$i" "$parentDir/png/" || failed=true
        if [ "@$failed" = "@true" ]; then
            echo "mv -f \"$parentDir/$i\" \"$parentDir/png/\"" >> ~/jpg-this-dir.txt
            echo "#     ^ failed" >> ~/jpg-this-dir.txt
            mv_failed_count=$((mv_failed_count+1))
        else
            echo "# mv -f \"$parentDir/$i\" \"$parentDir/png/\"" >> ~/jpg-this-dir.txt
            echo "# # successful"
            mv_count=$((mv_count+1))
        fi
        # echo "Moving $i..."

    fi
done
echo "# Converted $convert_count ($convert_failed_count failed)." >> ~/jpg-this-dir.txt
echo "# Moved $mv_count ($mv_failed_count failed)." >> ~/jpg-this-dir.txt
open ~/jpg-this-dir.txt
echo "Done."
echo
echo
