 
# Zircon Driver Development  锆石驱动程序开发 

Zircon drivers are shared libraries that are dynamically loaded in Device Host processes in user space. The process of loading a driver is controlled by theDevice Coordinator. See [Device Model](device-model.md) for more information onDevice Hosts, Device Coordinator and the driver and device lifecycles. Zircon驱动程序是共享库，它们在用户空间的设备主机进程中动态加载。加载驱动程序的过程由设备协调器控制。有关设备主机，设备协调器以及驱动程序和设备生命周期的更多信息，请参见[设备模型]（device-model.md）。

 
## Directory structure  目录结构 

Zircon drivers are found under [system/dev](/zircon/system/dev). They are grouped based on the protocols they implement.The driver protocols are defined in[ddk/include/ddk/protodefs.h](/zircon/system/ulib/ddk/include/ddk/protodefs.h).For example, a USB ethernet driver goes in [system/dev/ethernet](/zircon/system/dev/ethernet)rather than [system/dev/usb](/zircon/system/dev/usb) because it implements an ethernet protocol.However, drivers that implement the USB stack are in [system/dev/usb](/zircon/system/dev/usb)because they implement USB protocols. Zircon驱动程序位于[system / dev]（/ zircon / system / dev）下。它们根据实现的协议进行分组。驱动程序协议在[ddk / include / ddk / protodefs.h]（/ zircon / system / ulib / ddk / include / ddk / protodefs.h）中定义。 USB以太网驱动程序进入[system / dev / ethernet]（/ zircon / system / dev / ethernet），而不是[system / dev / usb]（/ zircon / system / dev / usb），因为它实现了以太网协议。但是，实现USB堆栈的驱动程序位于[system / dev / usb]（/ zircon / system / dev / usb）中，因为它们实现了USB协议。

In the driver's `rules.mk`, the `MODULE_TYPE` should be `driver`. This will install the driver shared lib in `/boot/driver/`. 在驱动程序的“ rules.mk”中，“ MODULE_TYPE”应为“ driver”。这将在/ boot / driver /中安装驱动程序共享库。

If your driver is built outside Zircon, install them in `/system/driver/` . The Device Coordinator looks in those directories for loadabledrivers. 如果您的驱动程序是在Zircon之外构建的，则将它们安装在`/ system / driver /`中。设备协调器在这些目录中查找可加载的驱动程序。

 
## Declaring a driver  声明驱动程序 

At a minimum, a driver should contain the driver declaration and implement the `bind()` driver op. 驱动程序至少应包含驱动程序声明并实现`bind（）`驱动程序op。

Drivers are loaded and bound to a device when the Device Coordinator successfully finds a matching driver for a device. A driver declares thedevices it is compatible with via bindings.The following bind programdeclares the [AHCI driver](/zircon/system/dev/block/ahci/ahci.h): 当设备协调器成功找到设备的匹配驱动程序时，驱动程序将被加载并绑定到设备。驱动程序通过绑定声明与之兼容的设备。以下绑定程序声明[AHCI驱动程序]（/ zircon / system / dev / block / ahci / ahci.h）：

```c
ZIRCON_DRIVER_BEGIN(ahci, ahci_driver_ops, "zircon", "0.1", 4)
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_PCI),
    BI_ABORT_IF(NE, BIND_PCI_CLASS, 0x01),
    BI_ABORT_IF(NE, BIND_PCI_SUBCLASS, 0x06),
    BI_MATCH_IF(EQ, BIND_PCI_INTERFACE, 0x01),
ZIRCON_DRIVER_END(ahci)
```
 

The AHCI driver has 4 directives in the bind program. `"zircon"` is the vendor id and `"0.1"` is the driver version. It binds with `ZX_PROTOCOL_PCI` deviceswith PCI class 1, subclass 6, interface 1. AHCI驱动程序在绑定程序中具有4个指令。 “ zircon”是供应商ID，“ 0.1”是驱动程序版本。它与具有PCI 1类，6类，接口1的ZX_PROTOCOL_PCI设备绑定。

The [PCI driver](/zircon/system/dev/bus/pci/kpci/kpci.c) publishes the matching device with the following properties: [PCI驱动程序]（/ zircon / system / dev / bus / pci / kpci / kpci.c）发布具有以下属性的匹配设备：

