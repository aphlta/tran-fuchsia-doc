 
# Zircon Device Model  锆石设备型号 

 
## Introduction  介绍 

In Zircon, device drivers are implemented as ELF shared libraries (DSOs) which are loaded into Device Host (devhost) processes.  The Device Manager (devmgr) process,contains the Device Coordinator which keeps track of drivers and devices, managesthe discovery of drivers, the creation and direction of Device Host processes, andmaintains the Device Filesystem (devfs), which is the mechanism through which userspaceservices and applications (constrained by their namespaces) gain access to devices. 在Zircon中，设备驱动程序实现为ELF共享库（DSO），该库已加载到设备主机（devhost）进程中。设备管理器（devmgr）进程包含设备协调器，该协调器跟踪驱动程序和设备，管理驱动程序的发现，设备主机进程的创建和方向，以及维护设备文件系统（devfs），通过该机制，用户空间服务和应用程序（受其名称空间限制）可以访问设备。

The Device Coordinator views devices as part of a single unified tree. The branches (and sub-branches) of that tree consist of some number ofdevices within a Device Host process.  The decision as to how to sub-dividethe overall tree among Device Hosts is based on system policy for isolatingdrivers for security or stability reasons and colocating drivers for performancereasons. 设备协调器将设备视为单个统一树的一部分。该树的分支（和子分支）由设备主机进程中的一些设备组成。关于如何在设备主机之间细分整体树的决定基于系统策略，出于安全性或稳定性的考虑，隔离驱动程序，并出于性能原因共置驱动程序。

Note: The current policy is simple (each device representing a physical bus-master capable hardware device and its children are placed into a separate devhost).  Itwill evolve to provide finer-grained partitioning. 注意：当前策略很简单（每个代表物理总线主设备的硬件设备及其子设备都放置在单独的devhost中）。它将演变为提供更细粒度的分区。

 

 
## Devices, Drivers, and Device Hosts  设备，驱动程序和设备主机 

Here's a (slightly trimmed for clarity) dump of the tree of devices in Zircon running on Qemu x86-64: 这是在Qemu x86-64上运行的Zircon中的设备树的转储（为清晰起见，略有修饰）：

```sh
$ dm dump
[root]
   <root> pid=1509
      [null] pid=1509 /boot/driver/builtin.so
      [zero] pid=1509 /boot/driver/builtin.so
   [misc]
      <misc> pid=1645
         [console] pid=1645 /boot/driver/console.so
         [dmctl] pid=1645 /boot/driver/dmctl.so
         [ptmx] pid=1645 /boot/driver/pty.so
         [i8042-keyboard] pid=1645 /boot/driver/pc-ps2.so
            [hid-device-001] pid=1645 /boot/driver/hid.so
         [i8042-mouse] pid=1645 /boot/driver/pc-ps2.so
            [hid-device-002] pid=1645 /boot/driver/hid.so
   [sys]
      <sys> pid=1416 /boot/driver/bus-acpi.so
         [acpi] pid=1416 /boot/driver/bus-acpi.so
         [pci] pid=1416 /boot/driver/bus-acpi.so
            [00:00:00] pid=1416 /boot/driver/bus-pci.so
            [00:01:00] pid=1416 /boot/driver/bus-pci.so
               <00:01:00> pid=2015 /boot/driver/bus-pci.proxy.so
                  [bochs_vbe] pid=2015 /boot/driver/bochs-vbe.so
                     [framebuffer] pid=2015 /boot/driver/framebuffer.so
            [00:02:00] pid=1416 /boot/driver/bus-pci.so
               <00:02:00> pid=2052 /boot/driver/bus-pci.proxy.so
                  [intel-ethernet] pid=2052 /boot/driver/intel-ethernet.so
                     [ethernet] pid=2052 /boot/driver/ethernet.so
            [00:1f:00] pid=1416 /boot/driver/bus-pci.so
            [00:1f:02] pid=1416 /boot/driver/bus-pci.so
               <00:1f:02> pid=2156 /boot/driver/bus-pci.proxy.so
                  [ahci] pid=2156 /boot/driver/ahci.so
            [00:1f:03] pid=1416 /boot/driver/bus-pci.so
```
 

The names in square brackets are devices.  The names in angle brackets are proxy devices, which are instantiated in the "lower" devhost, when processisolation is being provided.  The pid= field indicates the process objectid of the devhost process that device is contained within.  The path indicateswhich driver implements that device. 方括号中的名称是设备。尖括号中的名称是代理设备，当提供进程隔离时，将在“下部” devhost中实例化它们。 pid =字段指示设备所在的devhost进程的进程objectid。该路径指示哪个驱动程序实现该设备。

