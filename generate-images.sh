#!/bin/sh
set -e
# debug
#set -x

# separate from the main generate script because these can take quite some time

rm -rf build/*
rm -rf temp/*
mkdir -p build temp

# create temp images
# MLK @ GC2024
magick -background none -fill white -font "DejaVu-Sans-Condensed-Bold" -pointsize 20 label:"barbeque.one         usdx.eu                 mylittlekaraoke.com" -trim temp/mlk-gc2024-urls.png

# create actual images
# backgrounds
# My Little Karaoke @ GalaCon 2024
cp src/images/mlk/Card.jpg build/[bg-load]mlk-gc2024.jpg
magick src/images/mlk/background.jpg -fill black -colorize 60 temp/[bg-main]mlk-gc2024.jpg
composite -gravity northeast -geometry +20+00 src/images/mlk/Logo_mini_RGB.png temp/[bg-main]mlk-gc2024.jpg temp/[bg-main]mlk-gc2024.jpg
composite -gravity northeast -geometry +2+2 temp/mlk-gc2024-urls.png temp/[bg-main]mlk-gc2024.jpg temp/[bg-main]mlk-gc2024.jpg
cp temp/[bg-main]mlk-gc2024.jpg build/[bg-main]mlk-gc2024.jpg

# note area
# to-be-sung notes
magick -size 16x32 xc:transparent -fill "rgb(40,180,80)" -draw 'fill #ffffff88 rectangle 0,0 15,1 fill #00000088 rectangle 0,30 15,31' -draw 'rectangle 0,2 15,29' build/[sing]notesPlainMid.png
magick -size 16x32 xc:transparent -fill "rgb(40,180,80)" -draw 'fill #ffffff88 circle 15,15 15,30 fill #00000088 circle 15,17 15,31' -draw 'circle 16,16 16,30' build/[sing]notesPlainLeft.png
magick build/[sing]notesPlainLeft.png -flop build/[sing]notesPlainRight.png

# singbar (the thing beneath the scores)
# singbar v2: just only draw the bar
magick -size 128x16 xc:'#00000000' build/[sing]singBarBack.png
magick -size 16x16 xc:'#ffffff88' build/[sing]singBarBar.png
magick -size 128x16 xc:'#ffffff00' build/[sing]singBarFront.png
# ball icon
magick -size 45x45 xc:transparent -draw 'fill black circle 22,22 22,44' -draw 'fill white circle 22,22, 22,39' build/[sing]LyricsBall.png

# keyboard
declare -A keys100
keys100[C]=c
keys100[J]=j
keys100[M]=m
keys100[P]=p
keys100[R]=r

declare -A keys150
keys150["1..3"]=13
keys150[Alt]=alt
keys150[Del]=del
keys150[⏎]=enter
keys150[Esc]=esc
keys150[Ins]=ins
keys150["↔↕"]=navi

declare -A keys175
keys175["A..Z"]=az

for i in "${!keys100[@]}"; do
  cat src/key-1-100-blank.svg | sed "s/TEXT/$i/" | inkscape --pipe --export-filename="build/[button]${keys100[$i]}.png" --export-height=64
done
for i in "${!keys150[@]}"; do
  cat src/key-1-150-blank.svg | sed "s/TEXT/$i/" | inkscape --pipe --export-filename="build/[button]${keys150[$i]}.png" --export-height=64
done
for i in "${!keys175[@]}"; do
  cat src/key-1-175-blank.svg | sed "s/TEXT/$i/" | inkscape --pipe --export-filename="build/[button]${keys175[$i]}.png" --export-height=64
done

# other icons
cp src/cd-512.png build/[icon]cd.png

# pause
magick -background none -fill white -font "DejaVu-Sans-Condensed-Bold" -pointsize 288 label:Pause -trim \
  \( +clone -background black -shadow 100x3+0+0 -channel A -level 0,50% +channel \) +swap \
  +repage -gravity center -composite build/[sing]pause.png

# lyric/time bars
inkscape src/sing-textbar.svg --export-filename="build/[sing]textBar.png"
inkscape src/sing-textbar-top.svg --export-filename="build/[sing]textBarDuet.png"
magick -size 1x1 xc:'#000000ff' "build/[sing]timeBarBG.png"

# default cover
# MLK @ GC2024
cp src/images/mlk/Card-crop-for-songCover.jpg build/[main]songCover-mlk-gc2024.jpg

# dummy images to replace ones that are now obsolete
magick -size 1x1 xc:'#00000000' build/[score]rating_0.png
for i in {1..7}; do
  cp build/[score]rating_0.png "build/[score]rating_${i}.png"
done