```c
zx_device_prop_t device_props[] = {
    {BIND_PROTOCOL, 0, ZX_PROTOCOL_PCI},
    {BIND_PCI_VID, 0, info.vendor_id},
    {BIND_PCI_DID, 0, info.device_id},
    {BIND_PCI_CLASS, 0, info.base_class},
    {BIND_PCI_SUBCLASS, 0, info.sub_class},
    {BIND_PCI_INTERFACE, 0, info.program_interface},
    {BIND_PCI_REVISION, 0, info.revision_id},
    {BIND_PCI_BDF_ADDR, 0, BIND_PCI_BDF_PACK(info.bus_id, info.dev_id,
                                             info.func_id)},
};
```
 

Binding variables and macros are defined in [zircon/driver/binding.h](/zircon/system/public/zircon/driver/binding.h).If you are introducing a new device class, you may need to introduce newbinding variables in that file.Binding variables are 32-bit values. If yourvariable value requires greater than a 32-bit value,split them into multiple 32-bit variables. Anexample is ACPI HID values, which are 8 characters (64-bits) long.It is split into `BIND_ACPI_HID_0_3` and `BIND_ACPI_HID_4_7`. 绑定变量和宏在[zircon / driver / binding.h]（/ zircon / system / public / zircon / driver / binding.h）中定义。如果要引入新的设备类，则可能需要在其中引入newbinding变量。该文件。绑定变量是32位值。如果您的变量值需要大于32位的值，请将其拆分为多个32位变量。一个示例是ACPI HID值，长度为8个字符（64位），分为``BIND_ACPI_HID_0_3''和``BIND_ACPI_HID_4_7''。

Binding directives are evaluated sequentially. The branching directives `BI_GOTO()` and `BI_GOTO_IF()` allow you to jump forward to the matchinglabel, defined by `BI_LABEL()`. 绑定指令按顺序求值。分支指令BI_GOTO（）和BI_GOTO_IF（）允许您跳转到BI_LABEL（）定义的匹配标签。

`BI_ABORT_IF_AUTOBIND` may be used (usually as the first instruction) to prevent the default automatic binding behaviour.In that case, a driver can be bound to a device using`fuchsia.device.Controller/Bind` FIDL call 可以使用BI_ABORT_IF_AUTOBIND（通常作为第一条指令）来防止默认的自动绑定行为，在这种情况下，可以使用fuchsia.device.Controller / Bind FIDL调用将驱动程序绑定到设备。

 

 
## Driver binding  驱动程序绑定 

A driver's `bind()` function is called when it is matched to a device. Generally a driver will initialize any data structures needed for the deviceand initialize hardware in this function. It should not perform anytime-consuming tasks or block in this function, because it is invoked from thedevhost's RPC thread and it will not be able to service other requests in themeantime. Instead, it should spawn a new thread to perform lengthy tasks. 当驱动程序的“ bind（）”函数与设备匹配时，将调用该函数。通常，驱动程序将初始化设备所需的任何数据结构，并在此功能中初始化硬件。它不应执行任何耗时的任务或在此功能中阻塞，因为它是从devhost的RPC线程调用的，并且在主题时间中将无法为其他请求提供服务。相反，它应该产生一个新线程来执行冗长的任务。

The driver should make no assumptions about the state of the hardware in `bind()`, resetting the hardware or otherwise ensuring it is in a known state.Because the system recovers from adriver crash by re-spawning the devhost, the hardware may be in an unknownstate when `bind()` is invoked. 驱动程序不应对bind（）中的硬件状态进行任何假设，重置硬件或以其他方式确保其处于已知状态。由于系统可以通过重新生成devhost从驱动程序崩溃中恢复，因此硬件可能是当调用bind（）时处于未知状态。

A driver is required to publish a `zx_device_t` in `bind()` by calling `device_add()`. This is necessary for the Device Coordinator to keeptrack of thedevice lifecycle. If the driver is not able to publish a functional device in`bind()`, for example if it is initializing the full device in a thread, itshould publish an invisible device, and make this device visible wheninitialization is completed. See `DEVICE_ADD_INVISIBLE` and`device_make_visible()` in[zircon/ddk/driver.h](/zircon/system/ulib/ddk/include/ddk/driver.h). 需要驱动程序通过调用device_add（）在bind（）中发布zz_device_t。这对于设备协调器跟踪设备生命周期是必要的。如果驱动程序无法在`bind（）`中发布功能设备，例如，如果它正在线程中初始化整个设备，则它应发布不可见的设备，并在初始化完成后使该设备可见。请参阅[zircon / ddk / driver.h]（/ zircon / system / ulib / ddk / include / ddk / driver.h）中的`DEVICE_ADD_INVISIBLE`和`device_make_visible（）`。