Above, for example, the pid 1416 devhost contains the pci bus driver, which has created devices for each PCI device in the system.  PCI device 00:02:00 happensto be an intel ethernet interface, which we have a driver for (intel-ethernet.so).A new devhost (pid 2052) is created, set up with a proxy device for PCI 00:02:00,and the intel ethernet driver is loaded and bound to it. 例如，在上面的pid 1416 devhost包含pci总线驱动程序，该驱动程序已为系统中的每个PCI设备创建了设备。 PCI设备00:02:00恰好是一个英特尔以太网接口，我们有一个驱动程序（intel-ethernet.so）。创建了一个新的devhost（pid 2052），并为PCI 00:02设置了代理设备： 00，并加载并绑定了英特尔以太网驱动程序。

Proxy devices are invisible within the Device filesystem, so this ethernet device appears as `/dev/sys/pci/00:02:00/intel-ethernet`. 代理设备在设备文件系统中不可见，因此该以太网设备显示为`/ dev / sys / pci / 00：02：00 / intel-ethernet`。

 

 
## Protocols, Interfaces, and Classes  协议，接口和类 

Devices may implement Protocols, which are Banjo ABIs used by child devices to interact with parent devices in a device-specific manner. The[PCI Protocol](/zircon/system/banjo/ddk.protocol.pci/pci.banjo),[USB Protocol](/zircon/system/banjo/ddk.protocol.usb/usb.banjo),[Block Core Protocol](/zircon/system/banjo/ddk.protocol.block/block.banjo), and[Ethernet Protocol](/zircon/system/banjo/ddk.protocol.ethernet/ethernet.banjo), areexamples of these.  Protocols are usually in-process interactions betweendevices in the same devhost, but in cases of driver isolation, they may takeplace via RPC to a "higher" devhost (via proxy). 设备可以实现协议，这些协议是子级设备用于以特定于设备的方式与父级设备交互的Banjo ABI。 [PCI协议]（/ zircon / system / banjo / ddk.protocol.pci / pci.banjo），[USB协议]（/ zircon / system / banjo / ddk.protocol.usb / usb.banjo），[Block Core协议]（/ zircon / system / banjo / ddk.protocol.block / block.banjo）和[以太网协议]（/ zircon / system / banjo / ddk.protocol.ethernet / ethernet.banjo）是这些示例。协议通常是同一devhost中设备之间的进程内交互，但是在驱动程序隔离的情况下，它们可能会通过RPC到达“更高”的devhost（通过代理）。

Devices may implement Interfaces, which are [FIDL](/docs/development/languages/fidl/README.md) RPC protocolsthat clients (services, applications, etc) use.  The base device interfacesupports POSIX style open/close/read/write IO.  Interfaces are supported viathe `message()` operation in the base device interface. 设备可以实现接口，即客户端（服务，应用程序等）使用的[FIDL]（/ docs / development / languages / fidl / README.md）RPC协议。基本设备接口支持POSIX样式的打开/关闭/读/写IO。通过基本设备接口中的“ message（）”操作支持接口。

In many cases a Protocol is used to allow drivers to be simpler by taking advantage of a common implementation of an Interface.  For example, the "block" driver implementsthe common block interface, and binds to devices implementing the Block Core Protocol,and the "ethernet" driver does the same thing for the Ethernet Interface and EthermacProtocol.  Some protocols, such as the two cited here, make use of shared memory, andnon-rpc signaling for more efficient, lower latency, and higher throughput than couldbe achieved otherwise. 在许多情况下，协议可用于通过利用接口的通用实现来简化驱动程序。例如，“块”驱动程序实现公共块接口，并绑定到实现块核心协议的设备，而“以太网”驱动程序对以太网接口和EthermacProtocol执行相同的操作。某些协议（如此处引用的两种协议）利用共享内存和非rpc信令，以实现比其他方式更有效，更低的延迟和更高的吞吐量。

Classes represent a promise that a device implements an Interface or Protocol. Devices exist in the Device Filesystem under a topological path, like`/sys/pci/00:02:00/intel-ethernet`.  If they are a specific class, they also appearas an alias under `/dev/class/CLASSNAME/...`.  The `intel-ethernet` driver implementsthe Ethermac interface, so it also shows up at `/dev/class/ethermac/000`.  The nameswithin class directories are unique but not meaningful, and are assigned on demand. 类表示设备实现接口或协议的承诺。设备存在于设备文件系统中的拓扑路径下，例如/ sys / pci / 00：02：00 / intel-ethernet。如果它们是特定的类，它们也将作为别名出现在`/ dev / class / CLASSNAME / ...`下。 “ intel-ethernet”驱动程序实现了Ethermac接口，因此它也显示在“ / dev / class / ethermac / 000”上。类目录中的名称是唯一的，但没有意义，并且是按需分配的。

