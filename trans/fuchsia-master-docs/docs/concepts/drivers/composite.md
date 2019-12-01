 

 
# Composite Devices  复合设备 

This document is part of the [Zircon Driver Development Kit](/docs/concepts/drivers/overview.md)documentation. 本文档是[Zircon驱动程序开发套件]（/ docs / concepts / drivers / overview.md）文档的一部分。

[TOC]  [目录]

 
## Introduction  介绍 

In this section, we look at **composite devices**. A composite device is a device composed of other devices. 在本节中，我们将研究“复合设备”。复合设备是由其他设备组成的设备。

These devices address the case of hardware-level composition, in which a "device" (from the user's perspective) is implemented by severaldistinct hardware blocks. 这些设备解决了硬件级组合的情况，其中“设备”（从用户的角度来看）是由几个不同的硬件模块实现的。

Examples include:  示例包括：

 
* a touch panel composed of an I2C device and a GPIO,  *由I2C设备和GPIO组成的触摸面板，
* an ethernet device composed of a MAC chip and one or more PHYs, or  *由MAC芯片和一个或多个PHY组成的以太网设备，或者
* an audio device composed of an audio controller and a set of codecs.  *由音频控制器和一组编解码器组成的音频设备。

In these situations, the relationship of the hardware is known to the board driver at boot time (either statically or through a dynamic means, such asACPI). 在这些情况下，板驱动程序在引导时（静态地或通过动态方式（例如ACPI））就知道硬件的关系。

We'll use the `astro-audio` device for our examples:  我们将在示例中使用“ astro-audio”设备：

![Figure: Composite hardware device on I2C bus with GPIOs](composite-audio.png)  ！[图：具有GPIO的I2C总线上的复合硬件设备]（composite-audio.png）

This device features:  该设备功能：

 
* an I2C bus interface  * I2C总线接口
* two sets of GPIOs (one for fault, one for enable)  *两套GPIO（一套用于故障，一套用于启用）
* MMIO (memory mapped I/O) for bulk data transfer, and  * MMIO（内存映射的I / O）用于批量数据传输，以及
* an IRQ (interrupt request) line to generate interrupts to the driver.  * IRQ（中断请求）行，以生成对驱动程序的中断。

Note that the `ZX_PROTOCOL_I2C` and `ZX_PROTOCOL_GPIO` protocols are used to transfer data; that is, I2C messages, and GPIO pin status are sent and receivedvia the respective drivers. 注意，`ZX_PROTOCOL_I2C`和`ZX_PROTOCOL_GPIO`协议用于传输数据。也就是说，通过相应的驱动程序发送和接收I2C消息和GPIO引脚状态。

The `ZX_PROTOCOL_PDEV` part is different. Here, the protocol is used only to grant access (the green checkmarks in thediagram) to the MMIO and IRQ; the actual MMIO data and interrupts are **not**handled by the `PDEV`; they're handled directly by the `astro-audio` driveritself. ZX_PROTOCOL_PDEV部分不同。这里，该协议仅用于授予对MMIO和IRQ的访问权限（图中的绿色复选标记）；实际的MMIO数据和中断不是由PDEV处理的；它们由“ astro-audio”驱动程序本身直接处理。

 
## Creating a composite device  创建复合设备 

To create a composite device, a number of data structures need to be set up.  要创建复合设备，需要设置许多数据结构。

 
### Binding instructions  装订说明 

We need a number of binding instructions (`zx_bind_inst_t`) that tell us which devices we match.These binding instructions are the ones we've already discussed in the["Registration" topic](simple.md#Registration) in the introduction section. 我们需要许多绑定指令（`zx_bind_inst_t`）来告诉我们我们匹配的设备。这些绑定指令是我们在简介部分的[“ Registration”主题]（simple.mdRegistration）中已经讨论过的。

For the `astro-audio` device, we have:  对于“ astro-audio”设备，我们有：

```c
static const zx_bind_inst_t root_match[] = {
    BI_MATCH(),
};

static const zx_bind_inst_t i2c_match[] = {
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_I2C),
    BI_ABORT_IF(NE, BIND_I2C_BUS_ID, ASTRO_I2C_3),
    BI_MATCH_IF(EQ, BIND_I2C_ADDRESS, I2C_AUDIO_CODEC_ADDR),
};

static const zx_bind_inst_t fault_gpio_match[] = {
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_GPIO),
    BI_MATCH_IF(EQ, BIND_GPIO_PIN, GPIO_AUDIO_SOC_FAULT_L),
};

static const zx_bind_inst_t enable_gpio_match[] = {
    BI_ABORT_IF(NE, BIND_PROTOCOL, ZX_PROTOCOL_GPIO),
    BI_MATCH_IF(EQ, BIND_GPIO_PIN, GPIO_SOC_AUDIO_EN),
};
```
 

These binding instructions are used to find the devices.  这些绑定说明用于查找设备。

We have four binding instruction arrays; a `root_match[]`, which contains common information for the other three, and then the three devices:the I2C (`i2c_match[]`) device and the two GPIOs (`fault_gpio_match[]` and`enable_gpio_match[]`). 我们有四个绑定指令数组。一个root_match []，包含其他三个设备以及三个设备的公共信息：I2C（i2c_match []`）设备和两个GPIO（`fault_gpio_match []和enable_gpio_match []）。

These instructions are then placed into an array of structures (`device_component_part_t`) which defines each component: 然后将这些指令放入定义每个组件的结构数组（“ device_component_part_t”）中：

![Figure: Binding instructions gathered into a component array](composite-component.png) ！[图：将绑定指令收集到组件数组中]（composite-component.png）

In the `astro-audio` device, we have:  在“ astro-audio”设备中，我们有：

```c
static const device_component_part_t i2c_component[] = {
    { countof(root_match), root_match },
    { countof(i2c_match), i2c_match },
};

static const device_component_part_t fault_gpio_component[] = {
    { countof(root_match), root_match },
    { countof(fault_gpio_match), fault_gpio_match },
};

static const device_component_part_t enable_gpio_component[] = {
    { countof(root_match), root_match },
    { countof(enable_gpio_match), enable_gpio_match },
};
```
 

At this point, we have three component devices, `i2c_component[]`, `fault_gpio_component[]`, and `enable_gpio_component[]`. 此时，我们有三个组件设备：“ i2c_component []”，“ fault_gpio_component []”和“ enable_gpio_component []”。

 
### Component device matching rules  组件设备匹配规则 

The following rules apply:  适用以下规则：

 
1. The first element must describe the root of the device tree &mdash; this is why we've used the mnemonic `root_match` identifier.Note that this requirement is likely to change, since most users providean "always match" anyway. 1.第一个元素必须描述设备树的根mdash；这就是为什么我们使用助记符“ root_match”标识符的原因。请注意，由于大多数用户仍会提供“始终匹配”的条件，因此此要求可能会发生变化。
2. The last element must describe the target device itself.  2.最后一个元素必须描述目标设备本身。
3. The remaining elements must match devices on the path from the root to the target device, in order.Some of those **devices** may be skipped, but every **element** mustbe matched. 3.其余元素必须按顺序匹配从根到目标设备的路径上的设备。其中一些“设备”可能会被跳过，但是每个“元素”都必须匹配。
4. Every device on the path that has a property from the range `BIND_TOPO_START` through `BIND_TOPO_END` (basically buses, like I2Cand PCI) must be matched.These sequences of matches must be unique. 4.路径上具有从“ BIND_TOPO_START”到“ BIND_TOPO_END”范围的属性的每个设备（基本上是总线，如I2C和PCI）都必须匹配。这些匹配序列必须唯一。

Finally, we combine them into an aggregate called `components[]` of type `device_component_t`: 最后，我们将它们组合成一个名为device_component_t的聚合称为components []：

![Figure: Gathering components into an aggregate](composite-components.png)  ！[图：将组件收集到集合中]（composite-components.png）

This now gives us a single identifier, `components[]`, that we can use when creating the composite device. 现在，这为我们提供了一个单一的标识符“ components []”，我们可以在创建复合设备时使用它。

In `astro-audio`, this looks like:  在`astro-audio`中，它看起来像：

```c
static const device_component_t components[] = {
    { countof(i2c_component), i2c_component },
    { countof(fault_gpio_component), fault_gpio_component },
    { countof(enable_gpio_component), enable_gpio_component },
};
```
 

 
### Creating the device  创建设备 

For simple (non-composite) devices, we used **device_add()** (which we saw in the ["Registration" section](simple.md#Registration) previously). 对于简单的（非复合）设备，我们使用** device_add（）**（之前在[“ Registration”部分]（simple.mdRegistration）中看到的）。

For composite devices, we use **device_add_composite()**:  对于复合设备，我们使用** device_add_composite（）**：

```c
zx_status_t device_add_composite(
    zx_device_t* dev,
    const char* name,
    const zx_device_prop_t* props,
    size_t props_count,
    const device_component_t* components,
    size_t components_count,
    uint32_t coresident_device_index);
```
 

The arguments are as follows:  参数如下：

Argument                  | Meaning --------------------------|---------------------------------------------------`dev`                     | Parent device`name`                    | The name of the device`props`                   | Properties ([see "Declaring a Driver"](driver-development.md#declaring-a-driver))`props_count`             | How many entries are in `props``components`              | The individual component devices`components_count`        | How many entries are in `components``coresident_device_index` | Which devhost to use 争论含义-------------------------- | ---------------------- -----------------------------`dev` |父设备名称|设备名称“ props” |属性（[请参见“声明驱动程序”]（driver-development.mddeclaring-a-driver）） props组件中有多少个条目？各个组件设备`components_count` | “ components” coresident_device_index`中有多少个条目？使用哪个devhost

The `dev` value must be the `zx_device_t` corresponding to the "`sys`" device (i.e., the platform bus driver's device). dev的值必须是与“ sys”设备（即平台总线驱动程序的设备）相对应的zx_device_t。

Note that the `coresident_device_index` is used to indicate which devhost the new device should use.If you specify `UINT32_MAX`, the device will reside in a new devhost. 请注意，`coresident_device_index`用来指示新设备应该使用哪个devhost。如果指定`UINT32_MAX`，则设备将驻留在新的devhost中。

> Note that `astro-audio` uses **pbus_composite_device_add()** rather > than **composite_device_add()**.> The difference is that **pbus_composite_device_add()** is an API> provided by the platform bus driver that wraps **composite_device_add()** and> inserts an additional component for ferrying over direct-access resources> such as MMIO, IRQs, and BTIs. >请注意，`astro-audio`使用** pbus_composite_device_add（）**而不是** composite_device_add（）**。>区别在于** pbus_composite_device_add（）**是平台总线驱动程序提供的API>包装** composite_device_add（）**并>插入用于传递直接访问资源的附加组件，例如MMIO，IRQ和BTI。

 
## Using a composite device  使用复合设备 

From a programming perspective, a composite device acts like an ordinary device that implements a `ZX_PROTOCOL_COMPOSITE` protocol.This allows you to access all of the individual components that make up thecomposite device. 从编程的角度来看，复合设备的行为就像实现ZX_PROTOCOL_COMPOSITE协议的普通设备一样，这使您可以访问构成复合设备的所有单个组件。

The first thing to do is get a list of the devices. This is done via **composite_get_components()**: 首先要做的是获取设备列表。这是通过** composite_get_components（）**完成的：

```c
void composite_get_components (
     composite_protocol_t* composite,
     zx_device_t* components,
     size_t component_count,
     size_t* actual_count);
```
 

The arguments are as follows:  参数如下：

Argument          | Meaning ------------------|---------------------------------------------------`composite`       | The protocol handle`components`      | Pointer to an array of `zx_device_t*``component_count` | Size of `components` array`actual_count`    | Actual number of entries filled in `components` 争论含义------------------ | ------------------------------ ---------------------`composite` |协议句柄“组件” |指向`zx_device_t *``component_count`数组的指针| “ components array” actual_count`的大小|填写在“组件”中的实际条目数

The program starts by calling **device_get_protocol()** to get the protocol for the composite driver: 该程序通过调用** device_get_protocol（）**开始以获取复合驱动程序的协议：

```c
composite_protocol_t composite;

auto status = device_get_protocol(parent, ZX_PROTOCOL_COMPOSITE, &composite);
```
 

Assuming there aren't any errors (`status` is equal to `ZX_OK`), the next step is to declare an array of `zx_device_t*` pointers to hold the devices, and call**composite_get_components()**: 假设没有任何错误（状态等于ZX_OK），下一步是声明一个zx_device_t *指针数组来保存设备，并调用** composite_get_components（）**：

```c
enum {
    COMPONENT_I2C,
    COMPONENT_GPIO,
    COMPONENT_COUNT
};

zx_device_t* components[COMPONENT_COUNT];
size_t actual;
composite_get_components(&composite, components, COMPONENT_COUNT, &actual);
if (actual != COMPONENT_COUNT) {
    zxlogf(ERROR, "%s: could not get our components\n", __FILE__);
    return ZX_ERR_INTERNAL;
}
```
 

> The ordering of the devices returned by **device_get_components()** > is defined to be the same as the ordering given to the **device_add_composite()**> call by the board driver.> Therefore, any enums are for convenience, and are not inherently tied to the> ordering.> Many composite devices will have a fixed number of components in a specific> order, but there may also be composite devices that have a variable number> of components, in which case the components might be identified by device> metadata (via **device_get_metadata()**), or by some other means. >定义** device_get_components（）**返回的设备的顺序与板卡驱动程序给** device_add_composite（）**>调用的顺序相同。因此，任何枚举都是为了方便，而不是固有地与>顺序相关联。>许多复合设备将按特定的>顺序具有固定数量的组件，但是也可能有复合设备具有可变数量的组件，在这种情况下，这些组件可能可以通过device>元数据（通过** device_get_metadata（）**）或其他方式进行标识。

 
## Advanced Topics  进阶主题 

Here we discuss some specialized / advanced topics.  在这里，我们讨论一些专门的/高级的主题。

 
### Composite devices and proxies  复合设备和代理 

What's actually going on in the `astro-audio` driver is a little more complex than initially shown: astro-audio驱动程序中实际发生的事情比最初显示的要复杂一些：

![Figure: Composite hardware device using proxies](composite-proxy.png)  ！[图：使用代理的复合硬件设备]（composite-proxy.png）

The components are bound to an internal driver (located in the [//zircon/system/core/devmgr/component][component] directory). 组件绑定到内部驱动程序（位于[// zircon / system / core / devmgr / component] [component]目录中）。

The driver handles proxying across process boundaries if necessary. This proxying uses the `DEVICE_ADD_MUST_ISOLATE` mechanism (introducedin the [Isolate devices][isolate] section). 如果需要，驱动程序将处理跨进程的代理。此代理使用“ DEVICE_ADD_MUST_ISOLATE”机制（在[隔离设备] [隔离]部分中引入）。

When a device is added with `DEVICE_ADD_MUST_ISOLATE`, two devices end up being created:the normal device, in the same process as its parent, and a proxy. 当使用“ DEVICE_ADD_MUST_ISOLATE”添加设备时，最终将创建两个设备：与父设备相同的正常设备和一个代理。

The proxy is created in a new devhost; if the normal device's driver is `normal.so`, then its driver is `normal.proxy.so`.This driver is expected to implement a **create()** method which calls**device_add()** and stashes the IPC channel it's given.That channel will be used later for communicating with the normaldevice in order to satisfy the proxy's children's requests. 代理是在新的devhost中创建的；如果普通设备的驱动程序是“ normal.so”，则其驱动程序是“ normal.proxy.so”。该驱动程序应实现** create（）**方法，该方法调用** device_add（）**并隐藏IPC通道，该通道稍后将用于与普通设备进行通信，以满足代理的子级请求。

The normal device implements the `rxrpc` hook, which is invoked by the driver runtime each time a message is received from the channelshared with the proxy. 普通设备实现“ rxrpc”钩子，每次从与代理共享的通道接收到消息时，驱动程序运行时就会调用该钩子。

So, in order to implement a new protocol proxy, one must modify the `component.proxy.so` drivers to handle the desired protocol by sendingmessages to the normal device, and modify the `component.so` driver toservice those messages appropriately. 因此，为了实现一种新的协议代理，必须修改“ component.proxy.so”驱动程序以通过向正常设备发送消息来处理所需的协议，并修改“ component.so”驱动程序以适当地服务那些消息。

The component proxy is implemented in [/zircon/system/core/devmgr/component/component-proxy.cpp][component-proxy.cpp], andthe other half in[/zircon/system/core/devmgr/component/component.cpp][component.cpp]. 组件代理在[/zircon/system/core/devmgr/component/component-proxy.cpp][component-proxy.cpp]中实现，另一半在[/ zircon / system / core / devmgr / component / component中实现。 cpp] [component.cpp]。

<!-- xrefs -->  <！-外部参照->

[component-proxy.cpp]: /zircon/system/core/devmgr/component/component-proxy.cc [component.cpp]: /zircon/system/core/devmgr/component/component.cc[component]: /zircon/system/core/devmgr/component/[composite.banjo]: /zircon/system/banjo/ddk.protocol.composite/composite.banjo[driver.h]: /zircon/system/ulib/ddk/include/ddk/driver.h[isolate]: driver-development.md#isolate-devices [component-proxy.cpp]：/ zircon / system / core / devmgr / component / component-proxy.cc [component.cpp]：/ zircon / system / core / devmgr / component / component.cc [component]：/ zircon /system/core/devmgr/component/[composite.banjo]：/zircon/system/banjo/ddk.protocol.composite/composite.banjo[driver.h]：/ zircon / system / ulib / ddk / include / ddk / driver.h [isolate]：driver-development.mdisolate-devices

