#!/bin/bash

# Variables
ISO_URL="https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.3-x86_64-dvd.iso"
ISO_NAME="Rocky-9.3-x86_64-dvd.iso"
CUSTOM_ISO_NAME="Rocky-9.3-x86_64-custom.iso"
WORK_DIR="custom_iso"
KS_FILE="ks.cfg"

# Download the official Rocky Linux ISO
wget $ISO_URL -O $ISO_NAME

# Create working directory
mkdir -p $WORK_DIR

# Mount the ISO
sudo mount -o loop $ISO_NAME /mnt/iso

# Copy ISO contents to working directory
cp -rT /mnt/iso $WORK_DIR

# Unmount the ISO
sudo umount /mnt/iso

# Add Kickstart file to the working directory
cp $KS_FILE $WORK_DIR/

# Modify bootloader to use the Kickstart file
sed -i '/append/ s/$/ inst.ks=cdrom:\/$KS_FILE/' $WORK_DIR/isolinux/isolinux.cfg

# Rebuild the ISO
mkisofs -o $CUSTOM_ISO_NAME \
  -b isolinux/isolinux.bin \
  -c isolinux/boot.cat \
  -no-emul-boot -boot-load-size 4 -boot-info-table \
  -J -R -V "Custom_Rocky_Linux" $WORK_DIR

# Clean up
rm -rf $WORK_DIR
rm $ISO_NAME
