 
# Zircon's Platform Bus  Zircon的平台巴士 

 
## Introduction  介绍 

The term **platform bus** refers to a specific Zircon driver with source code located at [//fuchsia/zircon/system/dev/bus/platform/](../../../zircon/system/dev/bus/platform/)).However this term also refers to the framework that manages the lower level drivers in Zircon.In this document, **platform bus driver** refers to a specific driver and **platform bus**refers to the general framework. 术语“平台总线”是指特定的Zircon驱动程序，其源代码位于[//fuchsia/zircon/system/dev/bus/platform/](../../../zircon/system/dev / bus / platform /））。但是，该术语还指代管理Zircon中较低级驱动程序的框架。在本文档中，** platform bus driver **是指特定的驱动程序，** platform bus **是指一般框架。

The platform bus as a whole contains several types of drivers:  整个平台总线包含几种类型的驱动程序：

 
- The **platform bus driver**, which manages the platform bus. This is a generic driver with no hardware specific functionality. The platform bus driver is started automaticallyby the devmgr when the system boots. -**平台总线驱动程序**，用于管理平台总线。这是没有硬件特定功能的通用驱动程序。系统启动时，devmgr会自动启动平台总线驱动程序。

 
- The **board driver**, which is the first driver loaded by the platform bus driver. The board driver contains all the platform specific information needed by the platform busand controls what other drivers will be loaded by the platform bus.On arm64 platforms, the platform bus driver uses information from the bootloader or boot shimto bind the correct board driver for the platform it is running on.On x86 platforms, the platform bus driver always loads the x86 board driver and creates platformdevices based on information from ACPI. -**板驱动程序**，这是平台总线驱动程序加载的第一个驱动程序。板卡驱动程序包含平台总线所需的所有特定于平台的信息，并控制平台总线将加载其他驱动程序。在arm64平台上，平台总线驱动程序使用来自引导加载程序或引导程序的信息来为平台绑定正确的板卡驱动程序在x86平台上，平台总线驱动程序始终加载x86板驱动程序并根据ACPI信息创建平台设备。

 
- The **platform device drivers** are the foundations for the higher level drivers in Zircon. These drivers provide the lowest level of support for a particular feature, like USB,eMMC or NAND storage, etc., with higher level drivers loading on top of that. -**平台设备驱动程序**是Zircon中更高级别驱动程序的基础。这些驱动程序为特定功能（如USB，eMMC或NAND存储等）提供最低级别的支持，并在其上加载更高级别的驱动程序。

 
- The **protocol implementation drivers** are drivers that provide protocols that are needed by the board driver. One common example of this is the GPIO driver, which is often needed by theboard driver for pin-muxing. In the past, the platform bus used to also proxy these drivers'protocols to platform devices, but now we use composite devices instead.Over time we will likely phase out the use of protocol implementation drivers in the platform busand replace it with a new approach that does not require blocking to wait for drivers to load. -协议实施驱动程序是提供板级驱动程序所需协议的驱动程序。 GPIO驱动程序是一个常见的示例，板载驱动程序通常需要使用该GPIO进行引脚复用。过去，平台总线也曾经将这些驱动程序的协议代理到平台设备，但现在我们使用复合设备。随着时间的流逝，我们可能会逐步淘汰平台总线中协议实现驱动程序的使用，并以新方法代替它不需要阻塞即可等待驱动程序加载。

 
- Finally, the **platform proxy driver** a companion to the platform bus driver that loads into the platform device devhosts. This driver supports proxying the platform device protocoland other resource protocols from the platform device driver to the platform bus driver andprotocol implementation drivers. This is needed because the platform device drivers run in adifferent devhost process than the platform bus driver and the protocol implementation drivers. -最后，“平台代理驱动程序” **是平台总线驱动程序的伴侣，该驱动程序加载到平台设备devhosts中。该驱动程序支持代理平台设备协议和其他资源协议，从平台设备驱动程序到平台总线驱动程序和协议实现驱动程序。之所以需要这样做，是因为平台设备驱动程序在与平台总线驱动程序和协议实现驱动程序不同的devhost进程中运行。

![Zircon Platform Bus diagram](platform-bus.png) Source: [https://goto.google.com/zircon-platform-bus-diagram](https://goto.google.com/zircon-platform-bus-diagram) ！[Zircon平台总线图]（platform-b​​us.png）来源：[https://goto.google.com/zircon-platform-b​​us-diagram]（https://goto.google.com/zircon-platform-总线图）

 
## Platform Bus Initialization  平台总线初始化 

The platform bus driver is started automatically by the devmgr at boot. Since the platform bus driver is a generic driver that contains no information about theplatform it is running on, it first loads the board driver, which handles platform specific logic.To determine which board driver to load, platform bus driver reads the `ZBI_TYPE_PLATFORM_ID`record from the [ZBI data](../../../zircon/system/public/zircon/boot/image.h) passed from thebootloader. It then adds a device with protocol `ZX_PROTOCOL_PBUS` with the`BIND_PLATFORM_DEV_VID` and `BIND_PLATFORM_DEV_PID` binding variables set to the vid and didfrom the platform data record. The correct board driver will bind to this device and continuethe platform bus initialization process. On x86 platforms, the x86 board driver is loadedautomatically. 平台总线驱动程序在启动时由devmgr自动启动。由于平台总线驱动程序是通用驱动程序，不包含有关其运行平台的信息，因此它首先加载处理平台特定逻辑的板卡驱动程序。要确定要加载的板卡驱动程序，平台总线驱动程序会读取“ ZBI_TYPE_PLATFORM_ID”记录从引导加载程序传递的[ZBI数据]（../../../ zircon / system / public / zircon / boot / image.h）中。然后，它添加一个协议为ZX_PROTOCOL_PBUS的设备，并将BIND_PLATFORM_DEV_VID和BIND_PLATFORM_DEV_PID绑定变量设置为从平台数据记录中获取的vid和did。正确的板卡驱动程序将绑定到此设备，并继续平台总线初始化过程。在x86平台上，将自动加载x86板驱动程序。

The board driver uses the platform bus protocol to communicate with the platform bus driver. After it does its own initialization, the board driver then uses the `ProtocolDeviceAdd()`call in the platform bus protocol to load protocol implementation drivers.After the protocol implementation driver loads, it must register its protocol with the platform busdriver by calling the  platform bus `RegisterProtocol()` API.`ProtocolDeviceAdd()` will block until the driver calls `RegisterProtocol()`, so the board drivermust call `RegisterProtocol()` from one of its own threads rather than a devmgr callback like`Bind()`. 板驱动程序使用平台总线协议与平台总线驱动程序进行通信。板卡驱动程序自行初始化后，然后使用平台总线协议中的ProtocolDeviceAdd（）调用来加载协议实现驱动程序。协议实现驱动程序加载后，必须通过调用平台向平台总线驱动程序注册其协议。总线“ RegisterProtocol（）” API。“ ProtocolDeviceAdd（）”将阻塞，直到驱动程序调用“ RegisterProtocol（）”，因此开发板驱动程序必须从其自己的线程之一而不是像`Bind（）这样的devmgr回调中调用“ RegisterProtocol（）”。 ）`。

After the protocol devices are added, the board driver will call the `DeviceAdd()` call in the platform bus protocol to create platform devices, which will result inplatform device drivers loading each in its own devhost.After the platform devices are created, the platform bus initialization is complete. 添加协议设备后，板驱动程序将在平台总线协议中调用“ DeviceAdd（）”调用以创建平台设备，这将导致平台设备驱动程序将每个设备加载到其自己的devhost中。创建平台设备后，平台总线初始化完成。

 
## Composite Platform Devices  复合平台设备 

The platform bus also supports adding platform devices to be used as components in composite devices. The platform bus `CompositeDeviceAdd()` call adds a composite device, with the zerothcomponent being a platform device described by the provided `PBusDev` struct.The binding rules for the remaining components are provided by the `components` parameter.The `coresident_device_index` is used to specify which devhost the composite deviceshould be created in. A value of `UINT32_MAX` will result in a new devhost being created for thecomposite device, while a value of 1 through n will add the composite device to the devhost of oneof the other components. Passing 0 is not allowed, since we do not want the composite deviceto be added to the platform bus driver's devhost. 平台总线还支持添加平台设备以用作复合设备中的组件。平台总线CompositeDeviceAdd（）调用添加了一个复合设备，第零个组件是由提供的PBusDev结构描述的平台设备。其余组件的绑定规则由components参数提供。coresident_device_index用于指定要在其中创建复合设备的devhost。值“ UINT32_MAX”将导致为复合设备创建一个新的devhost，而值1到n会将复合设备添加到另一个设备的devhost中。组件。不允许传递0，因为我们不希望将复合设备添加到平台总线驱动程序的devhost中。

The internals of composite platform devices are a bit different than the non-composite case. Instead of using the platform proxy driver, the devmgr **component** and **component proxy** driversproxy the platform device protcol instead. For example, in the diagram above we have a composite devicefor an audio driver with a platform device as its first component and an I2C channel as its second.The audio driver is started in a new devhost, and the devmmgr component and component proxy driversare responsible for proxying the PDEV and I2C protocols to the audio driver. 复合平台设备的内部结构与非复合情况有些不同。 devmgr ** component **和** component proxy **驱动程序代替了平台代理驱动程序，而是代理了平台设备协议。例如，在上图中，我们有一个用于音频驱动程序的复合设备，该设备的第一个组件是平台设备，第二个组件是I2C通道。音频驱动程序在新的devhost中启动，而devmmgr组件和组件代理驱动程序负责用于将PDEV和I2C协议代理到音频驱动程序。

 
## Platform Device Protocol  平台设备协议 

The [platform device protocol](../../..//zircon/system/banjo/ddk.protocol.platform.device/platform-device.banjo) (`ZX_PROTOCOL_PDEV`) is the main protocol provided by the platform bus toplatform device drivers. This protocol provides access to resources like MMIO ranges, interrupts,BTIs, and SMC ranges to the platform device driver. Rather than requesting MMIOs and interrupts byphysical addresses or IRQ numbers, these resource are requested by a zero-based index.This allows us to have platform device drivers for particular IP that works across multipleplatforms, since the knowledge of the exact MMIO addresses and interrupt numbers do not need to beknown by the driver. Instead the board driver configures the MMIO addresses and IRQ numbers in the`PbusDev` struct passed via `AddDevice()`. [平台设备协议]（../../..// zircon / system / banjo / ddk.protocol.platform.device / platform-device.banjo）（`ZX_PROTOCOL_PDEV`）是平台提供的主要协议总线到平台设备驱动程序。该协议提供对平台设备驱动程序的MMIO范围，中断，BTI和SMC范围等资源的访问。这些资源不是通过物理地址或IRQ号来请求MMIO和中断，而是通过从零开始的索引来请求这些资源。这使我们能够为跨多个平台工作的特定IP提供平台设备驱动程序，因为知道确切的MMIO地址和中断号不需要驾驶员知道。相反，板驱动程序在通过AddDevice（）传递的PbusDev结构中配置MMIO地址和IRQ号。

The platform device protocol is also available to protocol implementation drivers. For example, a GPIO driver may use the platform device protocol to access its MMIO and interrupts.This allows protocol implementation drivers to be shared among different SOC variants,where the functionality may be identical but the MMIO addresses and interrupt numbers may bedifferent. 平台设备协议也可用于协议实现驱动程序。例如，GPIO驱动程序可以使用平台设备协议访问其MMIO和中断。这允许协议实现驱动程序在不同的SOC变体之间共享，其中功能可能相同，但MMIO地址和中断号可能不同。

 
## Platform Bus Protocol  平台总线协议 

The [platform bus protocol](../../..//zircon/system/banjo/ddk.protocol.platform.bus/platform-bus.banjo) (`ZX_PROTOCOL_PBUS`) is used by board drivers and protocol implementation driversto communicate with the platform bus driver. It is only available to drivers running in theplatform bus's devhost (in particular, it is not accessible to platform device drivers).The purpose of this protocol is for the board driver to load protocol implementation driversand to start platform device drivers. It is also used by protocol implementation drivers toregister their protocols with the platform bus so their protocols can be made availableto platform device drivers. 平台驱动程序和协议实现使用[平台总线协议]（../../..// zircon / system / banjo / ddk.protocol.platform.bus / platform-b​​us.banjo）（`ZX_PROTOCOL_PBUS`）驱动程序与平台总线驱动程序进行通信。它仅对在平台总线的devhost中运行的驱动程序可用（尤其是平台设备驱动程序无法访问）。此协议的目的是使板驱动程序加载协议实现驱动程序并启动平台设备驱动程序。协议实现驱动程序还使用它在平台总线上注册其协议，以便它们的协议可用于平台设备驱动程序。

