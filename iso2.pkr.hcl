
variable "iso_url" {
  default = "https://download.rockylinux.org/pub/rocky/9/isos/x86_64/Rocky-9.3-x86_64-dvd.iso"
}

source "null" "iso_customizer" {
  communicator = "none"
}

build {
  name = "rocky-linux-custom-iso"

  sources = ["source.null.iso_customizer"]

  provisioner "file" {
    source      = "ks.cfg"
    destination = "ks.cfg"
  }

  provisioner "shell-local" {
    inline = [
      "mkdir -p iso_mount iso_extract custom_iso",
      "mount -o loop ${var.iso_url} iso_mount",
      "cp -rT iso_mount iso_extract",
      "cp ks.cfg iso_extract/",
      "xorriso -as mkisofs -o custom_iso/RockyLinux-Custom.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table -R -J -v -T iso_extract",
      "umount iso_mount",
      "rm -rf iso_mount iso_extract"
    ]
  }
}
```

---

### 📄 Kickstart File (`ks.cfg`)

Here’s a minimal example:

```bash
#version=RHEL9
install
lang en_US.UTF-8
keyboard us
timezone America/New_York --isUtc
rootpw --plaintext yourpassword
auth --useshadow --passalgo=sha512
selinux --enforcing
firewall --enabled
network --bootproto=dhcp --device=eth0 --onboot=on
reboot
%packages
@core
%end
```

---

##