There are generally four outcomes from `bind()`:  通常，bind（）有四个结果：

 
1. The driver determines the device is supported and does not need to do any heavy lifting, so publishes a new device via `device_add()` and returns`ZX_OK`. 1.驱动程序确定设备受支持并且不需要做任何繁重的工作，因此通过`device_add（）`发布新设备并返回`ZX_OK`。

 
2. The driver determines that even though the bind program matched, the device cannot be supported (maybe due to checking hw version bits or whatnot) andreturns an error. 2.驱动程序确定即使绑定程序匹配，也无法支持该设备（可能是由于检查硬件版本位或其他原因），并返回错误。

 
3. The driver needs to do further initialization before the device is ready or it's sure it can support it, so it publishes an invisible device and kicks offa thread to keep working, while returning `ZX_OK`. That thread will eventuallymake the device visible or, if it cannot successfully initialize it, remove it. 3.驱动程序需要在设备准备就绪或可以支持该设备之前进行进一步的初始化，因此它会发布不可见的设备并踢出fa线程以继续工作，同时返回“ ZX_OK”。该线程最终将使该设备可见，或者，如果无法成功对其进行初始化，则将其删除。

 
4. The driver represents a bus or controller with 0..n children which may dynamically appear or disappear. In this case it should publish a deviceimmediately representing the bus or controller, and then dynamically publishchildren (that downstream drivers will bind to) representing hardware on thatbus. Examples: AHCI/SATA, USB, etc. 4.驱动程序代表具有0..n个子代的总线或控制器，这些子代可能动态出现或消失。在这种情况下，它应该立即发布代表总线或控制器的设备，然后动态发布代表该总线上的硬件的子代（下游驱动程序将绑定到该子代）。例如：AHCI / SATA，USB等

After a device is added and made visible by the system, it is made available to client processes and for binding by compatible drivers. 添加设备并使其对系统可见后，该设备可用于客户端进程并由兼容驱动程序进行绑定。

 
## Device protocols  设备协议 

A driver provides a set of device ops and optional protocol ops to a device. Device ops implement the device lifecycle methods and the external interfaceto the device that are called by other user space applications and services.Protocol ops implement the ddk-internal protocols of the device that arecalled by other drivers. 驱动程序为设备提供一组设备操作和可选协议操作。设备操作实现其他用户空间应用程序和服务所调用的设备生命周期方法和设备的外部接口。协议操作实现其他驱动程序所调用的设备的ddk内部协议。

You can pass one set of protocol ops for the device in `device_add_args_t`. If a device supports multiple protocols, implement the `get_protocol()` deviceop. A device can only have one protocol id. The protocol id corresponds to theclass the device is published under in devfs. 您可以在device_add_args_t中为设备传递一组协议操作。如果设备支持多种协议，则实现`get_protocol（）`deviceop。一台设备只能有一个协议ID。协议ID对应于设备在devfs中发布的类。

Device protocol headers are found in [ddk/protocol/](/zircon/system/ulib/ddk/include/ddk/protocol). Ops and any datastructures passed between drivers should be defined in this header. 设备协议标头位于[ddk / protocol /]（/ zircon / system / ulib / ddk / include / ddk / protocol）中。驱动程序之间传递的操作和任何数据结构都应在此标头中定义。

 
## Driver operation  驾驶员操作 

A driver generally operates by servicing client requests from children drivers or other processes. It fulfills those requests either by communicatingdirectly with hardware (for example, via MMIO) or by communicating with itsparent device (for example, queuing a USB transaction). 驱动程序通常通过服务子驱动程序或其他进程的客户端请求来进行操作。它通过与硬件直接通信（例如，通过MMIO）或与其父设备进行通信（例如，对USB事务进行排队）来满足这些请求。

External client requests from processes outside the devhost are fulfilled by children drivers, generally in the same process, are fulfilled by deviceprotocols corresponding to the device class. Driver-to-driver requests shoulduse device protocols instead of device ops. 来自devhost外部进程的外部客户端请求由子驱动程序满足，通常在同一进程中由与设备类相对应的设备协议满足。驾驶员对驾驶员的请求应使用设备协议而不是设备操作。

A device can get a protocol supported by its parent by calling `device_get_protocol()` on its parent device. 设备可以通过在其父设备上调用device_get_protocol（）来获得其父设备支持的协议。

 
## Device interrupts  设备中断 

