 

 

<!-- (C) Copyright 2018 The Fuchsia Authors. All rights reserved.Use of this source code is governed by a BSD-style license that can befound in the LICENSE file.--> <！-（C）版权所有2018 The Fuchsia Authors。保留所有权利。此源代码的使用由BSD样式的许可证管理，该许可证可以在LICENSE文件中找到。-->

 
# Advanced Topics and Tips  高级主题和技巧 

This document is part of the [Driver Development Kit tutorial](ddk-tutorial.md) documentation.  本文档是[Driver Development Kit教程]（ddk-tutorial.md）文档的一部分。

 
## Taking a long time to initialize  需要很长时间进行初始化 

What if your device takes a long time to initialize? When we discussed the **null_bind()** function above, we indicated that a successfulreturn told the device manager that the driver is now associated with the device.We can't spend a lot of time in the bind function; we're basically expected to initializeour device, publish it, and be done. 如果您的设备花很长时间初始化怎么办？当我们在上面讨论** null_bind（）**函数时，我们指出成功返回告诉设备管理器驱动程序已经与设备关联。我们不能在绑定函数上花费很多时间；基本上，我们应该初始化设备，发布并完成。

But your device might need to perform a lengthy initialization operation, such as:  但是您的设备可能需要执行冗长的初始化操作，例如：

 
*   enumerate hardware points  *列举硬件要点
*   load firmware  *加载固件
*   negotiate a protocol  *协商协议

and so on, which might take a long time to do.  等等，这可能要花很长时间。

You can publish your device as "invisible" using the `DEVICE_ADD_INVISIBLE` flag. This meets the requirements for the binding function, but nobody is able to useyour device (because nobody knows about it yet, because it's not visible).Now your device can perform the long operations via a background thread. 您可以使用`DEVICE_ADD_INVISIBLE`标志将设备发布为“不可见”。这符合绑定功能的要求，但是没有人能够使用您的设备（因为尚不知道，因为它不可见，因此尚无人知道）。现在，您的设备可以通过后台线程执行长时间的操作。

When your device is ready to service client requests, call **device_make_visible()**which will cause it to appear in the pathname space. 当您的设备准备好服务客户端请求时，请调用** device_make_visible（）**，这会使它出现在路径名空间中。

 
### Power savings  省电 

Two callouts, **suspend()** and **resume()**, are available for your device in order to support power or other resource saving features. 您的设备可以使用两个标注** suspend（）**和** resume（）**来支持电源或其他资源节省功能。

Both take a device context pointer and a flags argument, but the flags argument is used only in the suspend case. 两者都带有设备上下文指针和flags参数，但是flags参数仅在挂起情况下使用。

Flag                                | Meaning ------------------------------------|------------------------------------------------------------`DEVICE_SUSPEND_FLAG_REBOOT`        | The driver should shut itself down in preparation for a reboot or shutdown of the machine`DEVICE_SUSPEND_FLAG_REBOOT_BOOTLOADER` | ?`DEVICE_SUSPEND_FLAG_REBOOT_RECOVERY`   | ?`DEVICE_SUSPEND_FLAG_POWEROFF`      | The driver should shut itself down in preparation for power off`DEVICE_SUSPEND_FLAG_MEXEC`         | @@@ almost nobody uses this except for a graphics controller, what does it do? @@@`DEVICE_SUSPEND_FLAG_SUSPEND_RAM`   | The driver should arrange so that it can be restarted from RAM 标记|含义------------------------------------ | ------------ DEVICE_SUSPEND_FLAG_REBOOT ------------------------------------------------ `|驱动程序应自行关闭，以准备重新引导或关闭计算机DEVICE_SUSPEND_FLAG_REBOOT_BOOTLOADER`。 DEVICE_SUSPEND_FLAG_REBOOT_RECOVERY` | ？`DEVICE_SUSPEND_FLAG_POWEROFF` |驱动程序应自行关闭以准备断电。DEVICE_SUSPEND_FLAG_MEXEC @@@除了图形控制器，几乎没有人使用它，它有什么作用？ @@@`DEVICE_SUSPEND_FLAG_SUSPEND_RAM` |驱动程序应进行安排，以便可以从RAM重新启动

> @@@ Yeah, I'm just guessing on the flags; they're used so little...  > @@@是的，我只是在猜旗帜。他们用得很少...

For documentation purposes, what should I write? That they are just hints, or that you *must* do something because of a given flag, or ... ? 出于文档目的，我应该写什么？它们只是提示，或者您*必须*因为给定的标志而做某事，或者...？

 
## Reference: Support functions  参考：支持功能 

This section lists support functions that are provided for your driver to use.  本节列出了供驱动程序使用的支持功能。

 
### Accessor functions  访问器功能 

The context block that's passed as the first argument to your driver's protocol functions is an opaque data structure.This means that in order to access the data elements, you need to call an accessor function: 作为驱动程序协议函数的第一个参数传递的上下文块是不透明的数据结构，这意味着要访问数据元素，您需要调用访问器函数：

Function                | Purpose ------------------------|-------------------------------------------**device_get_name()**        | Retrieves the name of the device**device_get_parent()**      | Retrieves the parent device of the device 功能介绍目的------------------------ | ------------------------ ------------------- ** device_get_name（）** |检索设备的名称** device_get_parent（）** |检索设备的父设备

 
### Administrative functions  行政职能 

The following functions are used to administer the device:  以下功能用于管理设备：

Function                    | Purpose ----------------------------|-------------------------------------------**device_add()**                 | Adds a device to a parent**device_make_visible()**        | Makes a device visible**device_async_remove()**        | Schedules the removal of a device and all its children 功能介绍目的---------------------------- | -------------------- ----------------------- ** device_add（）** |将设备添加到父设备** device_make_visible（）** |使设备可见** device_async_remove（）** |计划移除设备及其所有子设备

 
### Signalling  发信号 

The following functions are used to set the state of a device:  以下功能用于设置设备的状态：

Function                | Purpose ------------------------|-------------------------------------------**device_state_set()**       | sets the given signal(s) on the device**device_state_clr()**       | clears the given signal(s) on the device 功能介绍目的------------------------ | ------------------------ ------------------- ** device_state_set（）** |设置设备上的给定信号** device_state_clr（）** |清除设备上的给定信号

We saw these in the `/dev/misc/demo-fifo` handler above.  我们在上面的`/ dev / misc / demo-fifo`处理程序中看到了这些。

@@@ Notes only @@@  @@@仅注释@@@

This section is great for things like talking about buffer management, threading, best practices, advanced options for device_add(), and so on.I think it can be somewhere between the man page ("printf is used to print a stringand takes the following parameters") and an application note &mdash; I want to seeexamples of how to use the functions, what the arguments mean, what the impact ofvarious design decisions is, that kind of thing. 本节非常适合讨论缓冲区管理，线程，最佳实践，device_add（）的高级选项等内容。我认为它可以在手册页之间（“ printf用于打印字符串，并接受以下内容）参数”）和应用说明-我想看看有关如何使用函数，参数含义，各种设计决策的影响之类的示例。

