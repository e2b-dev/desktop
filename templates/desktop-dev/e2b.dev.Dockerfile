FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN yes | unminimize

RUN apt-get update && \
    apt-get -y upgrade

# Basic system tools
RUN apt-get -y install \
    sudo \
    curl \
    wget \
    git

# Network tools
RUN apt-get -y install \
    net-tools \
    netcat

# UI Requirements
RUN apt-get -y install \
    xfce4 \
    xfce4-goodies \
    xfce4-terminal \
    xfce4-panel \
    xfce4-session \
    xvfb \
    xterm \
    xdotool \
    scrot \
    imagemagick \
    mutter \
    x11vnc

# Python/pyenv reqs
RUN apt-get -y install \
    build-essential \
    libssl-dev  \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev

# PPA req
RUN apt-get -y install \
    software-properties-common

# Userland apps
RUN add-apt-repository ppa:mozillateam/ppa && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    firefox-esr \
    x11-apps \
    xpdf \
    gedit \
    xpaint \
    tint2 \
    galculator \
    pcmanfm \
    unzip && \
    apt-get clean

# Install noVNC
RUN git clone --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

# Set custom wallpaper
RUN mkdir -p /usr/share/backgrounds/xfce
COPY ./wallpaper.png /usr/share/backgrounds/xfce
RUN mkdir -p /root/.config/xfce4/xfconf/xfce-perchannel-xml
COPY ./xfce4-desktop.dev.xml /root/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml

COPY ./start-up.dev.sh /
RUN chmod +x /start-up.dev.sh