#!/bin/bash

: ${DPI:=96}
: ${WIDTH:=1024}
: ${HEIGHT:=768}

Xvfb :0 -ac -screen 0 ${WIDTH}x${HEIGHT}x24 -retro -dpi $DPI -nolisten tcp -nolisten unix &

wait_for_xvfb() {
    local timeout=10
    local start_time=$(date +%s)
    while ! xdpyinfo -display :0 >/dev/null 2>&1; do
        if [ $(($(date +%s) - start_time)) -gt $timeout ]; then
            echo "Xvfb failed to start within $timeout seconds" >&2
            return 1
        fi
        sleep 0.1
    done
    return 0
}

wait_for_xvfb

DISPLAY=:0 startxfce4 &

sleep 5

### --==[ VNC Server ]==--

: ${VNC_PORT:=5900}
: ${NOVNC_PORT:=6080}

# [wait_for_port <port> [<timeout>]]
wait_for_port() {
    local port=$1
    local timeout=${2:-10}
    local start_time=$(date +%s)
    
    while true; do
        if netstat -tuln | grep ":$port "; then
            return 0
        fi
        
        if [ $(($(date +%s) - start_time)) -gt $timeout ]; then
            echo "Timeout waiting for port $port after $timeout seconds" >&2
            return 1
        fi
        sleep 1
    done
}

start_x11vnc() {
    (x11vnc -display :0 \
        -forever \
        -wait 50 \
        -shared \
        -rfbport $VNC_PORT \
        $VNC_PW_FLAG \
        2>/tmp/x11vnc_stderr.log) &

    x11vnc_pid=$!

    # Wait for x11vnc to start
    wait_for_port $VNC_PORT

    (
        while true; do
            if ! kill -0 $x11vnc_pid 2>/dev/null; then
                echo "x11vnc process crashed, restarting..." >&2
                if [ -f /tmp/x11vnc_stderr.log ]; then
                    echo "x11vnc stderr output:" >&2
                    cat /tmp/x11vnc_stderr.log >&2
                    rm /tmp/x11vnc_stderr.log
                fi
                start_x11vnc
                return
            fi
            sleep 5
        done
    ) &
}

# Flag to handle authentication
VNC_PW_FLAG="-nopw"
if [ -n "$VNC_PASSWORD" ]; then
    mkdir -p ~/.vnc  # Password will be stored at ~/.vnc/passwd
    x11vnc -storepasswd "$VNC_PASSWORD" ~/.vnc/passwd
    VNC_PW_FLAG="-rbfauth ~/.vnc/passwd"
fi

start_x11vnc

/opt/noVNC/utils/novnc_proxy \
    --vnc localhost:$VNC_PORT \
    --listen $NOVNC_PORT \
    --web /opt/noVNC \
    > /tmp/novnc.log 2>&1 &

# Wait for noVNC to start
wait_for_port $NOVNC_PORT