Note: Currently names in class directories are 3 digit decimal numbers, but they are likely to change form in the future.  Clients should not assume there is anyspecific meaning to a class alias name. 注意：当前，类目录中的名称是3位十进制数字，但是将来它们可能会更改形式。客户不应假定类别名名称有任何特定含义。

 

 
## Device Driver Lifecycle  设备驱动程序生命周期 

Device drivers are loaded into devhost processes when it is determined they are needed.  What determines if they are loaded or not is the Binding Program, whichis a description of what device a driver can bind to.  The Binding Program isdefined using macros in [`ddk/binding.h`](/zircon/system/ulib/ddk/include/ddk/binding.h) 确定需要将设备驱动程序加载到devhost进程中。决定是否加载它们的是绑定程序，它描述了驱动程序可以绑定到的设备。使用[`ddk / binding.h`]（/ zircon / system / ulib / ddk / include / ddk / binding.h）中的宏定义绑定程序。

An example Binding Program from the Intel Ethernet driver:  来自英特尔以太网驱动程序的绑定程序示例：

```c
ZIRCON_DRIVER_BEGIN(intel_ethernet, intel_ethernet_driver_ops, "zircon", "0.1", 9)
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_PCI),
    BI_ABORT_IF(NE, BIND_PCI_VID, 0x8086),
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x100E), // Qemu
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15A3), // Broadwell
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x1570), // Skylake
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x1533), // I210 standalone
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15b7), // Skull Canyon NUC
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15b8), // I219
    BI_MATCH_IF(EQ, BIND_PCI_DID, 0x15d8), // Kaby Lake NUC
ZIRCON_DRIVER_END(intel_ethernet)
```
 

