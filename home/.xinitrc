#!/bin/sh
userresources=$HOME/.Xresources
if [ -f "$userresources" ]; then
  xrdb -merge "$userresources"
fi
exec i3 --shmlog-size=26214400
