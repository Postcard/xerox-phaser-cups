#!/bin/bash

# Start Wifi Access Point if WIFI_ON
if [ "$WIFI_ON" = 1 ]; then
    /etc/init.d/cups stop
    export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
    sleep 15 # Delay needed to avoid DBUS introspection errors
    node /usr/src/app/resin-wifi-connect/src/app.js --clear=false
    /etc/init.d/cups start
fi

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