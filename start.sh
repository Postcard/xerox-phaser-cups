

echo "Installing Xerox Printer Phaser 7100D"

lpadmin \
    -p 'Xerox_Phaser_7100N' \
    -v 'usb://Xerox/Phaser%207100N?serial=026552' \
    -P '/usr/share/ppd/Xerox_Phaser_7100N.ppd' \
    -o 'ColorModel=Gray' \
    -o 'StpQuality=Standard' \
    -o 'Duplex=DuplexNoTumble' \
    -o 'StpBrightness=700' \
    -o 'StpContrast=1100' \
    -o 'StpImageType=Photo' \
    -E

python -m xerox_phaser_cups