 
# `dev_finder`  `dev_finder` 

`dev_finder` is the command line tool for device discovery. It uses mDNS to find Fuchsia devices. dev_finder是用于设备发现的命令行工具。它使用mDNS查找紫红色的设备。

Currently only Linux is supported. For Mac users see the "For Mac Users" section. 当前仅支持Linux。对于Mac用户，请参阅“对于Mac用户”部分。

 
## For Linux Users  对于Linux用户 

 
### Finding all Devices  查找所有设备 

The simplest way to get all the devices on the network by their address is to run 通过地址获取网络上所有设备的最简单方法是运行

```
$ ./dev_finder list
192.168.42.156
```
 

This will give you the addresses of all Fuchsia devices on the network. If you'd like to get their hostnames as well as their addresses, you can include the`-full` flag. 这将为您提供网络上所有Fuchsia设备的地址。如果您想获取他们的主机名和地址，则可以包含-full标志。

 
### Finding devices by hostname  按主机名查找设备 

If you'd like to find your device by its unique hostname (e.g. `lunch-feta-stool-woozy`) you can use the `resolve` command: 如果您想通过设备的唯一主机名（例如“ lunch-feta-stool-woozy”）查找设备，则可以使用“ resolve”命令：

```
$ ./dev_finder resolve lunch-feta-stool-woozy
192.168.42.156
```
 

 
### Finding the Interface Connected to the Device  查找连接到设备的接口 

To find the interface connected to the device, include the `-local` flag to either the `list` command or the `resolve` command, which will give you theaddress that the Fuchsia device can use to connect to your host. 要查找连接到该设备的接口，请在list命令或resolve命令中包含“ -local”标志，这将为您提供Fuchsia设备可用于连接到主机的地址。

 
## For Mac Users  对于Mac用户 

For those on Mac hosts, you can use the included `dns-sd` command to find your device. Here's an example command along with the output you should see when adevice is on your network: 对于Mac主机上的主机，可以使用随附的`dns-sd`命令来查找设备。这是一个示例命令，以及设备在网络上时应显示的输出：

```
$ dns-sd -B _fuchsia._udp .
Browsing for _fuchsia._udp
DATE: ---Fri 14 Dec 2018---
15:28:21.447  ...STARTING...
Timestamp     A/R    Flags  if Domain       Service Type   Instance Name
15:28:21.448  Add        2   7 local.       _fuchsia._udp. quake-agile-lurk-even
```
 

