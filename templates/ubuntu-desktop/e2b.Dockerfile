FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN yes | unminimize

RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install \
    # UI Requirements
    xfce4 \
    xfce4-panel \
    xfce4-goodies \
    xfce4-terminal \
    xfce4-session \
    xvfb \
    xterm \
    xdotool \
    scrot \
    imagemagick \
    sudo \
    mutter \
    x11vnc \
    # Python/pyenv reqs
    build-essential \
    libssl-dev  \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    curl \
    wget \
    git \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libxml2-dev \
    libxmlsec1-dev \
    libffi-dev \
    liblzma-dev \
    # Network tools
    net-tools \
    netcat \
    # PPA req
    software-properties-common && \
    # Userland apps
    sudo add-apt-repository ppa:mozillateam/ppa && \
    sudo apt-get install -y --no-install-recommends \
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
COPY ./xfce4-desktop.xml /root/.config/xfce4/xfconf/xfce-perchannel-xml
    
COPY ./start-up.sh /
RUN chmod +x /start-up.sh

ENV DPI=96
ENV WIDTH=1024
ENV HEIGHT=768
ENV DISPLAY=:0