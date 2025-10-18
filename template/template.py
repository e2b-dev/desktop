from e2b import CopyItem, Template

template = (
    Template(file_context_path="files")
    .from_image("ubuntu:22.04")
    .set_user("root")
    .set_workdir("/")
    .set_envs(
        {
            # Avoid system prompts
            "DEBIAN_FRONTEND": "noninteractive",
            "DEBIAN_PRIORITY": "high",
            # Pip settings
            "PIP_DEFAULT_TIMEOUT": "100",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1",
            "PIP_NO_CACHE_DIR": "1",
        }
    )
    # Initial system setup and packages
    # We are not using .apt_install() here because some packages have interactive prompts (keyboard layout setup, etc.)
    .run_cmd(
        [
            "yes | unminimize",
            "apt-get update",
            "apt-get install -y \
                xserver-xorg \
                x11-xserver-utils \
                xvfb \
                x11-utils \
                xauth \
                xfce4 \
                xfce4-goodies \
                util-linux \
                sudo \
                curl \
                git \
                wget \
                python3-pip \
                xdotool \
                scrot \
                ffmpeg \
                x11vnc \
                net-tools \
                netcat \
                x11-apps \
                libreoffice \
                xpdf \
                gedit \
                xpaint \
                tint2 \
                galculator \
                pcmanfm \
                software-properties-common \
                apt-transport-https \
                libgtk-3-bin",
        ]
    )
    .pip_install("numpy")
    # Setup NoVNC and websockify
    .run_cmd(
        [
            "git clone --branch e2b-desktop https://github.com/e2b-dev/noVNC.git /opt/noVNC",
            "ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html",
            "git clone --branch v0.12.0 https://github.com/novnc/websockify ./opt/noVNC/utils/websockify",
        ]
    )
    # Install browsers and set up repositories
    .run_cmd(
        [
            "add-apt-repository ppa:mozillateam/ppa",
            "wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -",
            'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list',
            "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add -",
            'add-apt-repository -y "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"',
            "apt-get update",
        ],
    )
    # Install browsers and VS Code
    .apt_install(["firefox-esr", "google-chrome-stable", "code"])
    # Configure system settings
    .run_cmd(
        [
            "ln -sf /usr/bin/xfce4-terminal.wrapper /etc/alternatives/x-terminal-emulator",
            "update-alternatives --set x-www-browser /usr/bin/firefox-esr",
            "mkdir -p /home/user/.config/Code/User",
            "mkdir -p /home/user/.config/xfce4/xfconf/xfce-perchannel-xml/",
            "update-desktop-database /usr/share/applications/",
        ],
    )
    # Copy all configuration files
    .copy_items(
        [
            CopyItem(
                src="google-chrome.desktop",
                dest="/usr/share/applications/google-chrome.desktop",
            ),
            CopyItem(
                src="settings.json",
                dest="/home/user/.config/Code/User/settings.json",
            ),
            CopyItem(
                src="wallpaper.png",
                dest="/usr/share/backgrounds/xfce/wallpaper.png",
            ),
            CopyItem(
                src="xfce4-desktop.xml",
                dest="/home/user/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml",
            ),
            CopyItem(
                src="firefox-policies.json",
                dest="/usr/lib/firefox-esr/distribution/policies.json",
            ),
            CopyItem(
                src="firefox-autoconfig.js",
                dest="/usr/lib/firefox-esr/defaults/pref/autoconfig.js",
            ),
            CopyItem(src="firefox.cfg", dest="/usr/lib/firefox-esr/firefox.cfg"),
        ]
    )
)

# Template with user and workdir set
template_with_user_workdir = template.set_user("user").set_workdir("/home/user")
