import atexit
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def main():
    context = ssl._create_unverified_context()
    si = SmartConnect(host="your-vsphere-server", user="your-username", pwd="your-password", sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()

    datacenter = get_obj(content, [vim.Datacenter], "your-datacenter")
    cluster = get_obj(content, [vim.ClusterComputeResource], "your-cluster")
    resource_pool = cluster.resourcePool
    datastore = get_obj(content, [vim.Datastore], "your-datastore")

    vm_folder = datacenter.vmFolder
    vm_name = "custom-vm"
    vm_config = vim.vm.ConfigSpec(
        name=vm_name,
        memoryMB=2048,
        numCPUs=2,
        guestId="centos7_64Guest",
        files=vim.vm.FileInfo(vmPathName=f"[{datastore.name}]"),
        deviceChange=[
            vim.vm.device.VirtualDeviceSpec(
                operation=vim.vm.device.VirtualDeviceSpec.Operation.add,
                device=vim.vm.device.VirtualCdrom(
                    backing=vim.vm.device.VirtualCdrom.IsoBackingInfo(
                        fileName="[datastore] path/to/custom.iso"
                    ),
                    connectable=vim.vm.device.VirtualDevice.ConnectInfo(
                        startConnected=True,
                        allowGuestControl=True
                    )
                )
            )
        ]
    )

    task = vm_folder.CreateVM_Task(config=vm_config, pool=resource_pool)
    task.info.state

if __name__ == "__main__":
    main()
