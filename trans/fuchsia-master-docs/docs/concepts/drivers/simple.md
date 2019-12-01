<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# Simple Drivers  简单的驱动程序 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

 
## Overview  总览 

In this chapter, we're going to learn about the fundamentals of drivers. We'll progress from simple through to moderately complex, with each driver illustrating aspecific set of concepts as follows: 在本章中，我们将学习驱动程序的基础知识。我们将从简单过渡到中等复杂，每个驱动程序都说明了一组特定的概念，如下所示：

`dev/misc/demo-null` and `dev/misc/demo-zero`:  `dev / misc / demo-null`和`dev / misc / demo-zero`：

 
*   trivial, "no-state" sink / source drivers, used to explain the basics, like how to handle a client's **read()** and **write()** requests. *简单的“无状态”接收器/源驱动程序，用于解释基础知识，例如如何处理客户端的** read（）**和** write（）**请求。

`dev/misc/demo-number`:  `dev / misc / demo-number`：

 
*   a driver that returns an ASCII number, illustrates per-device context, one-shot **read()** operation, and introduces FIDL-based control operations. *返回ASCII码的驱动程序，说明每个设备的上下文，一次读取（read（））操作，并引入基于FIDL的控制操作。

`dev/misc/demo-multi`:  `dev / misc / demo-multi`：

 
*   a driver with multiple sub-devices.  *具有多个子设备的驱动程序。

`dev/misc/demo-fifo`:  `dev / misc / demo-fifo`：

 
*   shows more complex device state, examines partial **read()** and **write()** operations, and introduces state signalling to enable blocking I/O. *显示更复杂的设备状态，检查部分** read（）**和** write（）**操作，并引入状态信令以启用阻塞I / O。

For reference, the source code for all of these drivers is in the `//zircon/system/dev/sample` directory. 作为参考，所有这些驱动程序的源代码位于`// zircon / system / dev / sample`目录中。

 
## Registration  注册 

A system process called the device manager (`devmgr` henceforth) is responsible for device drivers. During initialization, it searches `/boot/driver` and `/system/driver` for drivers.<!-- @@@ TODO Brian says that /system is going away as we transition to a package-basedworld, at which point these drivers will be provided by the package manager in garnet -->These drivers are implemented as Dynamic Shared Objects (**DSO**s), and providetwo items of interest: 一个称为设备管理器的系统进程（此后称为devmgr）负责设备驱动程序。在初始化期间，它将在`/ boot / driver`和`/ system / driver`中搜索驱动程序。<！-@@@ TODO Brian表示/ system在我们过渡到基于软件包的世界时正在消失。驱动程序将由garnet中的程序包管理器提供->这些驱动程序以动态共享对象（** DSO **）的形式实现，并提供了两个感兴趣的项目：

 
*   a set of instructions for `devmgr` to use when evaluating driver binding, and  *一组`devmgr`的说明，用于在评估驱动程序绑定时使用，以及
*   a binding function.  *绑定功能。

Let's look at the bottom of `demo-null.c` in the `dev/sample/null` directory:  让我们看一下dev / sample / null目录中的demo-null.c的底部：

```c
static zx_driver_ops_t demo_null_driver_ops = {
    .version = DRIVER_OPS_VERSION,
    .bind = null_bind,
};

ZIRCON_DRIVER_BEGIN(demo_null_driver, demo_null_driver_ops, "zircon", "0.1", 1)
    BI_MATCH_IF(EQ, BIND_PROTOCOL, ZX_PROTOCOL_MISC_PARENT),
ZIRCON_DRIVER_END(demo_null_driver)
```
 

<!-- @@@ alainv sez these macros are being deprecated in favour of a Driver Binding Language -->  <！-@@@ alainv sez不推荐使用这些宏，而推荐使用驱动程序绑定语言->

The C preprocessor macros `ZIRCON_DRIVER_BEGIN` and `ZIRCON_DRIVER_END` delimit an ELF note section that's created in the DSO.This section contains one or more statements that are evaluated by `devmgr`. C预处理程序宏`ZIRCON_DRIVER_BEGIN`和`ZIRCON_DRIVER_END`界定了在DSO中创建的ELF注释部分。该部分包含一个或多个由`devmgr`评估的语句。

In the above, the macro `BI_MATCH_IF` is a condition that evaluates to `true` if the device has `BIND_PROTOCOL` equal to `ZX_PROTOCOL_MISC_PARENT`.A `true` evaluation causes `devmgr` to then bind the driver, using the binding opsprovided in the `ZIRCON_DRIVER_BEGIN` macro. 在上面的代码中，如果设备的BIND_PROTOCOL等于ZX_PROTOCOL_MISC_PARENT的宏，则BI_MATCH_IF的条件为true的评估。在`ZIRCON_DRIVER_BEGIN`宏中。

We can ignore this "glue" for now, and just note that this part of the code:  现在我们可以忽略此“胶水”，只需注意以下部分代码即可：

 
*   tells `devmgr` that this driver can be bound to devices requiring the `ZX_PROTOCOL_MISC_PARENT` protocol, and *告诉`devmgr`该驱动程序可以绑定到需要`ZX_PROTOCOL_MISC_PARENT`协议的设备上，并且
*   contains a pointer to the `zx_drivers_ops_t` table that lists the functions provided by this DSO. *包含指向zz_drivers_ops_t表的指针，该表列出了此DSO提供的功能。

To initialize the device, `devmgr` calls the binding function **null_bind()** through the `.bind` member (also in `demo-null.c`): 为了初始化设备，`devmgr`通过`.bind`成员（同样在`demo-null.c`中）调用绑定函数** null_bind（）**：

```c
static zx_protocol_device_t null_device_ops = {
    .version = DEVICE_OPS_VERSION,
    .read = null_read,
    .write = null_write,
};

zx_status_t null_bind(void* ctx, zx_device_t* parent) {
    device_add_args_t args = {
        .version = DEVICE_ADD_ARGS_VERSION,
        .name = "demo-null",
        .ops = &null_device_ops,
    };

    return device_add(parent, &args, NULL);
}
```
 

The binding function is responsible for "publishing" the device by calling **device_add()** witha pointer to the parent device, and an arguments structure. 绑定函数负责通过调用** device_add（）**以及指向父设备的指针和参数结构来“发布”设备。

The new device is bound relative to the parent's pathname &mdash; notice how we pass just `"demo-null"` in the `.name` member above. 新设备是相对于父设备的路径名绑定的。注意我们如何在上面的.name成员中仅传递“ demo-null”。

The `.ops` member is a pointer to a `zx_protocol_device_t` structure that lists the operations available for that device.We'll see these functions, **null_read()** and **null_write()**, below. .ops成员是指向zx_protocol_device_t结构的指针，该结构列出了该设备可用的操作。我们将在下面看到这些函数** null_read（）**和** null_write（）**。

