FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBIAN_PRIORITY=high

RUN apt-get update && \
    apt-get -y upgrade && \
    yes | unminimize

RUN apt-get update && apt-get -y install \
    # Basic tools
    sudo curl wget git vim \
    # Network tools
    net-tools netcat \
    # UI Requirements
    xfce4 xfce4-goodies xfce4-terminal xfce4-panel xfce4-session \
    xauth xvfb xterm xdotool scrot imagemagick mutter x11vnc ffmpeg \
    # Python/pyenv reqs
    build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
    libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev \
    libxmlsec1-dev libffi-dev liblzma-dev python3-pip python3-tk \
    python3-dev python-is-python3 \
    # PPA req
    software-properties-common

RUN pip install numpy

RUN git clone --branch v1.5.0 https://github.com/novnc/noVNC.git /opt/noVNC && \
    git clone --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html

COPY ./wallpaper.png /usr/share/backgrounds/xfce/wallpaper.png

COPY ./Xauthority /home/user/.Xauthority

COPY ./45-allow-colord.pkla /etc/polkit-1/localauthority/50-local.d/45-allow-colord.pkla

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
    gnumeric \
    pcmanfm \
    unzip && \
    apt-get clean

# Install vscode
RUN apt update -y \
    && apt install -y software-properties-common apt-transport-https wget \
    && wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && add-apt-repository -y "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" \
    && apt update -y \
    && apt install -y code