 
# Using the C++ DDK Template Library  使用C ++ DDK模板库 

This document is part of the [Driver Development Kit tutorial][ddk-tutorial] documentation.  本文档是[Driver Development Kit教程] [ddk-tutorial]文档的一部分。

The preceding sections in the tutorial have illustrated the basics of what a device driver needs to do (e.g., register its name, handleoperations, etc.) and were presented in C. 本教程的前面各节介绍了设备驱动程序需要执行的操作的基本知识（例如，注册其名称，处理操作等），并以C语言进行了介绍。

In this section, we'll look at the C++ DDK Template Library, or "**DDKTL**" for short. It's a set of C++ templated classes that simplify the work of writing a driverby providing mixins that ensure type safety and perform basic functionality. 在本节中，我们将看一下C ++ DDK模板库，或简称为“ ** DDKTL **”。它是一组C ++模板化类，通过提供可确保类型安全和执行基本功能的混合来简化编写驱动程序的工作。

> If you're not familiar with mixins, you should read the Wikipedia articles on: > * [mixins] and> * [CRTPs &mdash; or Curiously Recurring Template Patterns][crtp]. >如果您不熟悉mixins，则应阅读Wikipedia文章：> * [mixins]和> * [CRTP mdash;或奇怪的重复出现的模板模式] [crtp]。

The mixins that we'll be discussing are defined in [`//zircon/system/ulib/ddktl/include/ddktl/device.h`][/zircon/system/ulib/ddktl/include/ddktl/device.h]. 我们将要讨论的mixin在[`//zircon/system/ulib/ddktl/include/ddktl/device.h`][/zircon/system/ulib/ddktl/include/ddktl/device.h]中定义。

The following mixins are provided:  提供了以下mixin：

Mixin class            | Function             | Purpose -----------------------|----------------------|------------------------------`ddk::GetProtocolable` | **DdkGetProtocol()** | fetches the protocol`ddk::Openable`        | **DdkOpen()**        | client's **open()**`ddk::Closable`        | **DdkClose()**       | client's **close()**`ddk::UnbindableNew`   | **DdkUnbindNew()**   | called when this device is being removed`ddk::Readable`        | **DdkRead()**        | client's **read()**`ddk::Writable`        | **DdkWrite()**       | client's **write()**`ddk::GetSizable`      | **DdkGetSize()**     | returns size of device`ddk::Messageable`     | **DdkMessage()**     | for FIDL IPC messages`ddk::Suspendable`     | **DdkSuspend()**     | to suspend device`ddk::Resumable`       | **DdkResume()**      | to resume device`ddk::Rxrpcable`       | **DdkRxrpc()**       | remote messages for bus devices 混合类|功能介绍目的----------------------- | ---------------------- |- ----------------------------`ddk :: GetProtocolable` | ** DdkGetProtocol（）** |获取协议ddk :: Openable` | ** DdkOpen（）** |客户的open（）** ddk :: Closable` | ** DdkClose（）** |客户的** close（）**`ddk :: UnbindableNew` | ** DdkUnbindNew（）** |在移除此设备时调用ddk :: Readable` | ** DdkRead（）** |客户的** read（）**`ddk :: Writable` | ** DdkWrite（）** |客户的** write（）**`ddk :: GetSizable` | ** DdkGetSize（）** |返回设备`ddk :: Messageable`的大小。 ** DdkMessage（）** | FIDL IPC消息ddk :: Suspendable ** DdkSuspend（）** |暂停设备ddk :: Resumable` | ** DdkResume（）** |恢复设备`ddk :: Rxrpcable` | ** DdkRxrpc（）** |总线设备的远程消息

When defining the class for your device, you specify which functions it will support by including the appropriate mixins.For example (line numbers added for documentation purposes only): 在定义设备的类时，您可以通过包含适当的mixins来指定设备支持的功能，例如（仅出于文档目的添加行号）：

```c++
[01] using DeviceType = ddk::Device<MyDevice,
[02]                                ddk::Openable,        // we support open()
[03]                                ddk::Closable,        // close()
[04]                                ddk::Readable,        // read()
[05]                                ddk::UnbindableNew>;  // and the device can be unbound
```
 