After calling **device_add()**, the device name is registered, and the operations passed inthe `.ops` member of the argument structure are bound to the device.A successful return from **null_bind()** indicates to `devmgr` that the driver is nowassociated with the device. 在调用** device_add（）**之后，设备名称被注册，并且在参数结构的`.ops`成员中传递的操作被绑定到该设备。** null_bind（）**的成功返回表示`表示驱动程序已与设备关联。

At this point, our `/dev/misc/demo-null` device is ready to handle client requests, which means that it must: 至此，我们的`/ dev / misc / demo-null`设备已经准备好处理客户端请求，这意味着它必须：

 
*   support **open()** and **close()**  *支持** open（）**和** close（）**
*   provide a **read()** handler that returns end-of-file (**EOF**) immediately  *提供一个** read（）**处理程序，该处理程序立即返回文件结尾（** EOF **）
*   provide a **write()** handler that discards all data sent to it  *提供一个** write（）**处理程序，该处理程序将丢弃发送给它的所有数据

No other functionality is required.  不需要其他功能。

 
## Reading data from the device  从设备读取数据 

In the `zx_protocol_device_t` structure `null_device_ops`, we indicated that we support reading and writing via the functions **null_read()** and **null_write()** respectively. 在“ zx_protocol_device_t”结构“ null_device_ops”中，我们表示我们分别支持通过函数** null_read（）**和** null_write（）**进行读取和写入。

The **null_read()** function provides reading:  ** null_read（）**函数提供以下内容：

```c
static zx_status_t
null_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    *actual = 0;
    return ZX_OK;
}
```
 

and ends up being called in response to a client's call to **read()**.  并最终因响应客户对** read（）**的调用而被调用。

Notice that there are two size-related arguments passed to the handler:  请注意，有两个与大小相关的参数传递给处理程序：

Parameter   | Meaning ------------|--------------------------------------------------------`count`     | Maximum number of bytes that the client can accept`actual`    | Actual number of bytes sent to the client 参数含义------------ | ------------------------------------ --------------------`count` |客户端可以接受“实际”的最大字节数|发送给客户端的实际字节数

The following diagram illustrates the relationship:  下图说明了这种关系：

![Figure: Relationship between client's **read()** and `/dev/misc/demo-null`'s **null_read()**](simple-000-cropped.png) ！[图：客户端的** read（）**和`/ dev / misc / demo-null`的** null_read（）**之间的关系]（simple-000-cropped.png）

That is, the available size of the client's buffer (here, `sizeof(buf)`), is passed as the `count` parameter to **null_read()**.Similarly, when **null_read()** indicates the number of bytes that it read (0 in our case), thisappears as the return value from the client's **read()** function. 也就是说，客户端缓冲区的可用大小（此处为sizeof（buf））作为count参数传递给** null_read（）**。类似地，当** null_read（）**表示读取的字节数（在我们的例子中为0），它显示为客户端** read（）**函数的返回值。

 

Note: The handler is expected to always return immediately. By convention, indicating zero bytes in `*actual` indicates EOF 注意：处理程序应总是立即返回。按照惯例，在* actual中指示零字节表示EOF

There are, of course, cases when the device doesn't have data immediately available, *AND* it's not an EOF situation.For example, a serial port may be waiting for more characters to arrive from the remote end.This is handled by a special notification, which we'll see below, in the `/dev/misc/demo-fifo`device. 当然，在某些情况下设备无法立即获得数据，* AND *也不是EOF情况，例如，串行端口可能正在等待更多字符从远端到达。一个特殊的通知，我们将在/ dev / misc / demo-fifo设备中看到。

 
### Writing data to the device  将数据写入设备 

Writing data from the client to the device is almost identical, and is provided by **null_write()**: 从客户端向设备写入数据几乎是相同的，并且由** null_write（）**提供：

```c
static zx_status_t
null_write(void* ctx, const void* buf, size_t count, zx_off_t off, size_t* actual) {
    *actual = count;
    return ZX_OK;
}
```
 

As with the **read()**, the **null_write()** is triggered by the client's call to **write()**:  与** read（）**一样，** null_write（）**是由客户端调用** write（）**触发的：

![Figure: Relationship between client's **write()** and `/dev/misc/demo-null`'s **null_write()**](simple-001-cropped.png) ！[图：客户端的** write（）**和`/ dev / misc / demo-null`的** null_write（）**之间的关系]（simple-001-cropped.png）

The client specifies the number of bytes they wish to transfer in their **write()** function, and this appears as the `count` parameter in the device's **null_write()** function.It's possible that the device may be full (not in the case of our `/dev/misc/demo-null`, though&mdash; it never fills up), so the device needs to tell the client how many bytes it actuallywrote.This is done via the `actual` parameter, which shows up as the return value to the client's**write()** function. 客户端在** write（）**函数中指定要传输的字节数，这在设备的** null_write（）**函数中显示为`count`参数。已满（不是我们的`/ dev / misc / demo-null`，尽管它永远不会填满；所以它永远不会填满），所以设备需要告诉客户端它实际写了多少字节。这是通过`actual`参数完成的，显示为客户端** write（）**函数的返回值。

Note that our **null_write()** function includes the code:  请注意，我们的** null_write（）**函数包含以下代码：

```c
*actual = count;
```
 

This tells the client that all of their data was written. Of course, since this is the `/dev/misc/demo-null` device, the data doesn't actually *go*anywhere. 这告诉客户端他们的所有数据均已写入。当然，由于这是`/ dev / misc / demo-null`设备，因此数据实际上并没有“走”到任何地方。

Note: Just like in the **null_read()** case, the handler must not block.  注意：就像在** null_read（）**情况下一样，处理程序不得阻塞。

 
## What about **open()** and **close()**?  ** open（）**和** close（）**呢？ 

We didn't provide an **open()** nor **close()** handler, and yet our device supports those operations. 我们没有提供** open（）**或** close（）**处理程序，但您的设备支持这些操作。

This is possible because any operation hooks that are not provided take on defaults. Most of the defaults simply return "not supported," but in the case of **open()** and **close()**the defaults provide adequate support for simple devices. 这是可能的，因为未提供的任何操作挂钩都采用默认值。大多数默认值仅返回“不支持”，但是对于** open（）**和** close（）**而言，默认值为简单设备提供了足够的支持。

 
## `/dev/misc/demo-zero`  `/ dev / misc / demo-zero` 

As you might imagine, the source code for the `/dev/misc/demo-zero` device is almost identical to that for `/dev/misc/demo-null`.From an operational point of view, `/dev/misc/demo-zero` is supposed to return an endless streamof zeros &mdash; for as long as the client cares to read.We don't support writing. 就像您想象的那样，`/ dev / misc / demo-zero`设备的源代码几乎与`/ dev / misc / demo-null`相同。从操作的角度来看，`/ dev / misc / demo-zero`应该返回无穷无尽的零流mdash;只要客户关心阅读，我们就不支持写作。

Consider `/dev/misc/demo-zero`'s **zero_read()** function:  考虑`/ dev / misc / demo-zero`的** zero_read（）**函数：

```c
static zx_status_t
zero_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    memset(buf, 0, count);
    *actual = count;
    return ZX_OK;
}
```
 

The code sets the entire buffer `buf` to zero (the length is given by the client in the `count` argument),and tells the client that that many bytes are available (by setting `*actual` to the same numberas the client request). 该代码将整个缓冲区“ buf”设置为零（长度由客户端在“ count”参数中给出），并告诉客户端有许多字节可用（通过将“ * actual”设置为与客户端相同的数字）请求）。

 
## `/dev/misc/demo-number`  `/ dev / misc / demo-number` 

Let's build a more complicated device, based on the concepts we learned above. We'll call it `/dev/misc/demo-number`, and its job is to return an ASCII string representingthe next number in sequence.For example, the following might be a typical command-line session using the device: 基于上面学到的概念，让我们构建一个更复杂的设备。我们将其称为`/ dev / misc / demo-number`，其工作是返回代表下一个数字的ASCII字符串，例如，以下可能是使用该设备的典型命令行会话：

```shell
$ cat /dev/misc/demo-number
0
$ cat /dev/misc/demo-number
1
$ cat /dev/misc/demo-number
2
```
 

And so on.  等等。

Whereas `/dev/misc/demo-null` returned EOF immediately, and `/dev/misc/demo-zero` returned a never-ending stream of zeros, `/dev/misc/demo-number` is kind of in the middle: it needsto return a short data sequence, and *then* return EOF. / dev / misc / demo-null立即返回EOF，而/ dev / misc / demo-zero返回永无休止的零流，而/ dev / misc / demo-number是其中的一种。中间：它需要返回一个简短的数据序列，然后“ *”返回EOF。

In the real world, the client could read one byte at a time, or it could ask for a large buffer's worth of data.For our initial version, we're going to assume that the client asks for a buffer that's "bigenough" to get all the data at once. 在现实世界中，客户端一次可以读取一个字节，或者可以要求一个大缓冲区的数据。对于我们的初始版本，我们将假设客户端要求一个“双字节”的缓冲区来一次获取所有数据。

This means that we can take a shortcut. There's an offset parameter (`zx_off_t off`) that's passed as the 4th parameter to the **read()**handler function: 这意味着我们可以采取捷径。有一个偏移量参数（`zx_off_t off`）作为第四个参数传递给** read（）**处理函数：

```c
static zx_status_t
number_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual)
```
 

This indicates where the client would like to begin (or continue) reading from. The simplification that we're making here is that if the client has an offset of zero, it meansthat it's starting from the beginning, so we return as much data as the client can handle.However, if the offset isn't zero, we return `EOF`. 这表明客户端要从哪里开始（或继续）阅读。我们在这里所做的简化是，如果客户端的偏移量为零，则意味着它是从头开始的，因此我们返回的数据量是客户端可以处理的，但是如果偏移量不为零，则我们将返回返回`EOF`。

Let's discuss the code (note that we're initially presenting a slightly simpler version than what's in the source directory): 让我们讨论一下代码（请注意，我们最初提供的版本比源目录中的版本要简单一些）：

```c
static int global_counter;      // good and bad, see below

