#!/bin/bash
set -e

TMPFILE='/tmp/usdxthemediff'
# create a tmpfile and have it be deleted if/when the script exits
>$TMPFILE
function cleanup {
  rm -f $TMPFILE
}

cd src/generate-theme

# manually make changes to blocks-git...
cat blocks-git/* > $TMPFILE
diffuse ~/gits/Ultrastar/USDX/game/themes/Modern.ini $TMPFILE

# ...then open a diff editor for every block that has changes
# NOT ALL BLOCKS ARE ACTUALLY USED!!! KEEP THIS IN SYNC!
for i in 00 02 03 07 08 34 36 41 51; do
  cmp --silent blocks-git/$i-*.ini blocks/$i-*.ini || diffuse blocks-git/$i-*.ini blocks/$i-*.ini
done
