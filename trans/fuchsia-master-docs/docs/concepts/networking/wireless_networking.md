 
# Fuchsia Wireless Networking  紫红色无线网络 

 
## Introduction  介绍 

Fuchsia's wireless networking stack intends to provide a compliant non-AP station implementation of IEEE Std 802.11. It supports hardware with both "full MAC" and"soft MAC" firmware, in which the MLME layer of the 802.11 spec is implementedin the firmware and the host OS, respectively. 紫红色的无线网络堆栈旨在提供IEEE Std 802.11的兼容非AP站实现。它支持具有“完整MAC”和“软MAC”固件的硬件，其中802.11规范的MLME层分别在固件和主机OS中实现。

 
## High-level architecture  高层架构 

```
                          +------------------+        +------------------+
 Fuchsia service          | Fuchsia netstack |        | Fuchsia Wireless |
                          |                  |        | Network Service  |
                          +------------------+        +------------------+
                              ^                        ^                ^
                              |                        |                |
 fdio/FIDL              ------|------------------------|----------------|-------------------
                              |                        |                |
                              v                        |                v
                          +------------------+         |               +--------------+
                          | Fuchsia ethernet |<--------|-------------->| Fuchsia WLAN |
                          | driver           |         |               | MLME driver  |
 devmgr                   +------------------+         |               +--------------+
                                         ^             |                    ^
                                         |             |                    |
                                         v             v                    v
                                    +-------------------+              +-------------------+
                                    | Driver            |              | Driver            |
                                    | (Full MAC device) |              | (Soft MAC device) |
                                    +-------------------+              +-------------------+
                                                      ^                    ^
                                                       \                  /
 hardware bus                       --------------------\----------------/------------------
 (USB, PCI, etc)                                         \              /
                                                          v            v
                                                     +---------------------+
                                                     | Wireless networking |
 hardware                                            | hardware            |
                                                     +---------------------+
```
 

 

 
## Drivers  车手 

A Full MAC driver relies on the firmware in the wireless hardware to implement the majority of the IEEE 802.11 MLME functions. Full MAC驱动程序依靠无线硬件中的固件来实现大多数IEEE 802.11 MLME功能。

A Soft MAC driver implements the basic building blocks of communication with the wireless hardware in order to allow the Fuchsia MLME driver to execute the IEEE802.11 MLME functions. 软MAC驱动程序实现与无线硬件通信的基本构造块，以允许紫红色MLME驱动程序执行IEEE802.11 MLME功能。

The Fuchsia MLME driver is a hardware-independent layer that provides state machines for synchronization, authentication, association, and other wirelessnetworking state. It communicates with a Soft MAC driver to manage the hardware. 紫红色MLME驱动程序是独立于硬件的层，为同步，身份验证，关联和其他无线网络状态提供状态机。它与Soft MAC驱动程序通信以管理硬件。

 
## WLAN service  WLAN服务 

The Fuchsia Wireless Network Service implements the IEEE 802.11 SME functions and holds state about all the wireless networks that are available in thecurrent environment. It is the interface to the hardware (via the drivers) usedby components like System UI. 紫红色无线网络服务实现了IEEE 802.11 SME功能，并保持了当前环境中所有可用无线网络的状态。它是系统UI等组件所使用的硬件接口（通过驱动程序）。

 
## Relation to the Ethernet stack  与以太网堆栈的关系 

Either a Full MAC driver or the Fuchsia WLAN MLME driver will expose an Ethernet device in devmgr. This device will behave as any other Ethernet device, and willprovide data packets to the rest of the system. TBD: whether to use Ethernet IIframes always, or support 802.2 SNAP frames. Full MAC驱动程序或Fuchsia WLAN MLME驱动程序都会在devmgr中公开以太网设备。该设备将像其他任何以太网设备一样工作，并将数据包提供给系统的其余部分。 TBD：是始终使用以太网II帧，还是支持802.2 SNAP帧。

 
## Interfaces  介面 

The Fuchsia Wireless Network Service will communicate with each hardware device using a channel to the driver, obtained via ioctl. (Eventually this will bereplaced by FIDL.) Messages exchanged over this channel will encode therequest/response for each action, generally following the IEEE 802.11 MLME SAPdefinitions. 紫红色无线网络服务将使用通过ioctl获得的驱动程序通道与每个硬件设备进行通信。 （最终将由FIDL替换。）通常在IEEE 802.11 MLME SAP定义之后，通过此通道交换的消息将对每个操作的请求/响应进行编码。

