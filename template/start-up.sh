#!/bin/bash

echo "export DISPLAY=:99" >> /home/user/.bashrc
source /home/user/.bashrc

Xvfb $DISPLAY -ac -screen 0 1024x768x24 &
/usr/bin/xfce4-session
# startxfce4