#!/bin/sh
set -e
# debug
#set -x
source ./sourceme.sh

mkdir -p build temp
# generating the images is in a separate script
# so it can be disabled if you're only debugging ini-related things
./generate-images.sh

# generate custom themes
(cd src/generate-theme && ./write.py)
# barbeque.one Widescreen
mv src/generate-theme/barbeque.one-Widescreen.ini temp/.

# add theme variants
cp src/theme-variants/*.ini build/.

# make themes work on dev git
DEVGIT="${USDX_GIT}/game/themes"
rm -rf themes/*
for i in barbeque.one-Widescreen; do
  mkdir -p "themes/${i}"
  cp "temp/${i}.ini" "themes/${i}.ini"
  # copy USDX theme
  cp --preserve=mode "${DEVGIT}/Modern/"* "themes/${i}/".
  # Remove default skins and SOME now unnecessary images
  rm -f "themes/${i}/"*.ini
  rm -f "themes/${i}/"'[bg-'*
  # modify with our stuff
  cp --preserve=mode build/* "themes/${i}/".
  sed -i "s/Theme=Modern/Theme=${i}/" "themes/${i}/"*.ini
done
