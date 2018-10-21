#!/bin/bash
BOOTSCRIPT=$PWD/src/init.d_shell_main-mqtt
INSTALL=/etc/init.d/inftable-lights

if [ ! -f $INSTALL ]; then
    echo "Existing boot script found, replacing"
    rm $INSTALL
fi

echo "Copying $BOOTSCRIPT"
echo "to $INSTALL"
cp $BOOTSCRIPT $INSTALL