This creates a shortcut to `DeviceType`. The `ddk::Device` templated class takes one or more arguments, with thefirst argument being the base class (here, `MyDevice`).The additional template arguments are the mixins that definewhich DDK device member functions are implemented. 这将创建一个到DeviceType的快捷方式。 ddk :: Device模板类具有一个或多个参数，第一个参数是基类（此处为MyDevice）。其他模板参数是用于定义要实现哪些DDK设备成员函数的混合。

Once defined, we can then declare our device class (`MyDevice`) as inheriting from `DeviceType`: 一旦定义，我们就可以声明我们的设备类（MyDevice）继承自DeviceType：

```c++
[07] class MyDevice : public DeviceType {
[08]   public:
[09]     explicit MyDevice(zx_device_t* parent)
[10]       : DeviceType(parent) {}
[11]
[12]     zx_status_t Bind() {
[13]         // Any other setup required by MyDevice.
[14]         // The device_add_args_t will be filled out by the base class.
[15]         return DdkAdd("my-device-name");
[16]     }
[17]
[18]     // Methods required by the ddk mixins
[19]     zx_status_t DdkOpen(zx_device_t** dev_out, uint32_t flags);
[20]     zx_status_t DdkClose(uint32_t flags);
[21]     zx_status_t DdkRead(void* buf, size_t count, zx_off_t off, size_t* actual);
[22]     void DdkUnbindNew(ddk::UnbindTxn txn);
[23]     void DdkRelease();
[24] };
```
 

Because the `DeviceType` class contains four mixins (lines `[02` .. `05]`: `Openable`, `Closable`, `Readable`, and `UnbindableNew`), we're required to providethe respective function implementations (lines `[18` .. `22]`)in our class. 由于DeviceType类包含四个mixins（第[02 ... 05]行：Openable，Closable，Readable和UnbindableNew），因此我们需要提供相应的函数实现（在我们班级的第[[18` ..`22]`行中。

All DDKTL classes must provide a release function (here, line `[23]` provides **DdkRelease()**), so that's why we didn't specify this in the mixin definitionfor `DeviceType`. 所有DDKTL类都必须提供一个释放函数（此处，第[23]行提供** DdkRelease（）**），因此这就是为什么我们没有在DeviceType的mixin定义中指定它的原因。

> Keep in mind that once you call **DdkAdd()** you _cannot_ safely use the > device instance &mdash; other threads may call **DdkUnbindNew()**, which typically> calls **DdkRelease()**, and that frees the driver's device context.> This would constitute a "use-after-free" violation. >请记住，一旦调用** DdkAdd（）**，就不能安全地使用设备实例mdash；其他线程可以调用** DdkUnbindNew（）**，通常>调用** DdkRelease（）**，从而释放驱动程序的设备上下文。>这将构成“释放后使用”冲突。

Recall from the preceding sections that your device must register with the device manager in order to be usable.This is accomplished as follows: 回想一下前面的部分，您的设备必须在设备管理器中注册才能使用。这可以通过以下步骤完成：

```c++
[26] zx_status_t my_bind(zx_device_t* device,
[27]                     void** cookie) {
[28]     auto dev = std::make_unique<MyDevice>(device);
[29]     auto status = dev->Bind();
[30]     if (status == ZX_OK) {
[31]         // devmgr is now in charge of the memory for dev
[32]         dev.release();
[33]     }
[34]     return status;
[35] }
```
 

Here, **my_bind()** creates an instance of `MyDevice`, calls the **Bind()** routine, and then returns a status. 在这里，my_bind（）创建一个MyDevice的实例，调用Bind（）例程，然后返回一个状态。

**Bind()** (line `[12]` in the `class MyDevice` declaration above), performs whatever setup it needs to, and then calls **DdkAdd()** with the device name. ** Bind（）**（上面的`MyDevice`类声明中的第[12]行），执行所需的任何设置，然后使用设备名称调用** DdkAdd（）**。

After this point, your device is registered with the device manager, and any **open()**, **close()**, and **read()** client callswill now flow to your implementations of **DdkOpen()**, **DdkClose()**,and **DdkRead()**, respectively. 此后，您的设备已在设备管理器中注册，并且任何open（）**，close（）**和read（）**客户端调用现在都将流向** DdkOpen的实现（）**，** DdkClose（）**和** DdkRead（）**。