Device interrupts are implemented by interrupt objects, which are a type of kernel objects. A driver requests a handle to the device interrupt from itsparent device in a device protocol method. The handle returned will be boundto the appropriate interrupt for the device, as defined by a parent driver.For example, the PCI protocol implements `map_interrupt()` for PCI children. Adriver should spawn a thread to wait on the interrupt handle. 设备中断由中断对象实现，中断对象是内核对象的一种。驱动程序通过设备协议方法从其父设备请求设备中断的句柄。返回的句柄将绑定到由父驱动程序定义的设备的适当中断。例如，PCI协议为PCI子代实现`map_interrupt（）`。 Adriver应该产生一个线程来等待中断句柄。

The kernel will automatically handle masking and unmasking the interrupt as appropriate, depending on whether the interrupt is edge-triggeredor level-triggered. For level-triggered hardware interrupts,[zx_interrupt_wait()](/docs/reference/syscalls/interrupt_wait.md) will mask the interruptbefore returning and unmask the interrupt when it is called again the nexttime. For edge-triggered interrupts, the interrupt remains unmasked. 内核将根据中断是边沿触发还是电平触发来自动处理屏蔽和取消屏蔽中断。对于级别触发的硬件中断，[zx_interrupt_wait（）]（/ docs / reference / syscalls / interrupt_wait.md）将在返回之前屏蔽该中断，并在下次再次调用该中断时取消屏蔽。对于边沿触发的中断，该中断保持未屏蔽状态。

The interrupt thread should not perform any long-running tasks. For drivers that perform lengthy tasks, use a worker thread. 中断线程不应执行任何长时间运行的任务。对于执行冗长任务的驱动程序，请使用辅助线程。

You can signal an interrupt handle with [zx_interrupt_trigger()](/docs/reference/syscalls/interrupt_trigger.md) on slot**ZX_INTERRUPT_SLOT_USER** to return from `zx_interrupt_wait()`. This isnecessary to shut down the interrupt thread during driver clean up. 您可以在插槽** ZX_INTERRUPT_SLOT_USER **上通过[zx_interrupt_trigger（）]（/ docs / reference / syscalls / interrupt_trigger.md）发出中断句柄信号，以从zx_interrupt_wait（）返回。在清理驱动程序期间，有必要关闭中断线程。

 
## FIDL Messages  FIDL消息 

Messages for each device class are defined in the [FIDL](/docs/development/languages/fidl/README.md) language.Each device implements zero or more FIDL protocols, multiplexed over a singlechannel per client.  The driver is given the opportunity to interpret FIDLmessages via the `message()` hook. 每个设备类的消息都以[FIDL]（/ docs / development / languages / fidl / README.md）语言定义。每个设备实现零个或多个FIDL协议，每个客户端通过单个通道多路复用。通过`message（）`钩子，驱动程序有机会解释FIDLmessages。

 
## Protocol ops vs. FIDL messages  协议操作与FIDL消息 

Protocol ops define the DDK-internal API for a device. FIDL messages define the external API.  Define a protocol op if the function is meant to be called byother drivers.  A driver should call a protocol op on its parent to make use ofthose functions. 协议操作定义了设备的DDK内部API。 FIDL消息定义了外部API。如果要由其他驱动程序调用该函数，请定义协议op。驱动程序应在其父级上调用协议op以使用这些功能。

 
## Isolate devices  隔离设备 

