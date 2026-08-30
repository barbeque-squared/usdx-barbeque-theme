# barbeque.one theme

This repository hosts the generation scripts and source files for the `barbeque.one-Widescreen` theme as well as some of its skins.
It is a very minimalist theme for USDX, optimized for 16:9 displays.
It also includes various helper scripts to keep it in sync with USDX' Modern theme.

**Warning: this theme is specifically for my local builds. 
It will work "close enough" on a stock USDX, and you are welcome to provide feedback on changes that you like or dislike, but not everything works out of the box on a stock USDX.**

## Requirements
* python
* bash
* imagemagick
* inkscape
* diffuse

## How to use
1. You will need to have [USDX](https://github.com/UltraStar-Deluxe/USDX) cloned and kept up-to-date
2. Copy `sourceme.example.sh` to `sourceme.sh` and give it the path of wherever you checked out USDX
3. Run `generate.sh`

This will generate any required images in the `temp` directory.
The `build` directory will contain the files and folders to be placed in USDX' `themes` directory (or you can symlink them!).

Theme generation is split into image generation and ini file generation.
The image generation step can be commented out in `generate.sh` if your input did not change.

The `gitdiffsrc.sh` is there to keep `src/blocks-git` and in turn `src/blocks` somewhat in sync with USDX' Modern theme.

## Known issues
Do not report these, they are known and require work in USDX itself.

### The awesome/bad/perfect end-of-line popups during singing are in the top-left corner
This theme does not use them.
The entire functionality is commented out in my local builds.
USDX defaults to then placing them at 0, 0.

### Some fonts are overflowing
Font rendering is different in my local builds, where they are not stretched.

### The oscilloscope is barely visible
In my local builds, oscilloscopes are drawn with the highest possible contrast (i.e. black or white) to some other color.
There is currently no functionality for this in USDX.

### The oscilloscope is hidden behind the scores
USDX always make the score 5 digits, my local build does not.

### Empty space on singing screen
Currently, the area where the notes are drawn is hardcoded in USDX.
In my local build this is hardcoded to a slightly bigger area.

## Future
Eventually I hope to start updating the Modern theme that USDX ships with in this direction.
