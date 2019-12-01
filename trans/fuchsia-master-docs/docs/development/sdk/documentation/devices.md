 
# Working with target devices  使用目标设备 

 
## Connecting to a device  连接到设备 

Fuchsia target devices must be connected to a host device via a network link. SSH is the protocol for communications over that link, as described in[this document](ssh.md). 紫红色的目标设备必须通过网络链接连接到主机设备。 SSH是通过该链接进行通信的协议，如[本文档]（ssh.md）中所述。

 
### Getting the device address  获取设备地址 

Getting the Fuchsia device address can be done using mDNS. Methods for device discovery are outlined in [this document](device_discovery.md) 可以使用mDNS获得Fuchsia设备的地址。 [本文档]（device_discovery.md）中概述了设备发现的方法。

 
## Flashing a device  闪烁设备 

In order to flash a device, start a [bootserver](bootserver.md) on the host and restart the device into its bootloader. 为了刷新设备，请在主机上启动[bootserver]（bootserver.md），然后将设备重新启动到其Bootloader中。

 
## Installing software onto a device  将软件安装到设备上 

The unit of installation on Fuchsia is a package. For information on how to push packages to a Fuchsia device, see the[this document](packages.md). 紫红色的安装单元是一个包装。有关如何将软件包推送到Fuchsia设备的信息，请参见[本文档]（packages.md）。

 
## Getting logs from a device  从设备获取日志 