The ZIRCON_DRIVER_BEGIN and _END macros include the necessary compiler directives to put the binding program into an ELF NOTE section, allowing it to be inspectedby the Device Coordinator without needing to fully load the driver into its process.The second parameter to the _BEGIN macro is a `zx_driver_ops_t` structure pointer (definedby `[ddk/driver.h](/zircon/system/ulib/ddk/include/ddk/driver.h)` which defines theinit, bind, create, and release methods. ZIRCON_DRIVER_BEGIN和_END宏包含必要的编译器指令，可将绑定程序放入ELF NOTE部分，从而允许设备协调器对其进行检查而无需将驱动程序完全加载到其进程中._BEGIN宏的第二个参数是` zx_driver_ops_t`结构指针（由[ddk / driver.h]（/ zircon / system / ulib / ddk / include / ddk / driver.h）定义，用于定义init，bind，create和release方法。

`init()` is invoked when a driver is loaded into a Device Host process and allows for any global initialization.  Typically none is required.  If the `init()` method isimplemented and fails, the driver load will fail. 将驱动程序加载到设备主机进程中时，将调用“ init（）”，并允许进行任何全局初始化。通常不需要。如果`init（）`方法实现并失败，则驱动程序加载将失败。

`bind()` is invoked to offer the driver a device to bind to.  The device is one that has matched the bind program the driver has published.  If the `bind()` method succeeds,the driver **must** create a new device and add it as a child of the device passed into the `bind()` method.  See Device Lifecycle for more information. 调用bind（）为驱动程序提供要绑定的设备。该设备是与驱动程序已发布的绑定程序匹配的设备。如果bind（）方法成功，则驱动程序必须创建一个新设备，并将其添加为传递给bind（）方法的设备的子设备。有关更多信息，请参见设备生命周期。

`create()` is invoked for platform/system bus drivers or proxy drivers.  For the vast majority of drivers, this method is not required. 为平台/系统总线驱动程序或代理驱动程序调用`create（）`。对于绝大多数驱动程序，不需要此方法。

`release()` is invoked before the driver is unloaded, after all devices it may have created in `bind()` and elsewhere have been destroyed.  Currently this method is**never** invoked.  Drivers, once loaded, remain loaded for the life of a Device Hostprocess. 在释放驱动程序之前，可能已经在“ bind（）”中创建的所有设备以及其他地方的设备都被销毁之后，会调用“ release（）”。目前，从未调用此方法。一旦加载驱动程序，驱动程序将在设备主机进程的整个生命周期内保持加载状态。

 

 
## Device Lifecycle  设备生命周期 

Within a Device Host process, devices exist as a tree of `zx_device_t` structures which are opaque to the driver.  These are created with `device_add()` which thedriver provides a `zx_protocol_device_t` structure to.  The methods defined by thefunction pointers in this structure are the "[device ops](device-ops.md)".  Thevarious structures and functions are defined in [`device.h`](/zircon/system/ulib/ddk/include/ddk/device.h) 在设备主机进程中，设备以“ zx_device_t”结构树的形式存在，对驱动程序而言是不透明的。这些是通过device_add（）创建的，驱动程序向其中提供了zx_protocol_device_t结构。在此结构中，功能指针定义的方法是“ [device ops]（device-ops.md）”。各种结构和功能在[`device.h`]（/ zircon / system / ulib / ddk / include / ddk / device.h）中定义

The `device_add()` function creates a new device, adding it as a child to the provided parent device.  That parent device **must** be either the device passedin to the `bind()` method of a device driver, or another device which has beencreated by the same device driver. device_add（）函数创建一个新设备，并将其作为子设备添加到提供的父设备中。父设备必须是传递给设备驱动程序的bind（）方法的设备，或者是由同一设备驱动程序创建的另一个设备。

A side-effect of `device_add()` is that the newly created device will be added to the global Device Filesystem maintained by the Device Coordinator.  If thedevice is created with the **DEVICE_ADD_INVISIBLE** flag, it will not be accessiblevia opening its node in devfs until `device_make_visible()` is invoked.  Thisis useful for drivers that have to do extended initialization or probing anddo not want to visibly publish their device(s) until that succeeds (and quietlyremove them if that fails). device_add（）的副作用是新创建的设备将被添加到由设备协调器维护的全局设备文件系统中。如果设备是使用** DEVICE_ADD_INVISIBLE **标志创建的，则在调用`device_make_visible（）`之前，无法通过在devfs中打开其节点来访问该设备。这对于必须执行扩展的初始化或探测并且在成功之前不希望可视地发布其设备的驱动程序很有用（如果失败，则静默删除它们）。

Devices are reference counted. A reference is acquired when a driver creates the device with `device_add()` and when the device is opened by a remote processvia the Device Filesystem. 设备按引用计数。当驱动程序使用device_add（）创建设备时，以及通过远程进程通过设备文件系统打开设备时，都会获取引用。

From the moment that `device_add()` is called without the **DEVICE_ADD_INVISIBLE** flag, or `device_make_visible()` is called on an invisible device, other deviceops may be called by the Device Host. 从不带DEVICE_ADD_INVISIBLE标志的情况下调用device_add（）或在不可见的设备上调用device_make_visible（）的那一刻起，设备主机便可以调用其他deviceop。

When `device_async_remove()` is called on a device, this schedules the removal of the device and its descendents. 当在设备上调用“ device_async_remove（）”时，这将安排设备及其后代的移除。

The removal of a device consists of four parts: running the device's `unbind()` hook, removal of the device from the Device Filesystem, dropping the reference acquiredby `device_add()` and running the device's `release()` hook. 删除设备包括四个部分：运行设备的“ unbind（）”钩子，从设备文件系统中删除设备，删除“ device_add（）”获取的引用以及运行设备的“ release（）”钩子。

When the `unbind()` method is invoked, this signals to the driver it should start shutting the device down, and call `device_unbind_reply()` once it has finished unbinding.This is an optional hook. If it is not implemented, it is treated as `device_unbind_reply()`was called immediately. 调用unbind（）方法时，这会向驱动程序发出信号，表明它应该开始关闭设备，并在完成解除绑定后调用device_unbind_reply（）。这是一个可选的钩子。如果未实现，则将其视为`device_unbind_reply（）`被立即调用。

Since a child device may have work in progress when its `unbind()` method is called, it's possible that the parent device (which already completedunbinding) could continue to receive device method calls or protocol methodcalls on behalf of that child.  It is advisable that before completing unbinding,the parent device should arrange for these methods to return errors, so thatcalls from a child before the child removal is completed do not start morework or cause unexpected interactions. 由于子设备在调用其unbind（）方法时可能正在进行工作，因此父设备（已完成解绑定）可能会继续代表该子设备接收设备方法调用或协议方法调用。建议在完成解除绑定之前，父设备应安排这些方法返回错误，以便在删除子进程之前从子进程进行的调用不会启动更多的工作或引起意外的交互。

The `release()` method is only called after the creating driver has completed unbinding, all open instances of that device have been closed,and all children of that device have been unbound and released.  Thisis the last opportunity for the driver to destroy or free any resources associatedwith the device.  It is not valid to refer to the `zx_device_t` for that deviceafter `release()` returns.  Calling any device methods or protocol methods forprotocols obtained from the parent device past this point is illegal and willlikely result in a crash. 仅在创建驱动程序完成解除绑定，关闭该设备的所有打开实例并且已解除绑定和释放该设备的所有子级之后，才调用release方法。这是驱动程序销毁或释放与设备关联的任何资源的最后机会。在`release（）`返回后，对该设备引用`zx_device_t`是无效的。超过此时间点调用从父设备获得的协议的任何设备方法或协议方法都是非法的，可能会导致崩溃。

 
### An Example of the Tear-Down Sequence  取下序列的示例 

To explain how the `unbind()` and `release()` work during the tear-down process, below is an example of how a USB WLAN driver would usually handle it.  In short,the `unbind()` call sequence is top-down while the `release()` sequence is bottom-up. 为了说明在拆解过程中unbind（）和release（）的工作方式，以下是USB WLAN驱动程序通常如何处理它的示例。简而言之，unbind（）调用序列是自上而下的，而release（）序列是自下而上的。

Note that this is just an example. This might not match what exactly the real WLAN driver is doing. 请注意，这仅是示例。这可能与真正的WLAN驱动程序所做的完全不匹配。

Assume a WLAN device is plugged in as a USB device, and a PHY interface has been created under the USB device. In addition to the PHY interface, 2 MAC interfaceshave been created under the PHY interface. 假设将WLAN设备作为USB设备插入，并且在USB设备下创建了PHY接口。除PHY接口外，还在PHY接口下创建了2个MAC接口。

```
            +------------+
            | USB Device | .unbind()
            +------------+ .release()
                  |
            +------------+
            |  WLAN PHY  | .unbind()
            +------------+ .release()
              |        |
    +------------+  +------------+
    | WLAN MAC 0 |  | WLAN MAC 1 | .unbind()
    +------------+  +------------+ .release()
```
 

Now, we unplug this USB WLAN device.  现在，我们拔下此USB WLAN设备。

 
* The USB XHCI detects the removal and calls `device_async_remove(usb_device)`.  * USB XHCI检测到删除并调用`device_async_remove（usb_device）`。

 
* This will lead to the USB device's `unbind()` being called. Once it completes unbinding, it would call `device_unbind_reply()`. *这将导致USB设备的`unbind（）`被调用。一旦解除绑定，它将调用device_unbind_reply（）。

```c
    usb_device_unbind(void* ctx) {
        // Stop interrupt or anything to prevent incoming requests.
        ...

        device_unbind_reply(usb_dev);
    }
```
 

 
* When the USB device completes unbinding, the WLAN PHY's `unbind()` is called. Once it completes unbinding, it would call `device_unbind_reply()`. *当USB设备完成解除绑定时，将调用WLAN PHY的`unbind（）`。一旦解除绑定，它将调用device_unbind_reply（）。

```c
    wlan_phy_unbind(void* ctx) {
        // Stop interrupt or anything to prevent incoming requests.
        ...

        device_unbind_reply(wlan_phy);
    }
```
 

 
* When wlan_phy completes unbinding, unbind() will be called on all of its children (wlan_mac_0, wlan_mac_1). *当wlan_phy完成解除绑定时，将在其所有子项（wlan_mac_0，wlan_mac_1）上调用unbind（）。

```c
    wlan_mac_unbind(void* ctx) {
        // Stop accepting new requests, and notify clients that this device is offline (often just
        // by returning an ZX_ERR_IO_NOT_PRESENT to any requests that happen after unbind).
        ...

        device_unbind_reply(iface_mac_X);
    }
```
 

 
* Once all the clients of a device have been removed, and that device has no children, its refcount will reach zero and its release() method will be called. *一旦删除了设备的所有客户端，并且该设备没有子代，其refcount将达到零，并调用release（）方法。

 
* WLAN MAC 0 and 1's `release()` are called.  *称为WLAN MAC 0和1的`release（）`。

```c
    wlan_mac_release(void* ctx) {
        // Release sources allocated at creation.
        ...

        // Delete the object here.
        ...
    }
```
 

 
* The wlan_phy has no open connections, but still has child devices (wlan_mac_0 and wlan_mac_1). Once they have both been released, its refcount finally reaches zero and its release()method is invoked. * wlan_phy没有打开的连接，但仍然具有子设备（wlan_mac_0和wlan_mac_1）。一旦它们都被释放，其引用计数最终将达到零，并调用其release（）方法。

```c
    wlan_phy_release(void* ctx) {
        // Release sources allocated at creation.
        ...

        // Delete the object here.
        ...
    }
```
 

 
