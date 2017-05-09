

echo "Installing Xerox Printer Phaser 7100D"

lpadmin \
    -p 'Xerox_Phaser_7100N' \
    -v 'usb://Xerox/Phaser%207100N?serial=026552' \
    -P '/usr/share/ppd/Xerox_Phaser_7100N.ppd' \
    -o 'PageSize=A3' \
    -o 'StpQuality=High' \
    -o 'Duplex=DuplexNoTumble' \
    -E

while true; do sleep 1; done