static zx_status_t
number_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    // (1) why are we here?
    if (off == 0) {
        // (2) first read; return as much data as we can
        int n = atomic_add(&global_counter);
        char tmp[22];           // 2^64 is 20 digits + \n + nul = 22 bytes
        *actual = snprintf(tmp, sizeof(tmp), "%d\n", n);
        if (*actual > count) {
            *actual = count;
        }
        memcpy(buf, tmp, *actual);
    } else {
        // (3) not the first time -- return EOF
        *actual = 0;
    }
    return ZX_OK;
}
```
 

The first decision we make is in step (1), where we determine if the client is reading the string for the first time, or not.If the offset is zero, it's the first time.In that case, in step (2), we grab a value from `global_counter`, put it into a string,and tell the client that we're returning some number of bytes.The number of bytes we return is limited to the smaller of: 我们的第一个决定是在步骤（1）中，我们确定客户端是否是第一次读取字符串，如果偏移量为零，则是第一次，在这种情况下，在步骤（2） ，我们从global_counter中获取一个值，并将其放入字符串中，然后告诉客户端我们要返回一定数量的字节。我们返回的字节数被限制为以下较小者：

 
*   the size of the client's buffer (given by `count`), or  *客户缓冲区的大小（由`count`给出），或
*   the size of the generated string (returned from **snprintf()**).  *生成的字符串的大小（从snprintf（）返回）。

If the offset is not zero, however, it means that it's not the first time that the client is reading data from this device.In this case, in step (3) we simply set the number of bytes that we're returning (the valueof `*actual`) to zero, and this has the effect of indicating `EOF` to the client (just likeit did in the `null` driver, above). 但是，如果偏移量不为零，则意味着这不是客户端第一次从该设备读取数据。在这种情况下，在步骤（3）中，我们只需设置要返回的字节数即可（ * actual的值）为零，这会向客户端指示“ EOF”（就像上面的“ null”驱动程序中所做的一样）。

 
### Globals are bad  全球人不好 

The `global_counter` that we used was global to the driver. This means that each and every session that ends up calling **number_read()** will end upincrementing that number. 我们使用的`global_counter`对驱动程序是全局的。这意味着每个结束调用** number_read（）**的会话都将最终增加该数字。

This is expected &mdash; after all, `/dev/misc/demo-number`'s job is to "hand out increasing numbers to its clients." 这是预期的-毕竟，“ / dev / misc / demo-number”的工作是“向其客户分发越来越多的数字”。

What may not be expected is that if the driver is instantiated multiple times (as might happen with real hardware drivers, for example), then the value is *shared* across those multipleinstances.Generally, this isn't what you want for real hardware drivers (because each driver instanceis independent). 可能无法预料的是，如果驱动程序被多次实例化（例如在实际的硬件驱动程序中可能发生的情况），则该值在多个实例之间是* shared *。通常，这不是真正的硬件所需的值驱动程序（因为每个驱动程序实例都是独立的）。

The solution is to create a "per-device" context block; this context block would contain data that's unique for each device. 解决方案是创建一个“每设备”上下文块。该上下文块将包含每个设备唯一的数据。

In order to create per-device context blocks, we need to adjust our binding routine. Recall that the binding routine is where the association is made between the device andits protocol ops.If we were to create our context block in the binding routine, we'd then be able touse it later on in our read handler: 为了创建每个设备的上下文块，我们需要调整绑定例程。回想一下绑定例程是在设备与其协议操作之间建立关联的地方，如果我们要在绑定例程中创建上下文块，则可以稍后在读取处理程序中使用它：

 

```c
typedef struct {
    zx_device_t*    zxdev;
    uint64_t        counter;
} number_device_t;

zx_status_t
number_bind(void* ctx, zx_device_t* parent) {
    // allocate & initialize per-device context block
    number_device_t* device = calloc(1, sizeof(*device));
    if (!device) {
        return ZX_ERR_NO_MEMORY;
    }

    device_add_args_t args = {
        .version = DEVICE_ADD_ARGS_VERSION,
        .name = "demo-number",
        .ops = &number_device_ops,
        .ctx = device,
    };

    zx_status_t rc = device_add(parent, &args, &device->zxdev);
    if (rc != ZX_OK) {
        free(device);
    }
    return rc;
}
```
 

Here we've allocated a context block and stored it in the `ctx` member of the `device_add_args_t` structure `args` that we passed to **device_add()**.A unique instance of the context block, created at binding time, is now associated with eachbound device instance, and is available for use in all protocol functions bound by**number_bind()**.Note that while we don't use the `zxdev` device from the context block, it's good practiceto hang on to it in case we need it for any other device related operations later. 这里我们分配了一个上下文块并将其存储在我们传递给** device_add（）**的device_add_args_t结构args的`ctx`成员中。上下文块的唯一实例是在绑定时创建的，现在与每个绑定的设备实例相关联，并且可用于由number_bind（）**绑定的所有协议功能。请注意，尽管我们不使用上下文块中的`zxdev`设备，但挂起是一种很好的做法以备不时之需，以便以后进行其他任何与设备相关的操作。

![Figure: **device_add()** binds context blocks to devices](simple-003-cropped.png) ！[图：** device_add（）**将上下文块绑定到设备]（simple-003-cropped.png）

The context block can be used in all protocol functions defined by `number_device_ops`, like our **number_read()** function: 上下文块可以在所有由number_device_ops定义的协议函数中使用，例如我们的** number_read（）**函数：

```c
static zx_status_t
number_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    if (off == 0) {
        number_device_t* device = ctx;
        int n = atomic_fetch_add(&device->counter, 1);

        //------------------------------------------------
        // everything else is the same as previous version
        //------------------------------------------------

        char tmp[22];   // 2^64 is 20 digits + \n + \0
        *actual = snprintf(tmp, sizeof(tmp), "%d\n", n);
        if (*actual > count) {
            *actual = count;
        }
        memcpy(buf, tmp, *actual);
    } else {
        *actual = 0;
    }
    return ZX_OK;
}
```
 

Notice how we replaced the original version's `global_counter` with the value from the context block.Using the context block, each device gets its own, independent counter. 注意我们如何用上下文块中的值替换原始版本的`global_counter`。使用上下文块，每个设备都有自己的独立计数器。

 
### Cleaning up the context  清理上下文 

Of course, every time we **calloc()** something, we're going to have to **free()** it somewhere. This is done in our **number_release()** handler, which we store in our `zx_protocol_device_tnumber_device_ops` structure: 当然，每次我们使用calloc（）进行某些操作时，都将不得不在某处进行free（）进行处理。这是在我们的** number_release（）**处理程序中完成的，该处理程序存储在我们的`zx_protocol_device_tnumber_device_ops`结构中：

```c
static zx_protocol_device_t
number_device_ops = {
    // other initializations ...
    .release = number_release,
};
```
 

The **number_release()** function is simply:  number_release（）函数很简单：

```c
static void
number_release(void* ctx) {
    free(ctx);
}
```
 

The **number_release()** function is called before the driver is unloaded.  在卸载驱动程序之前，将调用number_release（）函数。

 
### Controlling your device  控制您的设备 

Sometimes, it's desirable to send a control message to your device. This is data that doesn't travel over the **read()** / **write()** interface.For example, in `/dev/misc/demo-number`, we might want a way to preset the count to a given number. 有时，最好将控制消息发送到您的设备。这是无法通过** read（）** / ** write（）**接口传输的数据。例如，在`/ dev / misc / demo-number`中，我们可能需要一种方法来预置计数到给定的数字。

In a tradition POSIX environment, this is done with an **ioctl()** call on the client side, and an appropriate **ioctl()** handler on the driver side. 在传统的POSIX环境中，这是通过在客户端调用** ioctl（）**和在驱动程序一侧使用适当的** ioctl（）**处理程序来完成的。

Under Fuchsia, this is done differently, by marshalling data through the Fuchsia Interface Definition Language([**FIDL**](/docs/development/languages/fidl/README.md)). 在紫红色下，通过紫红色接口定义语言（[** FIDL **]（/ docs / development / languages / fidl / README.md））整理数据来完成此操作的方式有所不同。

For more details about FIDL itself, consult the reference above. For our purposes here, FIDL: 有关FIDL本身的更多详细信息，请参考上面的参考。对于我们这里的目的，FIDL：

 
*   is described by a C-like language,  *用类C语言描述，
*   is used to define the input and output arguments for your control functions,  *用于定义控制功能的输入和输出参数，
*   generates code for the client and driver side.  *为客户端和驱动程序端生成代码。

> If you're already familiar with Google's "Protocol Buffers" then you'll be very comfortable > with FIDL. >如果您已经熟悉Google的“协议缓冲区”，那么您将对FIDL非常满意。

There are multiple advantages to FIDL. Because the input and output arguments are well-defined, the result isgenerated code that has strict type safety and checking, on both the client and driversides.By abstracting the definition of the messages from their implementation, the FIDLcode generator can generate code for multiple different languages, without additionalwork on your part.This is especially useful, for example, when clients require APIsin languages with which you aren't necessarily familiar. FIDL有多个优点。由于输入和输出参数定义明确，因此生成的代码在客户端和驱动程序端均具有严格的类型安全性和检查功能。通过从消息实现中抽象出消息的定义，FIDLcode生成器可以为多种不同的代码生成代码语言，而无需您做额外的工作。例如，当客户端需要您不一定熟悉的语言的API时，这特别有用。

 
#### Using FIDL  使用FIDL 

In the majority of cases, you'll be using FIDL APIs already provided by the device, and will rarely need to create your own.However, it's a good idea to understand the mechanism, end-to-end. 在大多数情况下，您将使用设备已经提供的FIDL API，并且很少需要创建自己的API。但是，了解端到端的机制是一个好主意。

Using FIDL for your device control is simple:  使用FIDL进行设备控制很简单：

 
*   define your inputs, outputs, and protocols in a "`.fidl`" file,  *在“ .fidl”文件中定义您的输入，输出和协议，
*   compile the FIDL code and generate your client functions, and  *编译FIDL代码并生成您的客户端函数，以及
*   add message handlers to your driver to receive control messages.  *将消息处理程序添加到您的驱动程序以接收控制消息。

We'll look at these steps by implementing the "preset counter to value" control function for our `/dev/misc/demo-number` driver. 我们将通过为我们的`/ dev / misc / demo-number`驱动程序实现“预设值计数器”控制功能来查看这些步骤。

 
#### Define the FIDL protocol  定义FIDL协议 

The first thing we need to do is define what the protocol looks like. Since all we want to do is preset the count to a user-specified value,our protocol will be very simple. 我们需要做的第一件事是定义协议的外观。由于我们要做的只是将计数预设为用户指定的值，因此我们的协议将非常简单。

This is what the "`.fidl`" file looks like:  这就是“ .fidl`”文件的样子：