As an example, in the directory [`//zircon/system/dev/block/zxcrypt`][/zircon/system/dev/block/zxcrypt] we have a typical device declaration ([`device.h`][/zircon/system/dev/block/zxcrypt/device.h]): 例如，在目录[`// zircon / system / dev / block / zxcrypt]] [/ zircon / system / dev / block / zxcrypt]中，我们有一个典型的设备声明（[device.h`] [/ zircon / system / dev / block / zxcrypt / device.h]）：

```c++
[01] class Device;
[02] using DeviceType = ddk::Device<Device,
[03]                                ddk::GetProtocolable,
[04]                                ddk::GetSizable,
[05]                                ddk::UnbindableNew>;
...
[06] class Device final : public DeviceType,
[07]                      public ddk::BlockImplProtocol<Device, ddk::base_protocol>,
[08]                      public ddk::BlockPartitionProtocol<Device>,
[09]                      public ddk::BlockVolumeProtocol<Device> {
[10] public:
...
[11]     // ddk::Device methods; see ddktl/device.h
[12]     zx_status_t DdkGetProtocol(uint32_t proto_id, void* out);
[13]     zx_off_t DdkGetSize();
[14]     void DdkUnbindNew(ddk::UnbindTxn txn);
[15]     void DdkRelease();
...
```
 

Lines `[01` .. `05]` declare the shortcut `DeviceType` with the base class `Device` and three mixins, `GetProtocolable`, `GetSizable`, and `UnbindableNew`. 第[01. ..`05]行声明了带有设备基类Device和三个混合对象GetProtocolable，GetSizable和UnbindableNew的快捷方式DeviceType。

What's interesting here is line `[06]`: we not only inherit from the `DeviceType`, but also from other classes on lines `[07` .. `09]`. 这里有趣的是第[06]行：我们不仅继承自DeviceType，而且还继承了第[07。。。`09]行中的其他类。