Devices that are added with `DEVICE_ADD_MUST_ISOLATE` spawn a new proxy devhost. The device exists in both the parent devhost and as the root of the new devhost.Devmgr attempts to load **driver**`.proxy.so` into this proxy devhost. For example,PCI is supplied by `libpci.so` so devmgr would look to load `libpci.proxy.so`. Thedriver is provided a channel in `create()` when it creates the proxy device(the "bottom half" that runs in the new devhost). The proxy device should cachethis channel for when it needs to communicate with the top half (e.g. ifit needs to call API on the parent device). 添加了“ DEVICE_ADD_MUST_ISOLATE”的设备会产生一个新的代理devhost。该设备既存在于父devhost中，又作为新devhost的根存在.Devmgr尝试将** driver **。proxy.so`加载到此代理devhost中。例如，PCI由`libpci.so`提供，因此devmgr希望加载`libpci.proxy.so`。当驱动程序创建代理设备（在新devhost中运行的“下半部分”）时，会在`create（）`中为该驱动程序提供一个通道。代理设备应在需要与上半部分通信时（例如，如果它需要在父设备上调用API）缓存该通道。

`rxrpc()` is invoked on the top half when this channel is written to by the bottom half. There is no common wire protocol for this channel. For anexample, refer to the [PCI driver](/zircon/system/dev/bus/pci). 当该通道由下半部分写入时，在上半部分调用`rxrpc（）`。该通道没有通用的有线协议。有关示例，请参阅[PCI驱动程序]（/ zircon / system / dev / bus / pci）。

Note: This is a mechanism used by various bus devices and not something general drivers should have to worry about. (please ping swetland if you thinkyou need to use this) 注意：这是各种总线设备使用的一种机制，而普通驱动程序不必担心。 （如果您认为需要使用此功能，请ping swetland）

 
## Logging  记录中 

[ddk/debug.h](/zircon/system/ulib/ddk/include/ddk/debug.h) defines the `zxlogf(<log_level>,...)` macro. The log messages are printed to the systemdebuglog over the network and on the serial port if available for the device.By default, `ERROR` and `INFO` are always printed. You can control the loglevel for a driver by passing the boot cmdline`driver.<driver_name>.log=+<level>,-<level>`. For example,`driver.sdhci.log=-info,+trace,+spew` enables the `TRACE` and `SPEW` logs anddisable the `INFO` logs for the sdhci driver. [ddk / debug.h]（/ zircon / system / ulib / ddk / include / ddk / debug.h）定义了zzlogf（<log_level>，...）宏。日志消息将通过网络和串行端口打印到系统调试日志中（如果设备可用）。默认情况下，始终会打印``ERROR''和``INFO''。您可以通过传递引导cmdline`driver。<driver_name> .log = + <level>，-<level>`来控制驱动程序的日志级别。例如，driver.sdhci.log = -info，+ trace，+ spew启用sdhci驱动程序的TRACE和SPEW日志并禁用INFO日志。

The log levels prefixed by "L" (`LERROR`, `LINFO`, etc.) do not get sent over the network and are useful for network logging. 前缀为“ L”的日志级别（“ LERROR”，“ LINFO”等）不会通过网络发送，对于网络日志记录很有用。

 
## Driver testing  驱动程序测试 

 
### Manual hardware unit tests  手动硬件单元测试 

A driver may choose to implement the `run_unit_tests()` driver op, which provides the driver a hook in which it may run unit tests at systeminitialization with access to the parent device. This means the driver may testits bind and unbind hooks, as well as any interactions with real hardware. Ifthe tests pass (the driver returns `true` from the hook) then operation willcontinue as normal and `bind()` will execute. If the tests fail then the devicemanager will assume that the driver is invalid and never attempt to bind it. 驱动程序可以选择实现`run_unit_tests（）`驱动程序op，该驱动程序为驱动程序提供了一个钩子，可以在系统初始化时通过访问父设备来运行单元测试。这意味着驱动程序可以测试其绑定和取消绑定挂钩，以及与真实硬件的任何交互。如果测试通过（驱动程序从钩子返回“ true”），则操作将继续正常进行，并且将执行“ bind（）”。如果测试失败，则设备管理器将假定驱动程序无效，并且从不尝试将其绑定。

Since these tests must run at system initialization (in order to not interfere with the usual operation of the driver) they are activated via a [kernel commandline flag](/docs/reference/kernel/kernel_cmdline.md). To enable the hook for a specific driver, use`driver.<name>.tests.enable`. Or for all drivers: `driver.tests.enable`. If adriver doesn't implement `run_unit_tests()` then these flags will have noeffect. 由于这些测试必须在系统初始化时运行（为了不干扰驱动程序的正常运行），因此可以通过[内核命令行标志]（/ docs / reference / kernel / kernel_cmdline.md）激活它们。要为特定驱动程序启用挂钩，请使用driver。<name> .tests.enable。或对于所有驱动程序：`driver.tests.enable`。如果驱动程序未实现`run_unit_tests（）`，则这些标志将无效。

`run_unit_tests()` passes the driver a channel for it to write test output to. Test output should be in the form of `fuchsia.driver.test.Logger` FIDL messages.The driver-unit-test library contains a [helper class][] that integrates withzxtest and handles logging for you. run_unit_tests（）向驱动程序传递一个通道，以供其将测试输出写入其中。测试输出应采用“ fuchsia.driver.test.Logger” FIDL消息的形式。driver-unit-test库包含[helper class] []，与zxtest集成并为您处理日志。

[helper class]: /zircon/system/ulib/driver-unit-test/include/lib/driver-unit-test/logger.h  [帮助程序类]：/zircon/system/ulib/driver-unit-test/include/lib/driver-unit-test/logger.h

 

 
### Integration tests  整合测试 

`ZX_PROTOCOL_TEST` provides a mechanism to test drivers by running the driver under test in an emulated environment. Write a driver that binds to a`ZX_PROTOCOL_TEST` device. This driver should publish a device that the driverunder test can bind to, and it should implement the protocol functions thedriver under test invokes in normal operation. This helper driver should bedeclared with `BI_ABORT_IF_AUTOBIND` in the bindings. ZX_PROTOCOL_TEST提供了一种通过在仿真环境中运行被测驱动程序来测试驱动程序的机制。编写绑定到`ZX_PROTOCOL_TEST`设备的驱动程序。该驱动程序应发布被测驱动程序可以绑定到的设备，并且应实现被测驱动程序在正常操作中调用的协议功能。应当在绑定中使用“ BI_ABORT_IF_AUTOBIND”声明此辅助驱动程序。

The test harness calls `fuchsia.device.test.RootDevice/CreateDevice` on `/dev/test/test`, which will create a `ZX_PROTOCOL_TEST` device and returnits path. Then it calls `fuchsia.device.Controller/Bind` with the helper driver on thenewly created device.  This approach generally works better for mid-layerprotocol drivers. It's possible to emulate real hardware with the sameapproach but it may not be as useful. 测试工具在`/ dev / test / test`上调用`fuchsia.device.test.RootDevice / CreateDevice`，这将创建一个`ZX_PROTOCOL_TEST`设备并返回其路径。然后在新创建的设备上使用辅助驱动程序调用`fuchsia.device.Controller / Bind`。这种方法通常对中间层协议驱动程序更好。可以使用相同的方法来模拟真实的硬件，但可能没有用。

 

The bindings defined in [test.banjo](/zircon/system/banjo/ddk.protocol.test/test.banjo) are usedfor testing libraries that run as part of a driver. For an example, refer to[system/ulib/ddk/test](/zircon/system/ulib/ddk/test). The test harness for thesetests is[system/utest/driver-test/main.cc](/zircon/system/utest/driver-test/main.cc) [test.banjo]（/ zircon / system / banjo / ddk.protocol.test / test.banjo）中定义的绑定用于测试作为驱动程序一部分运行的库。有关示例，请参阅[system / ulib / ddk / test]（/ zircon / system / ulib / ddk / test）。这些测试的测试工具是[system / utest / driver-test / main.cc]（/ zircon / system / utest / driver-test / main.cc）

 
## Driver rights  驾驶员权利 

Although drivers run in user space processes, they have a more restricted set of rights than normal processes. Drivers are not allowed to access thefilesystem, including devfs. That means a driver cannot interact witharbitrary devices. If your driver needs to do this, consider writing a serviceinstead. For example, the virtual console is implemented by the[virtcon](/src/bringup/virtcon) service. 尽管驱动程序在用户空间进程中运行，但与普通进程相比，它们具有更多受限制的权限。驱动程序不允许访问文件系统，包括devfs。这意味着驱动程序无法与任意设备进行交互。如果您的驱动程序需要这样做，请考虑改为编写服务。例如，虚拟控制台由[virtcon]（/ src / bringup / virtcon）服务实现。

Privileged operations such as `zx_vmo_create_contiguous()` and [zx_interrupt_create](/docs/reference/syscalls/interrupt_create.md) require a root resourcehandle. This handle is not available to drivers other than the system driver([ACPI](/zircon/system/dev/board/x86) on x86 systems and[platform](/zircon/system/dev/bus/platform) on ARM systems). A device shouldrequest its parent to perform such operations for it. Contact the authorof the parent driver if its protocol does not address this use case. 诸如zx_vmo_create_contiguous（）和[zx_interrupt_create]（/ docs / reference / syscalls / interrupt_create.md）之类的特权操作需要根资源句柄。该句柄不适用于x86系统上的系统驱动程序（[ACPI]（/ zircon / system / dev / board / x86）和ARM系统上的[platform]（/ zircon / system / dev / bus / platform）以外的驱动程序）。设备应请求其父设备为其执行此类操作。如果其协议不能解决该用例，请与父驱动程序的作者联系。

