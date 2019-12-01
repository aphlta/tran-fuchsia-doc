Fuchsia Core Libraries ====================== 紫红色的核心库======================

This document describes the core libraries in the Fuchsia system, starting from the bottom of the dependency chain. 本文档从依赖关系链的底部开始描述了Fuchsia系统中的核心库。

 
# Zircon libraries  锆石库 

 
## libzircon  利比西康 

This library defines the Zircon system ABI.  该库定义了Zircon系统ABI。

TODO(kulakowski) Talk about how this is not quite the kernel syscall interface, since the VDSO abstracts that. TODO（kulakowski）讨论这不是内核syscall接口，因为VDSO对此进行了抽象。

 
## libzx  libzx 

libzircon defines C types and function calls acting on those objects. libzx is a light C++ wrapper around those. It adds typesafety beyond `zx_handle_t`, so that every kernel object type has acorresponding C++ type, and adds ownership semantics to thosehandles. It otherwise takes no opinions around naming or policy. libzircon定义了C类型和作用于这些对象的函数调用。 libzx是围绕它们的轻量级C ++包装器。除了`zx_handle_t`之外，它还增加了类型安全性，因此每个内核对象类型都具有对应的C ++类型，并为这些句柄添加了所有权语义。否则，它不会对命名或政策提出任何意见。

For more information about libzx, see [its documentation](/zircon/system/ulib/zx/README.md). 有关libzx的更多信息，请参见[其文档]（/ zircon / system / ulib / zx / README.md）。

 
## FBL  FBL 

Much of Zircon is written in C++, both in kernel and in userspace. Linking against the C++ standard library is not especiallywell suited to this environment (it is too easy to allocate, throwexceptions, etc., and the library itself is large). There are a numberof useful constructs in the standard library that we would wish to use,like type traits and unique pointers. However, C++ standard librariesare not really to be consumed piecemeal like this. So we built alibrary which provides similar constructs named fbl. This libraryalso includes constructs not present in the standard library but whichare useful library code for kernel and device driver environments (forinstance, slab allocation). Zircon的许多内容都是用C ++编写的，无论是在内核中还是在用户空间中。与C ++标准库的链接并不是特别适合此环境（它太容易分配，抛出异常等，并且库本身很大）。我们希望在标准库中使用许多有用的构造，例如类型特征和唯一指针。但是，C ++标准库并不是真的像这样被零碎使用。因此，我们构建了提供类似名为fbl的结构的库。该库还包含标准库中不存在的构造，但对内核和设备驱动程序环境（实例，平板分配）有用的库代码。

For more information about FBL, [read its overview](/docs/development/languages/c-cpp/cxx.md#fbl). 有关FBL的更多信息，请[阅读其概述]（/ docs / development / languages / c-cpp / cxx.mdfbl）。

 
# FXL  特长 

FXL is a platform-independent library containing basic C++ building blocks, such as logging and reference counting. FXL depends on the C++ standard library butnot on any Zircon- or Fuchsia-specific libraries. We build FXL both for target(Fuchsia) and for host (Linux, Mac) systems. FXL是一个独立于平台的库，其中包含基本的C ++构建块，例如日志记录和引用计数。 FXL依赖于C ++标准库，但不依赖于任何Zircon或紫红色的特定库。我们为目标（紫红色）和主机（Linux，Mac）系统构建FXL。