```fidl
library zircon.sample.number;

[Layout="Simple"]
protocol Number {

    // set the number to a given value
    SetNumber(uint32 value) -> (uint32 previous);
};
```
 

The first line, `library zircon.sample.number;` provides a name for the library that will be generated. 第一行“ library zircon.sample.number;”提供了将要生成的库的名称。

Next, `[Layout="Simple"]` generates [simple C bindings](/docs/development/languages/fidl/tutorial/tutorial-c.md#simple-bindings).  接下来，`[Layout =“ Simple”]`生成[简单C绑定]（/ docs / development / languages / fidl / tutorial / tutorial-c.mdsimple-bindings）。

Finally, the `protocol` section defines all of the methods that are available. Each method has a name, and specifies inputs and outputs. 最后，“协议”部分定义了所有可用的方法。每个方法都有一个名称，并指定输入和输出。

Here, we have one method function, called **SetNumber()**, which takes a `uint32` (which is the FIDL equivalent of the C standard integer `uint32_t` type) as input, and returns a `uint32`as the result (the previous value of the counter before it was changed). 在这里，我们有一个方法函数，叫做** SetNumber（）**，它以一个uint32（与C标准整数uint32_t类型的FIDL等效）作为输入，并以uint32作为返回值。结果（更改前计数器的先前值）。

We'll see more advanced examples below.  我们将在下面看到更多高级示例。

 
#### Compile the FIDL code  编译FIDL代码 

The FIDL code is compiled automatically by the build system; you just need to add a dependency into the `BUILD.` file.This is what a stand-alone `rules.mk` would look like, assuming the "`.fidl`" file is called`demo_number.fidl`: FIDL代码由构建系统自动编译；您只需要在`BUILD.`文件中添加一个依赖项。这就是独立的`rules.mk`的样子，假设“ .fidl”文件被称为`demo_number.fidl`：

```gn
import("$zx/public/gn/fidl.gni")

// Defined in $zx/system/fidl/fuchsia-io/BUILD.gn
fidl_library("zircon.sample.number") {
  sources = [
    "demo_number.fidl",
  ]
}
```
 

Once compiled, the interface files will show up in the build output directory. The exact path depends on the build target (e.g., ...`/zircon/build-x64/`... for x8664-bit builds), and the source directory containing the FIDL files. 编译后，接口文件将显示在构建输出目录中。确切的路径取决于构建目标（例如，对于x8664位构建，为...`/ zircon / build-x64 /`...），以及包含FIDL文件的源目录。

For this example, we'll use the following paths:  对于此示例，我们将使用以下路径：

 
* ...`/zircon/system/dev/sample/number/demo-number.c`  * ...`/ zircon / system / dev / sample / number / demo-number.c`
	* source file for `/dev/misc/demo-number` driver  *`/ dev / misc / demo-number`驱动程序的源文件
* ...`/zircon/system/fidl/zircon-sample/demo_number.fidl`  * ...`/ zircon / system / fidl / zircon-sample / demo_number.fidl`
	* source file for FIDL protocol definition  * FIDL协议定义的源文件
* ...`/zircon/build-x64/system/fidl/zircon-sample/gen/include/zircon/sample/number/c/fidl.h`  * ...`/ zircon / build-x64 / system / fidl / zircon-sample / gen / include / zircon / sample / number / c / fidl.h`
	* generated interface definition header include file  *生成的接口定义头包含文件

It's instructive to see the interface definition header file that was generated by the FIDL compiler.Here it is, annotated and edited slightly to just show the highlights: 查看由FIDL编译器生成的接口定义头文件很有启发性，在这里对其进行了注释和稍微编辑以仅显示突出显示的内容：

```c
// (1) Forward declarations
#define zircon_sample_number_NumberSetNumberOrdinal ((uint32_t)0x1)

// (2) Extern declarations
extern const fidl_type_t zircon_sample_number_NumberSetNumberRequestTable;
extern const fidl_type_t zircon_sample_number_NumberSetNumberResponseTable;

// (3) Declarations
struct zircon_sample_number_NumberSetNumberRequest {
    fidl_message_header_t hdr;
    uint32_t value;
};

struct zircon_sample_number_NumberSetNumberResponse {
    fidl_message_header_t hdr;
    uint32_t result;
};

// (4) client binding prototype
zx_status_t
zircon_sample_number_NumberSetNumber(zx_handle_t _channel,
                                     uint32_t value,
                                     uint32_t* out_result);

// (5) FIDL message ops structure
typedef struct zircon_sample_number_Number_ops {
    zx_status_t (*SetNumber)(void* ctx, uint32_t value, fidl_txn_t* txn);
} zircon_sample_number_Number_ops_t;

// (6) dispatch prototypes
zx_status_t
zircon_sample_number_Number_dispatch(void* ctx, fidl_txn_t* txn, fidl_msg_t* msg,
                                     const zircon_sample_number_Number_ops_t* ops);

zx_status_t
zircon_sample_number_Number_try_dispatch(void* ctx, fidl_txn_t* txn, fidl_msg_t* msg,
                                         const zircon_sample_number_Number_ops_t* ops);

// (7) reply prototype
zx_status_t
zircon_sample_number_NumberSetNumber_reply(fidl_txn_t* _txn, uint32_t result);
```
 

> Note that this generated file contains code relevant to both the client *and* the driver.  >请注意，此生成的文件包含与客户端*和*驱动程序相关的代码。

Briefly, the generated code presents:  简要地说，生成的代码显示：

 
1.  a definition for the command numbers (the "`NumberOrdinal`", recall we used command number `1` for **SetNumber()**), 1.命令编号的定义（“`NumberOrdinal`”，回想一下我们为** SetNumber（）**使用的命令编号为“ 1”），
2.  external definitions of tables (we don't use these),  2.表格的外部定义（我们不使用它们），
3.  declarations for the request and response message formats; these consist of a FIDL overhead header and the data we specified, 3.请求和响应消息格式的声明；这些由FIDL开销标头和我们指定的数据组成，
4.  client binding prototypes &mdash; we'll see how the client uses this below,  4.客户端绑定原型-我们将在下面看到客户如何使用它，
5.  FIDL message ops structure; this is a list of functions that you supply in the driver to handle each and every FIDL method defined by all the protocols in the "`.fidl`" file, 5. FIDL消息操作结构；这是驱动程序中提供的函数列表，用于处理“ .fidl”文件中所有协议定义的每个FIDL方法，
6.  dispatch prototypes &mdash; this is called by our FIDL message handler,  6.派发原型-这由我们的FIDL消息处理程序调用，
7.  reply prototype &mdash; we call this in our driver when we want to reply to the client.  7.回复原型mdash；当我们想回复客户时，我们会在驱动程序中称呼它。

 
#### The client side  客户端 

Let's start with a tiny, command-line based client, called `set_number`, that uses the above FIDL protocol.It assumes that the device we're controlling is called `/dev/misc/demo-number`.The program takes exactly one argument &mdash; the number to set the current counter to. 让我们从一个基于命令行的小型客户端set_number开始，该客户端使用上述FIDL协议，假设我们控制的设备名为`/ dev / misc / demo-number`。一个论点-设置当前计数器的编号。

Here's a sample of the program's operation:  这是程序操作的示例：

```bash
$ cat /dev/misc/demo-number
0
$ cat /dev/misc/demo-number
1
$ cat /dev/misc/demo-number
2
$ set_number 77
Original value was 3
$ cat /dev/misc/demo-number
77
$ cat /dev/misc/demo-number
78
```
 

The complete program is as follows:  完整的程序如下：

```c
#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#include <zircon/syscalls.h>
#include <lib/fdio/fdio.h>

// (1) include the generated definition file
#include <zircon/sample/number/c/fidl.h>

int main(int argc, const char** argv)
{
    static const char* dev = "/dev/misc/demo-number";

    // (2) get number from command line
    if (argc != 2) {
        fprintf(stderr, "set_number:  needs exactly one numeric argument,"
                " the value to set %s to\n", dev);
        exit(EXIT_FAILURE);
    }
    uint32_t n = atoi(argv[1]);

    // (3) establish file descriptor to device
    int fd = open(dev, O_RDWR);
    if (fd == -1) {
        fprintf(stderr, "set_number: can't open %s for O_RDWR, errno %d (%s)\n",
                dev, errno, strerror(errno));
        exit(EXIT_FAILURE);
    }

    // (4) establish handle to FDIO service on device
    zx_handle_t num;
    zx_status_t rc;
    if ((rc = fdio_get_service_handle(fd, &num)) != ZX_OK) {
        fprintf(stderr, "set_number: can't get fdio service handle, error %d\n", rc);
        exit(EXIT_FAILURE);
    }

    // (5) send FDIO command, get response
    uint32_t orig;
    if ((rc = zircon_sample_number_NumberSetNumber(num, n, &orig)) != ZX_OK) {
        fprintf(stderr, "set_number: can't execute FIDL command to set number, error %d\n", rc);
        exit(EXIT_FAILURE);
    }
    printf("Original value was %d\n", orig);
    exit(EXIT_SUCCESS);
}
```
 

This is very similar to the approach taken with POSIX **ioctl()**, except that:  这与POSIX ** ioctl（）**所采用的方法非常相似，除了：

 
*   we established a handle to the FDIO service (step 4), and  *我们建立了FDIO服务的句柄（步骤4），并且
*   the API is type-safe and prototyped for the specific operation (step 5).  * API是类型安全的，并且针对特定操作进行了原型设计（步骤5）。

Notice the FDIO command has a very long name: **zircon_sample_number_NumberSetNumber()** (which includes a lot of repetition).This is a facet of the code generation process from the FIDL compiler &mdash; the"`zircon_sample_number`" part came from the "`library zircon.sample.number`"statement, the first "`Number`" came from the "`protocol Number`" statement, and the final"`SetNumber`" is the name of the method from the protocol definition statement. 注意FDIO命令有一个很长的名字：** zircon_sample_number_NumberSetNumber（）**（包括很多重复）。这是FIDL编译器mdash的代码生成过程的一个方面。 “`zircon_sample_number`”部分来自“`library zircon.sample.number`”语句，第一个“`Number`”来自“`Protocol Number`”语句，最后一个“`SetNumber`”是协议定义语句中方法的名称。

 
#### Add a message handler to the driver  向驱动程序添加消息处理程序 

On the driver side, we need to:  在驱动程序方面，我们需要：

 
*   handle the FIDL message  *处理FIDL消息
*   demultiplex the message (figure out which control message it is)  *对消息进行多路分解（确定是哪个控制消息）
*   generate a reply  *产生回复

In conjunction with the prototype above, to handle the FIDL control message in our driver we need to bind a message handling function (just like we did in orderto handle **read()**, for example): 结合上面的原型，要在驱动程序中处理FIDL控制消息，我们需要绑定消息处理函数（例如，为了处理** read（）**，我们就这样做了）：

```c
static zx_protocol_device_t number_device_ops = {
    .version = DEVICE_OPS_VERSION,
    .read = number_read,
    .release = number_release,
    .message = number_message,  // handle FIDL messages
};
```
 

The **number_message()** function is trivial in this case; it simply wraps the dispatch function: 在这种情况下，** number_message（）**函数是微不足道的；它只是包装了dispatch函数：

```c
static zircon_sample_number_Number_ops_t number_fidl_ops = {
    .SetNumber = fidl_SetNumber,
};

static zx_status_t number_message(void* ctx, fidl_msg_t* msg, fidl_txn_t* txn) {
    zx_status_t status = zircon_sample_number_Number_dispatch(ctx, txn, msg, &number_fidl_ops);
    return status;
}
```
 

The generated **zircon_sample_number_Number_dispatch()** function takes the incoming message and calls the appropriate handling function based on the provided table of functions in`number_fidl_ops`.Of course, in our trivial example, there is only the one function, `SetNumber`: 生成的** zircon_sample_number_Number_dispatch（）**函数接收传入的消息并根据number_fidl_ops中提供的函数表调用适当的处理函数。当然，在我们平凡的示例中，只有一个函数SetNumber。 ：

```c
static zx_status_t fidl_SetNumber(void* ctx, uint32_t value, fidl_txn_t* txn)
{
    number_device_t* device = ctx;
    int saved = device->counter;
    device->counter = value;
    return zircon_sample_number_NumberSetNumber_reply (txn, saved);
}
```
 

The **fidl_SetNumber()** handler:  ** fidl_SetNumber（）**处理程序：

 
*   establishes a pointer to the device context,  *建立指向设备上下文的指针，
*   saves the current count value (so that it can return it later),  *保存当前计数值（以便以后可以返回），
*   sets the new value into the device context, and  *将新值设置为设备上下文，并且
*   calls the "reply" function to return the value to the client.  *调用“答复”功能以将值返回给客户端。

Notice that the **fidl_SetNumber()** function has a prototype that matches the FIDL specification, ensuring type safety. Similarly, the reply function,**zircon_sample_number_NumberSetNumber_reply()** also conforms to the FIDLspecification's prototype of the result portion of the method definition. 请注意，** fidl_SetNumber（）**函数具有与FIDL规范匹配的原型，从而确保类型安全。同样，回复函数** zircon_sample_number_NumberSetNumber_reply（）**也符合方法定义的结果部分的FIDLspecification原型。

 
#### Advanced uses  高级用途 

FIDL expressions can certainly be made more complex than what we've shown above. For example, nested structures can be used, rather than the simple `uint32`.Multiple parameters are allowed for both inputs and outputs. See the[FIDL reference](/docs/development/languages/fidl/README.md). FIDL表达式当然可以比我们上面显示的复杂。例如，可以使用嵌套结构，而不是简单的uint32。输入和输出都可以使用多个参数。请参阅[FIDL参考]（/ docs / development / languages / fidl / README.md）。

 
## Registering multiple devices with `/dev/misc/demo-multi`  用`/ dev / misc / demo-multi`注册多个设备 

So far, the devices discussed were "singletons" &mdash; that is, one registered name did one thing (`null` manifested the null device, `number` manifested the number device, and so on). 到目前为止，讨论的设备是“单个”设备。也就是说，一个注册名称做了一件事情（“ null”表示空设备，“ number”表示数字设备，依此类推）。

What if you have a cluster of devices that all perform similar functions? For example, you might have a multi-channel controller of some kind that has 16 channels. 如果您有一簇都执行相似功能的设备怎么办？例如，您可能有一个具有16个通道的某种多通道控制器。

The correct way to handle this is to:  解决此问题的正确方法是：

 
1.  create a driver instance,  1.创建一个驱动程序实例，
2.  create a base device node, and  2.创建一个基本设备节点，并
3.  manifest your sub-devices under that base device.  3.在该基本设备下显示您的子设备。

Creating the driver instance is good practice as discussed above, in "Globals are bad" (we'll discuss it a little more in this particular context later). 如上所述，创建驱动程序实例是一种好习惯，在“全局性很差”中（我们稍后将在此特定上下文中对其进行一些讨论）。

In this example, we're going to create a base device `/dev/misc/demo-multi`, and then we're going to create 16 sub-devices under that called `0` through `15` (e.g.,`/dev/misc/demo-multi/7`). 在此示例中，我们将创建一个基本设备“ / dev / misc / demo-multi”，然后在“ 0”至“ 15”（例如，“ / dev / misc / demo-multi / 7`）。

```c
static zx_protocol_device_t multi_device_ops = {
    .version = DEVICE_OPS_VERSION,
    .read = multi_read,
    .release = multi_release,
};

static zx_protocol_device_t multi_base_device_ops = {
    .version = DEVICE_OPS_VERSION,
    .read = multi_base_read,
    .release = multi_release,
};

zx_status_t multi_bind(void* ctx, zx_device_t* parent) {
    // (1) allocate & initialize per-device context block
    multi_root_device_t* device = calloc(1, sizeof(*device));
    if (!device) {
        return ZX_ERR_NO_MEMORY;
    }
    device->parent = parent;

    // (2) set up base device args structure
    device_add_args_t args = {
        .version = DEVICE_ADD_ARGS_VERSION,
        .ops = &multi_base_device_ops,          // use base ops initially
        .name = "demo-multi",
        .ctx = device,
    };

    // (3) bind base device
    zx_status_t rc = device_add(parent, &args, &device->base_device.zxdev);
    if (rc != ZX_OK) {
        return rc;
    }

    // (4) allocate and bind sub-devices
    args.ops = &multi_device_ops;               // switch to sub-device ops
    for (int i = 0; i < NDEVICES; i++) {
        char name[ZX_DEVICE_NAME_MAX + 1];
        sprintf(name, "%d", i);
        args.name = name;                       // change name for each sub-device
        device->devices[i] = calloc(1, sizeof(*device->devices[i]));
        if (device->devices[i]) {
            args.ctx = &device->devices[i];     // store device pointer in context
            device->devices[i]->devno = i;      // store number as part of context
            rc = device_add(device->base_device.zxdev, &args, &device->devices[i]->zxdev);
            if (rc != ZX_OK) {
                free(device->devices[i]);       // device "i" failed; free its memory
            }
        } else {
            rc = ZX_ERR_NO_MEMORY;
        }

        // (5) failure backout, schedule the removal of the base device and its children
        // sub-devices.
        if (rc != ZX_OK) {
            device_async_remove(device->base_device.zxdev);
            return rc;
        }
    }

    return rc;
}

// (6) release the per-device context block
static void multi_release(void* ctx) {
    free(ctx);
}
```
 

The steps are:  这些步骤是：

 
1.  Establish a device context pointer, in case this driver is loaded multiple times.  1.建立设备上下文指针，以防多次加载该驱动程序。
2.  Create and initialize an `args` structure that we'll pass to **device_add()**.This structure has the base device name, "`demo-multi`", and a context pointerto the multi root device `device`. 2.创建并初始化将传递给** device_add（）**的args结构。该结构具有基本设备名称“ demo-multi”和指向多根设备设备的上下文指针。 `。
3.  Call **device_add()** to add the base device. This has now created `/dev/misc/demo-multi`.Note that we store the newly created device into `base_device.zxdev`. This thenserves as the "parent" device for the sub-device children. 3.调用** device_add（）**以添加基本设备。现在已经创建了`/ dev / misc / demo-multi`。注意，我们将新创建的设备存储在`base_device.zxdev`中。然后，这充当子设备子代的“父”设备。
4.  Now create 16 sub-devices as children of the base ("parent") device. Notice that we changed the `ops` member to point to the sub-device protocol ops`multi_device_ops` instead of the base version.The name of each sub-device is simply the ASCII representation of the device number.Note that we store the device number index `i` (0 .. 15) in `devno` as context(we have an array of contexts called `multi_devices` which we'll see shortly).We also illustrate allocating each sub-device dynamically, rather thanallocating its space in the parent's structure.This is a more realistic use-case for "hot-plug" devices &mdash; you don'twant to allocate a large context structure, or perform initialization work,for devices that aren't (yet) present. 4.现在，创建16个子设备作为基本（“父”）设备的子设备。请注意，我们将ops成员更改为指向子设备协议ops`multi_device_ops而不是基本版本。每个子设备的名称只是设备编号的ASCII表示。请注意，我们存储设备在`devno`中以数字索引`i（0 .. 15）作为上下文（我们有一个称为`multi_devices`的上下文数组），我们还将说明动态分配每个子设备，而不是分配其空间在父母的结构中。这是“热插拔”设备的更实际的用例。您不想为尚不存在的设备分配大型上下文结构或执行初始化工作。
5.  In case of a failure, we need to remove and deallocate the devices that we already added, including the base device and the per-device context block.Note that we release up to, but not including, the failed device index.This is why we called **free()** on the sub-device structure in step 4 incase of **device_add()** failure. 5.如果发生故障，我们需要删除并重新分配已经添加的设备，包括基本设备和每设备上下文块。请注意，我们最多释放但不包括故障设备索引。这就是为什么在** device_add（）**失败的情况下，我们在步骤4中在子设备结构上调用** free（）**的原因。
6.  We release the per-device context block in our release handler. Since the base device and 16 sub-devices do not implement unbind hooks,**device_async_remove()** will invoke the release hooks of the sub-devices,followed by the base device. 6.我们在发布处理程序中释放每个设备的上下文块。由于基本设备和16个子设备未实现未绑定挂钩，** device_async_remove（）**将调用子设备的释放挂钩，随后是基本设备。

 
### Which device is which?  哪个设备？ 

We have two **read()** functions, **multi_read()** and **multi_base_read()**. This allows us to have different behaviors for reading the base device versusreading one of the 16 sub-devices. 我们有两个** read（）**函数，** multi_read（）**和** multi_base_read（）**。这使我们在读取基本设备和读取16个子设备之一方面具有不同的行为。

The base device read is almost identical to what we saw above in `/dev/misc/demo-number`:  基本设备读取的内容几乎与上面在/ dev / misc / demo-number中看到的内容相同：

```c
static zx_status_t
multi_base_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    const char* base_name = "base device\n";

    if (off == 0) {
        *actual = strlen(base_name);
        if (*actual > count) {
            *actual = count;
        }
        memcpy(buf, base_name, *actual);
    } else {
        *actual = 0;
    }
    return ZX_OK;
}
```
 

This just returns the string "`base device\n`" for the read, up to the maximum number of bytes allowed by the client, of course. 当然，这只是返回字符串“`base device \ n`”进行读取，当然不超过客户端允许的最大字节数。

But the read for the sub-devices needs to know which device it's being called on behalf of.We keep a device index, called `devno`, in the individual sub-device context block: 但是子设备的读取需要知道代表哪个设备被调用。我们在单个子设备上下文块中保留一个名为“ devno”的设备索引：

```c
typedef struct {
    zx_device_t*    zxdev;
    int             devno;              // device number (index)
} multidev_t;
```
 

The context blocks for the 16 sub-devices, as well as the base device, are stored in the per-device context block created in step (1) of the binding function, above. 16个子设备以及基本设备的上下文块存储在上面绑定功能的步骤（1）中创建的每个设备的上下文块中。

```c
// this contains our per-device instance
#define NDEVICES 16
typedef struct {
    zx_device_t*    parent;
    multidev_t*     devices[NDEVICES];  // pointers to our 16 sub-devices
    multidev_t      base_device;        // our base device
} multi_root_device_t;
```
 

Notice that the `multi_root_device_t` per-device context structure contains 1 `multidev_t` context block (for the base device) and 16 pointers to dynamically allocated contextblocks for the sub-devices.The initialization of those context blocks occurred in steps (3) (for the base device)and (4) (done in the `for` loop for each sub-device). 请注意，每个设备的`multi_root_device_t`上下文结构包含1个（对于基本设备）`multidev_t`上下文块和16个指向为子设备动态分配的上下文块的指针。这些上下文块的初始化发生在步骤（3）（ （4）（在每个子设备的“ for”循环中完成）。

![Figure: Relationship between per-device context and devices](simple-008-cropped.png)  ！[图：每个设备的上下文和设备之间的关系]（simple-008-cropped.png）

The diagram above illustrates the relationship between the per-device context block, and the individual devices.Sub-device 7 is representative of all sub-devices. 上图说明了每个设备上下文块与各个设备之间的关系。子设备7代表所有子设备。

This is what our **multi_read()** function looks like:  这就是我们的** multi_read（）**函数的样子：

```c
static const char* devnames[NDEVICES] = {
    "zero", "one", "two", "three",
    "four", "five", "six", "seven",
    "eight", "nine", "ten", "eleven",
    "twelve", "thirteen", "fourteen", "fifteen",
};

static zx_status_t
multi_read(void* ctx, void* buf, size_t count, zx_off_t off, size_t* actual) {
    multi_root_device_t* root_device = ctx;
    multidev_t* device = &root_device->base_device;

    if (off == 0) {
        char tmp[16];
        *actual = snprintf(tmp, sizeof(tmp), "%s\n", devnames[device->devno]);
        if (*actual > count) {
            *actual = count;
        }
        memcpy(buf, tmp, *actual);
    } else {
        *actual = 0;
    }
    return ZX_OK;
}
```
 

Exercising our device from the command line gives results like this:  从命令行执行设备可以得到如下结果：

```shell
$ cat /dev/misc/demo-multi
base device
$ cat /dev/misc/demo-multi/7
seven
$ cat /dev/misc/demo-multi/13
thirteen
```
 

and so on.  等等。

 
### Multiple multiple devices  多个设备 

It may seem odd to create a "per device" context block for a controller that supports multiple devices, but it's really no different than any other controller.If this were a real hardware device (say a 16 channel data acquisition system),you could certainly have two or more of these plugged into your system.Each driver would be given a unique base device name (e.g. `/dev/daq-0`,`/dev/daq-1`, and so on), and would then manifest its channels under that name(e.g., `/dev/daq-1/7` for the 8th channel on the 2nd data acquisition system). 为支持多个设备的控制器创建“每设备”上下文块似乎很奇怪，但实际上与其他任何控制器都没有什么不同。如果这是真正的硬件设备（例如16通道数据采集系统），则可以肯定有两个或多个插入到您的系统中。每个驱动程序将被赋予一个唯一的基本设备名称（例如`/ dev / daq-0`，`/ dev / daq-1等），然后以该名称显示其通道（例如，第二个数据采集系统上的第8个通道的“ / dev / daq-1 / 7”）。

Ideally, the assignment of unique base device names should be done based on some kind of hardware provided unique key.This has the advantage of repeatability / predictability, especially with hot-plugdevices.For example, in the data acquisition case, there would be distinct devices connectedto each of the controller channels.After a reboot, or a hot unplug / replug event, it would be desirable to be able toassociate each controller with a known base device name; it wouldn't be usefulto have the device name change randomly between plug / unplug events. 理想情况下，唯一的基本设备名称的分配应基于某种硬件提供的唯一密钥进行，这具有可重复性/可预测性的优势，尤其是对于热插拔设备而言，例如，在数据采集情况下，重新启动或热拔/插拔事件后，希望能够将每个控制器与已知的基本设备名称相关联；在插入/拔出事件之间随机更改设备名称并没有用。

 
## Blocking reads and writes: `/dev/misc/demo-fifo`  阻止读写：`/ dev / misc / demo-fifo` 

So far, all of the devices that we've examined returned data immediately (for a **read()** operation), or (in the case of `/dev/misc/demo-null`), accepted data without blocking(for the **write()** operation). 到目前为止，我们检查过的所有设备都立即返回了数据（用于read（）操作），或者（对于/ dev / misc / demo-null）返回了数据而没有阻塞（用于** write（）**操作）。

The next device we'll discuss, `/dev/misc/demo-fifo`, will return data immediately if there's data available, otherwise it will block the client until data is available.Similarly, for writing, it will accept data immediately if there's room, otherwiseit will block the client until room is available. 我们将讨论的下一个设备`/ dev / misc / demo-fifo`如果有可用数据将立即返回数据，否则将阻塞客户端直到有可用数据。类似地，对于写入，如果有可用数据，它将立即接受数据。有房间，否则它将阻止客户，直到有房间可用。

The individual handlers for reading and writing must return immediately (regardless of whether data or room is available or not).However, they don't have to return or accept *data* immediately; they can insteadindicate to the client that it should wait. 读写的各个处理程序必须立即返回（无论是否有可用的数据或空间）。但是，他们不必立即返回或接受* data *；他们可以改为向客户端指示应该等待。

Our FIFO device operates by maintaining a single, 32kbyte FIFO. Clients can read from, and write to, the FIFO, and will exhibit the blocking behavior discussedabove during full and empty conditions, as appropriate. 我们的FIFO设备通过维护一个32kbyte的FIFO进行操作。客户端可以读取和写入FIFO，并在适当的情况下展现出上述在满空情况下的阻塞行为。

 
### The context structure  上下文结构 

The first thing to look at is the context structure:  首先要看的是上下文结构：

```c
#define FIFOSIZE 32768

typedef struct {
    zx_device_t*    zxdev;
    mtx_t           lock;
    uint32_t        head;
    uint32_t        tail;
    char            data[FIFOSIZE];
} fifodev_t;
```
 

This is a basic circular buffer; data is written to the position indicated by `head` and read from the position indicated by `tail`.If `head == tail` then the FIFO is empty, if `head` is just before `tail` (using wraparound math)then the FIFO is full, otherwise it has both some data and some room available. 这是一个基本的循环缓冲区；数据被写入``head''指示的位置并从``tail''指示的位置读取。如果``head == tail''，则FIFO为空，如果``head''在``tail''之前（使用环绕数学）则FIFO已满，否则它既有一些数据，又有一些可用空间。

At a high level, the **fifo_read()** and **fifo_write()** functions are almost identical, so let's start with the **fifo_write()**: 在较高的层次上，** fifo_read（）**和** fifo_write（）**函数几乎相同，因此让我们从** fifo_write（）**开始：

 

```c
static zx_status_t
fifo_write(void* ctx, const void* buf, size_t len,
           zx_off_t off, size_t* actual) {
    // (1) establish context pointer
    fifodev_t* fifo = ctx;

    // (2) lock mutex
    mtx_lock(&fifo->lock);

    // (3) write as much data as possible
    size_t n = 0;
    size_t count;
    while ((count = fifo_put(fifo, buf, len)) > 0) {
        len -= count;
        buf += count;
        n += count;
    }

    if (n) {
        // (4) wrote something, device is readable
        device_state_set(fifo->zxdev, DEV_STATE_READABLE);
    }
    if (len) {
        // (5) didn't write everything, device is full
        device_state_clr(fifo->zxdev, DEV_STATE_WRITABLE);
    }

    // (6) release mutex
    mtx_unlock(&fifo->lock);

    // (7) inform client of results, possibly blocking it
    *actual = n;
    return (n == 0) ? ZX_ERR_SHOULD_WAIT : ZX_OK;
}
```
 

In step (1), we establish a context pointer to this device instance's context block. Next, we lock the mutex in step (2).This is done because we may have multiple threads in our driver, and we don'twant them to interfere with each other. 在步骤（1）中，我们建立指向该设备实例的上下文块的上下文指针。接下来，我们在步骤（2）中锁定互斥锁，这样做是因为我们的驱动程序中可能有多个线程，并且我们不希望它们相互干扰。

Buffer management is performed in step (3) &mdash; we'll examine the implementation later.  在步骤（3）中执行缓冲器管理。我们将在稍后检查实现。

It's important to understand what actions we need to take after step (3):  了解步骤（3）之后我们需要采取的行动很重要：

 
*   If we wrote one or more bytes (as indicated by `n` being non-zero), we need to mark the device as "readable" (via **device_state_set()**and `DEV_STATE_READABLE`),which is done in step (4). We do this because data is now available. *如果我们写了一个或多个字节（如n表示非零），则需要将设备标记为“可读”（通过device_state_set（）和DEV_STATE_READABLE），这在第四步）。我们这样做是因为现在可以使用数据。
*   If we still have bytes left to write (as indicated by `len` being non-zero), we need to mark the device as "not writable" (via**device_state_clr()** and`DEV_STATE_WRITABLE`), which is done in step (5). We know that the FIFO is full becausewe were not able to write all of our data. *如果还有剩余字节要写入（如len非零表示），则需要将设备标记为“不可写”（通过device_state_clr（）**和DEV_STATE_WRITABLE`），即在步骤（5）中完成。我们知道FIFO已满，因为我们无法写入所有数据。

It's possible that we may execute one or both steps (4) and (5) depending on what happened during the write.We will always execute at least one of them because `n` and `len` can never bothbe zero.That would imply an impossible condition where we both didn't write any data (`n`, thetotal number of bytes transferred, was zero) and simultaneously wrote all of the data(`len`, the remaining number of bytes to transfer, was also zero). 根据写入期间发生的情况，我们可能会执行步骤（4）和（5）中的一个或两个，我们将始终执行至少其中之一，因为`n`和`len`永远都不能为零。一个不可能的情况，我们都没有写任何数据（“ n”，已传输的字节总数为零，而同时写入了所有数据（“ len”，即要传输的剩余字节数也为零） 。

In step (7) is where the decision is made about blocking the client. If `n` is zero, it means that we were not able to write any data.In that case, we return `ZX_ERR_SHOULD_WAIT`.This return value blocks the client. 在步骤（7）中，做出有关阻止客户端的决定。如果n为零，则表示我们无法写入任何数据，在这种情况下，我们将返回ZX_ERR_SHOULD_WAIT，此返回值将阻止客户端。

The client is unblocked when the **device_state_set()** function is called in step (2) from the **fifo_read()** handler: 在步骤（2）中从** fifo_read（）**处理函数调用** device_state_set（）**函数时，客户端将不受阻塞：

```c
static zx_status_t
fifo_read(void* ctx, void* buf, size_t len,
          zx_off_t off, size_t* actual) {
    fifodev_t* fifo = ctx;

    mtx_lock(&fifo->lock);
    size_t n = 0;
    size_t count;

    while ((count = fifo_get(fifo, buf, len)) > 0) {
        len -= count;
        buf += count;
        n += count;
    }

    // (1) same up to here; except read as much as possible

    if (n) {
        // (2) read something, device is writable
        device_state_set(fifo->zxdev, DEV_STATE_WRITABLE);
    }
    if (len) {
        // (3) didn't read everything, device is empty
        device_state_clr(fifo->zxdev, DEV_STATE_READABLE);
    }

    mtx_unlock(&fifo->lock);
    *actual = n;

    return (n == 0) ? ZX_ERR_SHOULD_WAIT : ZX_OK;
}
```
 

The shape of the algorithm is the same as in the writing case, with two differences:  算法的形状与编写案例时相同，但有两个区别：

 
1.  We're reading data, so call **fifo_get()** instead of **fifo_put()**  1.我们正在读取数据，因此调用** fifo_get（）**而不是** fifo_put（）**
2.  The `DEV_STATE` logic is complementary: in the writing case we set readable and cleared writable, in the reading case we set writable and clearreadable. 2. DEV_STATE逻辑是互补的：在写的情况下，我们设置为可读和可清除，在读的情况下，我们设置为可写和可清除。

Similar to the writing case, after the `while` loop we will perform one or both of the following actions: 与编写案例类似，在“ while”循环之后，我们将执行以下一项或两项操作：

 
*   If we read one or more bytes (as indicated by `n` being non-zero), we need to mark the device as now being writable (we consumed data, so there's now some space free). *如果读取一个或多个字节（如n表示非零），则需要将该设备标记为可写（我们消耗了数据，因此现在有一些可用空间）。
*   If we still have bytes to read (as indicated by `len` being non-zero), we mark the device as empty (we didn't get all of our data, so that must be because we drainedthe device). *如果仍然有字节要读取（如len表示非零），则将设备标记为空（我们没有获取所有数据，因此一定是因为我们清空了设备）。

As in the writing case, at least one of the above actions will execute. In order for neither of them to execute, both `n` (the number of bytes read) and `len`(the number of bytes left to read) would have to be zero, implying the impossible,almost metaphysical condition of having read both nothing and everything at the same time. 与书写情况一样，将至少执行上述操作之一。为了使它们都不执行，“ n”（读取的字节数）和“ len”（剩余读取的字节数）都必须为零，这意味着同时读取这两者是不可能的，几乎是形而上的条件一无所有，一切都在同一时间。

> An additional subtlety applies here as well. > When `n` is zero, we *must* return `ZX_ERR_SHOULD_WAIT` &mdash; we can't return `ZX_OK`.> Returning `ZX_OK` with `*actual` set to zero indicates EOF, and that's definitely not> the case here. >此处也适用其他细微之处。 >当n为零时，我们必须*返回ZX_ERR_SHOULD_WAIT mdash;我们不能返回`ZX_OK`。>如果将`* actual`设置为零，返回`ZX_OK`则表示EOF，这肯定不是>。

 
### Read and write interaction  读写互动 

As you can see, the read handler is what allows blocked writing clients to unblock, and the write handler is what allows blocked reading clients to unblock. 如您所见，读取处理程序使阻塞的写入客户端解除阻塞，而写入处理程序使阻塞的读取客户机解除阻塞。

When a client is blocked (via the `ZX_ERR_SHOULD_WAIT` return code), it gets kicked by the corresponding **device_state_set()**function.This kick causes the client to try their read or write operation again. 当客户端被阻止时（通过ZX_ERR_SHOULD_WAIT返回代码），客户端将被相应的** device_state_set（）**函数踢出，此踢使客户端再次尝试其读取或写入操作。

Note that there's no guarantee of success for the client after it gets kicked. We can have multiple readers, for example, waiting for data.Assume that all of them are now blocked, because the FIFO is empty.Another client comes along and writes to the FIFO.This causes the **device_state_set()**function to get called with `DEV_STATE_READABLE`.It's possible that one of the clients consumes all of the available data; theother clients will try to read, but will get `ZX_ERR_SHOULD_WAIT` and will block. 请注意，客户端被踢后并不能保证成功。例如，我们可以有多个读取器在等待数据，假设由于FIFO为空，现在所有的读取器都被阻塞了，另一个客户端随之出现并写入FIFO，这导致** device_state_set（）**函数变为被DEV_STATE_READABLE调用。一个客户端有可能消耗了所有可用数据。其他客户端将尝试读取，但将获得ZX_ERR_SHOULD_WAIT并被阻止。

 
### Buffer management  缓冲区管理 

As promised, and for completeness, here's a quick examination of the buffer management that's common to both routines.We'll look at the read path (the write path is virtually identical). 为了保证完整性，以下是对这两个例程共有的缓冲区管理的快速检查，我们将看一下读取路径（写入路径实际上是相同的）。

In the heart of the read function, we see:  在读取功能的中心，我们看到：

```c
    size_t n = 0;
    size_t count;

    while ((count = fifo_get(fifo, buf, len)) > 0) {
        len -= count;
        buf += count;
        n += count;
    }
```
 

The three variables, `n`, `count`, and `len` are inter-related. The total number of bytes transferred is stored in `n`.During each iteration, `count` gets the number of bytes transferred, and it's used as thebasis to control the `while` loop.The variable `len` indicates the remaining number of bytes to transfer.Each time through the loop, `len` is decreased by the number of bytes transferred, and `n` iscorrespondingly increased. 三个变量“ n”，“ count”和“ len”是相互关联的。传输的总字节数存储在n中，在每次迭代中，count获取传输的字节数，并以此为基础来控制while循环。变量len表示剩余的字节数。要传输的字节数。每次循环，`len`减少传输的字节数，而`n`相应增加。

Because the FIFO is implemented as a circular buffer, it means that one complete set of data might be located contiguously in the FIFO, or it may wrap-aroundthe end of the FIFO back to the beginning. 因为FIFO被实现为循环缓冲区，所以这意味着一个完整的数据集可以连续地位于FIFO中，或者可以将FIFO的末尾回绕到开头。

The underlying **fifo_get()** function gets as much data as it can without wrapping. That's why the `while` loop "retries" the operation; to see if it could getmore data possibly due to the `tail` wrapping back to the beginning of the buffer. 基本的** fifo_get（）**函数无需包装即可获取尽可能多的数据。这就是“ while”循环“重试”操作的原因。看看是否可能由于`tail`包装回到缓冲区的开头而获得更多数据。

We'll call **fifo_get()** between one and three times.  我们将在1-3次之间调用** fifo_get（）**。

 
1.  If the FIFO is empty, we'll call it just once. It will return zero, indicating no data is available. 1.如果FIFO为空，我们将只调用一次。它将返回零，表示没有可用数据。
2.  We call it twice if the data is contiguously located in the underlying FIFO buffer; the first time to get the data, and the second time will return zero, indicating thatno more data is available. 2.如果数据连续位于底层FIFO缓冲区中，我们将其调用两次；第一次获取数据，第二次将返回零，表示没有更多数据可用。
3.  We'll call it three times if the data is wrapped around in the buffer. Once to get the first part, a second time to get the wrap-around part, and a third timewill return zero, indicating that no more data is available. 3.如果数据在缓冲区中包装，我们将调用它三遍。一次获取第一部分，第二次获取环绕部分，第三次返回零，表示没有更多数据可用。