Lines `[11` .. `15]` provide the prototypes for the three optional mixins and the mandatory **DdkRelease()** member function. 第[11. ..`15]行提供了三个可选mixin和强制性** DdkRelease（）**成员函数的原型。

Here's an example of the `zxcrypt` device's `DdkGetProtocol` implementation (from [`device.cpp`][/zircon/system/dev/block/zxcrypt/device.cc]): 以下是zxcrypt设备的DdkGetProtocol实现的示例（来自[device.cpp]] [/ zircon / system / dev / block / zxcrypt / device.cc]）：

```c++
zx_status_t Device::DdkGetProtocol(uint32_t proto_id, void* out) {
    auto* proto = static_cast<ddk::AnyProtocol*>(out);
    proto->ctx = this;
    switch (proto_id) {
    case ZX_PROTOCOL_BLOCK_IMPL:
        proto->ops = &block_impl_protocol_ops_;
        return ZX_OK;
    case ZX_PROTOCOL_BLOCK_PARTITION:
        proto->ops = &block_partition_protocol_ops_;
        return ZX_OK;
    case ZX_PROTOCOL_BLOCK_VOLUME:
        proto->ops = &block_volume_protocol_ops_;
        return ZX_OK;
    default:
        return ZX_ERR_NOT_SUPPORTED;
    }
}
```
 

 
# As seen in a driver  正如在驱动程序中看到的 

Let's take a look at how a driver uses the DDKTL.  让我们看一下驱动程序如何使用DDKTL。

We're going to use the USB XHCI driver for this set of code samples; you can find it [here: `//zircon/system/dev/usb/xhci/usb-xhci.cpp`][/zircon/system/dev/usb/xhci//usbx-hci.cc]. 我们将对这组代码示例使用USB XHCI驱动程序；您可以在[[//zircon/system/dev/usb/xhci/usb-xhci.cpp]][/zircon/system/dev/usb/xhci//usbx-hci.cc]中找到它。

In the previous sections, we saw [simple, C-based drivers](simple.md). Recall that those drivers had binding instructions (usually at the bottom of thesource file), like this: 在前面的部分中，我们看到了[基于C的简单驱动程序]（simple.md）。回想一下那些驱动程序具有绑定说明（通常在源文件的底部），如下所示：

```c
ZIRCON_DRIVER_BEGIN(driver_name, driver_ops, "zircon", "0.1", ...)
    // binding instructions
    ...
ZIRCON_DRIVER_END(driver_name)
```
 

The binding instructions bind to a `zx_driver_ops_t` structure as the second parameter to the **ZIRCON_DRIVER_BEGIN()** macro.In the C++ version we use a lambda function to help with initialization: 绑定指令绑定到zz_driver_ops_t结构，作为** ZIRCON_DRIVER_BEGIN（）**宏的第二个参数。在C ++版本中，我们使用lambda函数来帮助初始化：

```c++
namespace usb_xhci {
...
static zx_driver_ops_t driver_ops = [](){
    zx_driver_ops_t ops = {};
    ops.version = DRIVER_OPS_VERSION;
    ops.bind = UsbXhci::Create;
    return ops;
}();

} // namespace usb_xhci

ZIRCON_DRIVER_BEGIN(usb_xhci, usb_xhci::driver_ops, "zircon", "0.1", 9)
```
 

This executes the **driver_ops()** lambda, which returns an initialized `zx_driver_ops_t` structure. Why the lambda? C++ doesn't like partial initialization of structures, so we start with anempty instance of `ops`, set the fields we're interested in, and then return the structure. 这执行** driver_ops（）** lambda，该lambda返回初始化的`zx_driver_ops_t`结构。为什么是lambda？ C ++不喜欢结构的部分初始化，因此我们以`ops'的空实例开始，设置我们感兴趣的字段，然后返回结构。

The **UsbXhci::Create()** function is just like its C counterpart (e.g., **null_bind()** from the [Simple Drivers](simple.md) section), but with a few extras: ** UsbXhci :: Create（）**函数与它的C语言类似（例如，[Simple Drivers]（simple.md）节中的** null_bind（）**），但还有一些其他优点：

```c++
[01] zx_status_t UsbXhci::Create(void* ctx, zx_device_t* parent) {
[02]     fbl::AllocChecker ac;
[03]     auto dev = std::unique_ptr<UsbXhci>(new (&ac) UsbXhci(parent));
[04]     if (!ac.check()) {
[05]         return ZX_ERR_NO_MEMORY;
[06]     }
[07]
[08]     auto status = dev->Init();
[09]     if (status != ZX_OK) {
[10]         return status;
[11]     }
[12]
[13]     // devmgr is now in charge of the device.
[14]     __UNUSED auto* dummy = dev.release();
[15]     return ZX_OK;
[16] }
```
 

First, note the constructor for `dev` (it's the `new ... UsbXhci(parent)` call on line `[03]`) &mdash; we'll come back to it shortly. 首先，请注意`dev`的构造函数（这是`[03]`行上的`new ... UsbXhci（parent）`调用）。我们很快会再谈。

Once `dev` is constructed, line `[08]` calls **dev->Init()**, which serves as a de-multiplexing point calling one of two initialization functions: 构建好dev之后，第[08]行会调用dev-> Init（）**，它充当一个解复用点，调用了以下两个初始化函数之一：

```c++
zx_status_t UsbXhci::Init() {
    if (pci_.is_valid()) {
        return InitPci();
    } else if (pdev_.is_valid()) {
        return InitPdev();
    } else {
        return ZX_ERR_NOT_SUPPORTED;
    }
}
```
 

 
## Parent protocol usage  父协议用法 

Let's follow the path of the `pci_` member by way of the **InitPci()** function. We'll see how the device uses the functions from the parent protocol. 让我们通过** InitPci（）**函数来跟踪pci_成员的路径。我们将看到设备如何使用父协议中的功能。

In **UsbXhci::Create()** the constructor for `dev` initialized the member `pci_` from the `parent` argument.Here are the relevant excerpts from the class definition: 在** UsbXhci :: Create（）**中，`dev`的构造函数从`parent`参数中初始化了成员`pci_`，以下是类定义的相关摘录：

```c++
class UsbXhci: ... {
public:
    explicit UsbXhci(zx_device_t* parent)
        : UsbXhciType(parent), pci_(parent), pdev_(parent) {}
...
prviate:
    ddk::PciProtocolClient pci_;
...
};
```
 

The first use that **InitPci()** makes of the `pci_` member is to get a [**BTI** (Bus Transaction Initiator)][bti] object: ** InitPci（）**对`pci_`成员的首次使用是获得[** BTI **（Bus Transaction Initiator）] [bti]对象：

```c++
zx_status_t UsbXhci::InitPci() {
...
    zx::bti bti;
    status = pci_.GetBti(0, &bti);
    if (status != ZX_OK) {
        return status;
    }
    ...
```
 

This usage is typical.  这种用法很典型。

