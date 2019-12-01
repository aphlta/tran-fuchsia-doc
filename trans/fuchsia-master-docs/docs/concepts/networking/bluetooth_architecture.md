 
# The Bluetooth System  蓝牙系统 

The Fuchsia Bluetooth system ([source layout](bluetooth_source_layout.md)) aims to provide a dual-mode implementation of theBluetooth Host Subsystem versions 4.2 and 5.0+. This includes 紫红色的蓝牙系统（[source layout]（bluetooth_source_layout.md））旨在提供蓝牙主机子系统版本4.2和5.0+的双模式实现。这包括

 
- A framework for developing Bluetooth Low Energy applications in central, peripheral, broadcaster, and scanner roles. -用于在中央，外围设备，广播和扫描仪角色中开发低功耗蓝牙应用程序的框架。

 
- DDK interfaces for building LE and Traditional service drivers that have high throughput requirements. -DDK接口，用于构建对吞吐量有较高要求的LE和传统服务驱动程序。

 
- A DDK surface for building vendor-specific HCI drivers to support a wide range of Bluetooth controllers as well as generic transport drivers. -DDK表面，用于构建特定于供应商的HCI驱动程序，以支持各种蓝牙控制器以及通用传输驱动程序。

 
- Services for policy and management to integrate a system with the Generic Access Profile. -用于将系统与通用访问配置文件集成在一起的策略和管理服务。

 
## Device Stack  设备堆栈 

Bluetooth controllers that are present on the system surface as a hierarchy of devices. On an x86 platform this hierarchy may look like the following: 作为设备层次结构存在于系统表面上的Bluetooth控制器。在x86平台上，此层次结构可能如下所示：

```
[pci] pid=1633 /boot/driver/bus-acpi.so
   [00:14.0] pid=1633 /boot/driver/bus-pci.so
      <00:14.0> pid=2179 /boot/driver/bus-pci.proxy.so
         [xhci] pid=2179 /boot/driver/xhci.so
            [usb] pid=2179 /boot/driver/usb-bus.so
               [005] pid=2179 /boot/driver/usb-bus.so
                  [ifc-000] pid=2179 /boot/driver/usb-bus.so
                     [bt_transport_usb] pid=2179 /boot/driver/bt-transport-usb.so
                        [bthci-passthrough] pid=2179 /system/driver/bthci-passthrough.so
                           [bt-host] pid=2179 /system/driver/bthost.so
```
 

 
### HCI  人机交互 

Generic HCI transport functionality is provided by the `bt-transport` protocol. Bluetooth provides drivers that implement the HCI transport over[USB](/src/connectivity/bluetooth/hci/transport/usb/)and [UART](/src/connectivity/bluetooth/hci/transport/uart/).The transport protocol abstracts the HCI control, ACL, and SCOchannels (currently as Zircon [channels](/docs/concepts/objects/channel.md)). bt-transport协议提供了通用的HCI传输功能。蓝牙提供了驱动程序，用于通过[USB]（/ src / connectivity / bluetooth / hci / transport / usb /）和[UART]（/ src / connectivity / bluetooth / hci / transport / uart /）实现HCI传输。传输协议抽象HCI控件，ACL和SCOchannel（当前为Zircon [channel]（/ docs / concepts / objects / channel.md））。

A transport driver publishes a bt-transport device (e.g. `/dev/class/bt-transport/000`). Each of these devices only represents the transport and not an initializedBluetooth controller since most Bluetooth controllers require vendor-specific protocolsfor their setup (e.g. to load firmware). That logic is implemented by vendor HCIdrivers that bind to a bt-transport device. 传输驱动程序发布bt传输设备（例如`/ dev / class / bt-transport / 000`）。这些设备中的每一个仅代表传输，而不代表初始化的蓝牙控制器，因为大多数蓝牙控制器都需要特定于供应商的协议来进行设置（例如，加载固件）。该逻辑由绑定到bt传输设备的供应商HCI驱动程序实现。

Vendor drivers have access to the bt-transport protocol for HCI transactions, as well as other underlying protocols that the transport device supports. Once aBluetooth controller has been initialized and is ready for the host subsystem,the vendor driver publishes a `bt-hci` device. 供应商驱动程序可以访问HCI事务的bt-transport协议，以及传输设备支持的其他基础协议。一旦蓝牙控制器已经初始化并准备好用于主机子系统，供应商驱动程序就会发布一个“ bt-hci”设备。

The system provides the `bthci-passthrough` driver which binds to bt-transport devices that are not claimed by any vendor-specific driver. bthci-passthroughsimply publishes a bt-hci device without doing special initialization. 系统提供了“ bthci-passthrough”驱动程序，该驱动程序绑定到任何特定于供应商的驱动程序都未要求的bt传输设备。 bthci-passthroughs仅发布bt-hci设备，而无需进行特殊的初始化。

 
### Host  主办 

The `bthost` driver implements the core Bluetooth protocols that form the Generic Access Profile. bthost binds to bt-hci devices and publishes `bt-host`devices. A bt-host device claims the HCI control and data endpoints of the underlying`bt-hci` and implements: bthost驱动程序实现构成通用访问配置文件的核心蓝牙协议。 bthost绑定到bt-hci设备并发布“ bt-host”设备。 bt主机设备声明底层bt-hci的HCI控制和数据端点，并实现：

 
* The core dual-mode GAP bookkeeping  *核心双模式GAP簿记
* Handling of FIDL messages for core services  *为核心服务处理FIDL消息
* L2CAP and fixed channel protocols (GATT, SMP, SDP)  * L2CAP和固定通道协议（GATT，SMP，SDP）
* Pairing protocols and delegation  *配对协议和委托
* Other types of IPC (such as L2CAP sockets)  *其他类型的IPC（例如L2CAP插座）
* Bus protocol for child devices for services implemented as device drivers  *子设备的总线协议，用于实现为设备驱动程序的服务

Host devices are managed by the [Bluetooth system service](/src/connectivity/bluetooth/).The service allows only one bt-host to be accessed for service requests at a giventime. This bt-host is represented as the "active Adapter".[control.fidl](/sdk/fidl/fuchsia.bluetooth.control) provides a managementinterface to designate an active adapter when multiple adapters are present. 主机设备由[蓝牙系统服务]（/ src / connectivity / bluetooth /）管理。该服务只允许在给定时间访问一个bt主机以进行服务请求。此bt主机表示为“活动适配器”。[control.fidl]（/ sdk / fidl / fuchsia.bluetooth.control）提供了一个管理接口，用于在存在多个适配器时指定活动适配器。

bt-host devices implement the [host.fidl](/src/connectivity/bluetooth/fidl/host.fidl) protocol to communicate with the Bluetooth system service. bt-host设备实现[host.fidl]（/ src / connectivity / bluetooth / fidl / host.fidl）协议与蓝牙系统服务进行通信。

 

 
### Host Bus  主机总线 

TODO(armansito): child devices  TODO（armansito）：子设备

 
## Services  服务 

Bluetooth environment services are the primary way to implement Bluetooth services and applications. 蓝牙环境服务是实现蓝牙服务和应用程序的主要方式。

The [Control](/sdk/fidl/fuchsia.bluetooth.control) FIDL library is intended for privileged clients and is for device-level control/policy. [Control]（/ sdk / fidl / fuchsia.bluetooth.control）FIDL库旨在用于特权客户端，并且用于设备级控制/策略。

