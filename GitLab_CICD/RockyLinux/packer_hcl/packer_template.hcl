packer {
  required_plugins {
    vsphere = {
      version = ">= 1.0"
      source  = "github.com/hashicorp/vsphere"
    }
  }
}

source "vsphere-iso" "custom_vm" {
  vcenter_server      = "your-vcenter-server"
  username           = "your-username"
  password           = "your-password"
  datacenter         = "your-datacenter"
  datastore          = "your-datastore"
  iso_url            = "file:///path/to/custom.iso"
  iso_checksum       = "your-checksum"
  kickstart_file     = "file:///path/to/kickstart.cfg"
  guest_os_type      = "centos7_64Guest"
  vm_name            = "CustomVM"
  disk_size          = 40960
}

build {
  sources = ["source.vsphere-iso.custom_vm"]
}