#!/bin/bash

export DISPLAY=:0.0
export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket

# Start Wifi Access Point if WIFI_ON
if [ "$WIFI_ON" = 1 ]; then
    /etc/init.d/cups stop
    export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
    sleep 15 # Delay needed to avoid DBUS introspection errors
    node /usr/src/app/resin-wifi-connect/src/app.js --clear=false
    /etc/init.d/cups start
fi

# XORG SECTION

# rotate screen if env variable is set [normal, inverted, left or right]
if [[ ! -z "$ROTATE_DISPLAY" ]]; then
  echo "YES"
  (sleep 3 && DISPLAY=:0 xrandr -o $ROTATE_DISPLAY) & 
fi

# start firefox
echo "STARTING X"
startx /usr/src/app/firefox/firefox --width $WINDOW_WIDTH --height $WINDOW_HEIGHT --kiosk https://figure.co/print -- -nocursor

# #disable screen saving
# sleep 5
# xset -display :0 -dpms

# END OF XORG SECTION

FOO=${BRIGHTNESS:-700}

echo "Installing Xerox Printer Phaser 7100D"

lpadmin \
    -p 'Xerox_Phaser_7100N' \
    -v 'usb://Xerox/Phaser%207100N?serial=026552' \
    -P '/usr/share/ppd/Xerox_Phaser_7100N.ppd' \
    -o 'ColorModel=Gray' \
    -o 'StpQuality='${QUALITY:-Standard} \
    -o 'Duplex=DuplexNoTumble' \
    -o 'StpBrightness='${BRIGHTNESS:-700} \
    -o 'StpContrast='${CONTRAST:-1100} \
    -o 'StpImageType=Photo' \
    -E

python -m xerox_phaser_cups