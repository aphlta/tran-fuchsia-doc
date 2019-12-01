 
# The Banjo Tutorial  班卓琴教程 

This document is part of the [Zircon Driver Development Kit](/docs/concepts/drivers/overview.md) documentation.  本文档是[Zircon驱动程序开发套件]（/ docs / concepts / drivers / overview.md）文档的一部分。

[TOC]  [目录]

Banjo is a "transpiler" (like [FIDL's `fidlc`](/docs/development/languages/fidl/README.md))&mdash; a program that converts an interface definition language (**IDL**) into target languagespecific files. Banjo是一个“编译器”（例如[FIDL的`fidlc`]（/ docs / development / languages / fidl / README.md））将接口定义语言（** IDL **）转换为目标语言特定文件的程序。

This tutorial is structured as follows:  本教程的结构如下：

 
* brief overview of Banjo  *班卓琴简介
* simple example (I2C)  *简单示例（I2C）
* explanation of generated code from example  *举例说明生成的代码

There's also a reference section that includes:  还有一个参考部分，其中包括：

 
* a list of builtin keywords and primitive types.  *内置关键字和原始类型的列表。

 
# Overview  总览 

Banjo generates C and C++ code that can be used by both the protocol implementer and the protocol user. Banjo生成可由协议实现者和协议用户使用的C和C ++代码。

 
# A simple example  一个简单的例子 

As a first step, let's take a look at a relatively simple Banjo specification. This is the file [`//zircon/system/banjo/ddk.protocol.i2c/i2c.banjo`](/zircon/system/banjo/ddk.protocol.i2c/i2c.banjo): 第一步，让我们看一个相对简单的Banjo规范。这是文件[`//zircon/system/banjo/ddk.protocol.i2c/i2c.banjo`](/zircon/system/banjo/ddk.protocol.i2c/i2c.banjo）：

> Note that the line numbers in the code samples throughout this tutorial are not part of the files.  >请注意，本教程中的代码示例中的行号不是文件的一部分。

```banjo
[01] // Copyright 2018 The Fuchsia Authors. All rights reserved.
[02] // Use of this source code is governed by a BSD-style license that can be
[03] // found in the LICENSE file.
[04]
[05] library ddk.protocol.i2c;
[06]
[07] using zx;
[08]
[09] const uint32 I2C_10_BIT_ADDR_MASK = 0xF000;
[10] const uint32 I2C_MAX_RW_OPS = 8;
[11]
[12] /// See `Transact` below for usage.
[13] struct I2cOp {
[14]     vector<voidptr> data;
[15]     bool is_read;
[16]     bool stop;
[17] };
[18]
[19] [Layout = "ddk-protocol"]
[20] protocol I2c {
[21]     /// Writes and reads data on an i2c channel. Up to I2C_MAX_RW_OPS operations can be passed in.
[22]     /// For write ops, i2c_op_t.data points to data to write.  The data to write does not need to be
[23]     /// kept alive after this call.  For read ops, i2c_op_t.data is ignored.  Any combination of reads
[24]     /// and writes can be specified.  At least the last op must have the stop flag set.
[25]     /// The results of the operations are returned asynchronously via the transact_cb.
[26]     /// The cookie parameter can be used to pass your own private data to the transact_cb callback.
[27]     [Async]
[28]     Transact(vector<I2cOp> op) -> (zx.status status, vector<I2cOp> op);
[29]     /// Returns the maximum transfer size for read and write operations on the channel.
[30]     GetMaxTransferSize() -> (zx.status s, usize size);
[31]     GetInterrupt(uint32 flags) -> (zx.status s, handle<interrupt> irq);
[32] };
```
 

It defines an interface that allows an application to read and write data on an I2C bus. In the I2C bus, data must first be written to the device in order to solicita response.If a response is desired, the response can be read from the device.(A response might not be required when setting a write-only register, for example.) 它定义了一个接口，该接口允许应用程序在I2C总线上读取和写入数据。在I2C总线中，必须先将数据写入设备才能请求响应。如果需要响应，则可以从设备中读取响应（对于设置只读寄存器，可能不需要响应）例。）

Let's look at the individual components, line-by-line:  让我们逐行查看各个组件：

 
* `[05]` &mdash; the `library` directive tells the Banjo compiler what prefix it should use on the generated output; think of it as a namespace specifier. *`[05]`mdash; “ library”指令告诉Banjo编译器应该在生成的输出上使用什么前缀；将其视为名称空间说明符。
* `[07]` &mdash; the `using` directive tells Banjo to include the `zx` library.  *`[07]`mdash; using指令告诉Banjo包含zx库。
* `[09]` and `[10]` &mdash; these introduce two constants for use by the programmer.  *`[09]`和`[10]`mdash;这些引入了两个常量供程序员使用。
* `[13` .. `17]` &mdash; these define a structure, called `I2cOp`, that the programmer will then use for transferring data to and from the bus. *`[13` ..`17]`mdash;它们定义了一个称为“ I2cOp”的结构，程序员将使用该结构在总线之间来回传输数据。
* `[19` .. `32]` &mdash; these lines define the interface methods that are provided by this Banjo specification; we'll discuss this in greater detail [below](#the-interface). *`[19` ..`32]`mdash;这些行定义了此Banjo规范提供的接口方法；我们将在下面（界面）进行更详细的讨论。

> Don't be confused by the comments on `[21` .. `26]` (and elsewhere) &mdash; they're > "flow through" comments that are intended to be emitted into the generated source.> Any comment that starts with "`///`" (three! slashes) is a "flow through" comment.> Ordinary comments (that is, "`//`") are intended for the current module.> This will become clear when we look at the generated code. >不要对`[21` ..`26]`（及其他地方）的评论感到困惑；它们是>旨在发送到生成的源中的“流过”注释。>任何以“`///`”（三个！斜杠）开头的注释都是“流过”注释。>普通注释（也就是“`//`”）用于当前模块。>当我们查看生成的代码时，这将变得很清楚。

 
## The operation structure  运作架构 

In our I2C sample, the `struct I2cOp` structure defines three elements:  在我们的I2C示例中，“ struct I2cOp”结构定义了三个元素：

Element   | Type              | Use ----------|-------------------|-----------------------------------------------------------------`data`    | `vector<voidptr>` | contains the data sent to, and optionally received from, the bus`is_read` | `bool`            | flag indicating read functionality desired`stop`    | `bool`            | flag indicating a stop byte should be sent after the operation 元素|类型使用---------- | ------------------- | ------------------ -----------------------------------------------`数据` | `vector <voidptr>`|包含发送到总线is_read |或从总线is_read |接收的数据（可选） `bool` |表示需要读取功能的标志。 `bool` |指示应该在操作后发送停止字节的标志

The structure defines the communications area that will be used between the protocol implementation (the driver) and the protocol user (the program that's using the bus). 该结构定义了将在协议实现（驱动程序）和协议用户（正在使用总线的程序）之间使用的通信区域。

 
## The interface  介面 

The more interesting part is the `protocol` specification.  更有趣的部分是“协议”规范。

We'll skip the `[Layout]` (line `[19]`) and `[Async]` (line `[27]`) attributes for now, but will return to them below, in [Attributes](#attributes). 我们现在暂时跳过[Layout]（第[19]行）和[Async]（第[27]行）属性，但下面将在[Attributes]（属性）中返回它们。

The `protocol` section defines three interface methods:  协议部分定义了三种接口方法：

 
* `Transact`  *`交易`
* `GetMaxTransferSize`  *`GetMaxTransferSize`
* `GetInterrupt`  *`GetInterrupt`

Without going into details about their internal operations (this isn't a tutorial on I2C, after all), let's see how they translate into the target language.We'll look at the C and C++ implementations separately, using the C descriptionto include the structure definition that's common to the C++ version as well. 在不详细介绍它们的内部操作的情况下（毕竟这不是I2C的教程），让我们看看它们如何转换为目标语言。我们将分别使用C描述和C实现来了解C和C ++的实现。结构定义也是C ++版本共有的。

> Currently, generation of C and C++ code is supported, with Rust support planned > in the future. >当前，支持生成C和C ++代码，并计划在将来支持Rust。

 
## C  C 

The C implementation is relatively straightforward:  C实现相对简单：

 
* `struct`s and `union`s map almost directly into their C language counterparts.  *`struct`和`union`几乎直接映射到对应的C语言。
* `enum`s and constants are generated as `#define` macros.  *`enum`和常量作为`define`宏生成。
* `protocol`s are generated as two `struct`s:  *`protocol`生成为两个`struct`s：
    * a function table, and  *功能表，以及
    * a struct with pointers to the function table and a context.  *具有指向功能表和上下文的指针的结构。
* Some helper functions are also generated.  *还生成了一些辅助功能。

The C version is generated into `//zircon/build-`_TARGET_`/system/banjo/ddk-protocol-i2c/gen/include/ddk/protocol/i2c.h`,where _TARGET_ is the target architecture, e.g., `arm64`. C版本生成到`// zircon / build_`_TARGET_` / system / banjo / ddk-protocol-i2c / gen / include / ddk / protocol / i2c.h`中，其中_TARGET_是目标体系结构，例如， arm64`。

The file is relatively long, so we'll look at it in several parts.  该文件相对较长，因此我们将分几部分进行介绍。

 
### Boilerplate  样板 

The first part has some boilerplate which we'll show without further comment:  第一部分有一些样板，我们将在不做进一步评论的情况下显示它们：

```c
[01] // Copyright 2018 The Fuchsia Authors. All rights reserved.
[02] // Use of this source code is governed by a BSD-style license that can be
[03] // found in the LICENSE file.
[04]
[05] // WARNING: THIS FILE IS MACHINE GENERATED. DO NOT EDIT.
[06] //          MODIFY system/banjo/ddk-protocol-i2c/i2c.banjo INSTEAD.
[07]
[08] #pragma once
[09]
[10] #include <zircon/compiler.h>
[11] #include <zircon/types.h>
[12]
[13] __BEGIN_CDECLS
```
 

 
### Forward declarations  转发声明 

Next are forward declarations for our structures and functions:  接下来是我们的结构和功能的前向声明：

```c
[15] // Forward declarations
[16]
[17] typedef struct i2c_op i2c_op_t;
[18] typedef struct i2c_protocol i2c_protocol_t;
[19] typedef void (*i2c_transact_callback)(void* ctx, zx_status_t status, const i2c_op_t* op_list, size_t op_count);
[20]
[21] // Declarations
[22]
[23] // See `Transact` below for usage.
[24] struct i2c_op {
[25]     const void* data_buffer;
[26]     size_t data_size;
[27]     bool is_read;
[28]     bool stop;
[29] };
```
 

Note that lines `[17` .. `19]` only declare types, they don't actually define structures or prototypes for functions. 请注意，第[17 ...`19]行仅声明类型，而实际上并未定义函数的结构或原型。

Notice how the "flow through" comments (original `.banjo` file line `[12]`, for example) got emitted into the generated code (line `[23]` above), with one slash stripped off tomake them look like normal comments. 请注意如何将“流过”注释（例如，原始的.banjo文件行“ [12]”）发射到生成的代码中（上面的行“ [23]”），并去除一个斜杠以使它们看起来像正常的评论。

Lines `[24` .. `29`] are, as advertised, an almost direct mapping of the `struct I2cOp` from the `.banjo` file above (lines `[13` .. `17`]). 如广告所示，第[[24` ..`29`]行是上面的.banjo文件中的`struct I2cOp`的几乎直接映射（第[[13`..`17`]行）。

Astute C programmers will immediately see how the C++ style `vector<voidptr> data` (original `.banjo` file line `[14]`) is handled in C: it gets converted to a pointer("`data_buffer`") and a size ("`data_size`"). 精明的C程序员将立即看到如何在C中处理C ++样式的`vector <voidptr> data`（原始的`.banjo`文件行`[14]`）：将其转换为指针（“ data_buffer””）并大小（“ data_size”）。

> As far as the naming goes, the base name is `data` (as given in the `.banjo` file). > For a vector of `voidptr`, the transpiler appends `_buffer` and `_size` to convert the> `vector` into a C compatible structure.> For all other vector types, the transpiler appends `_list` and `_count` instead (for> code readability). >就命名而言，基本名称是`data`（如.banjo文件中所给）。 >对于矢量`voidptr`，Transpiler附加`_buffer`和`_size`将`vector`转换为C兼容结构。>对于所有其他矢量类型，Transpiler附加``_list`和`_count` （用于>代码可读性）。

 
### Constants  常数 

Next, we see our `const uint32` constants converted into `#define` statements:  接下来，我们将我们的const uint32常量转换为define语句：

```c
[31] #define I2C_MAX_RW_OPS UINT32_C(8)
[32]
[33] #define I2C_10_BIT_ADDR_MASK UINT32_C(0xF000)
```
 

In the C version, We chose `#define` instead of "passing through" the `const uint32_t` representation because: 在C版本中，我们选择“定义”而不是“通过” const uint32_t表示，因为：

 
* `#define` statements only exist at compile time, and get inlined at every usage site, whereas a `const uint32_t` would get embedded in the binary, and *`define`语句仅在编译时存在，并在每个使用站点内联，而`const uint32_t'将嵌入二进制文件中，并且
* `#define` allows for more compile time optimizations (e.g., doing math with the constant value).  *`define`可以进行更多的编译时间优化（例如，使用常数值进行数学运算）。

The downside is that we don't get type safety, which is why you see the helper macros (like **UINT32_C()** above); they just cast the constant to the appropriate type. 缺点是我们没有类型安全，这就是为什么您看到帮助程序宏的原因（例如上面的** UINT32_C（）**）；他们只是将常量转换为适当的类型。

 
### Protocol structures  协议结构 

And now we get into the good parts.  现在我们进入精采部分。

```c
[35] typedef struct i2c_protocol_ops {
[36]     void (*transact)(void* ctx, const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie);
[37]     zx_status_t (*get_max_transfer_size)(void* ctx, size_t* out_size);
[38]     zx_status_t (*get_interrupt)(void* ctx, uint32_t flags, zx_handle_t* out_irq);
[39] } i2c_protocol_ops_t;
```
 

This `typedef` creates a structure definition that contains the three `protocol` methods that were defined in the original `.banjo` file at lines `[28]`, `[30]` and `[31]`. 这个typedef创建一个结构定义，该结构定义包含在原始.banjo文件中的第[28]，第[30]和第[31]行中定义的三个`protocol`方法。

Notice the name mangling that has occurred &mdash; this is how you can map the `protocol` method names to the C function pointer names so that you know whatthey're called: 请注意发生的名称修改-mdash;这是将“协议”方法名称映射到C函数指针名称的方式，以便您知道它们的名称：

Banjo                | C                       | Rule ---------------------|-------------------------|---------------------------------------------------------------`Transact`           | `transact`              | Convert leading uppercase to lowercase`GetMaxTransferSize` | `get_max_transfer_size` | As above, and convert camel-case to underscore-separated style`GetInterrupt`       | `get_interrupt`         | Same as above 班卓| C |规则--------------------- | ------------------------- |- -------------------------------------------------- ------------`交易`| `transact` |将前导大写字母转换为小写字母GetMaxTransferSize `get_max_transfer_size` |如上所述，将驼峰式大小写转换为下划线分隔的样式GetInterrupt | `get_interrupt` |同上

Next, the interface definitions are wrapped in a context-bearing structure:  接下来，接口定义被包装在一个带有上下文的结构中：

```c
[41] struct i2c_protocol {
[42]     i2c_protocol_ops_t* ops;
[43]     void* ctx;
[44] };
```
 

And now the "flow-through" comments (`.banjo` file, lines `[21` .. `26]`) suddenly make way more sense! 现在，“流通”注释（.banjo`文件，第[[21`..`26]`行）突然变得更有意义了！

```c
[46] // Writes and reads data on an i2c channel. Up to I2C_MAX_RW_OPS operations can be passed in.
[47] // For write ops, i2c_op_t.data points to data to write.  The data to write does not need to be
[48] // kept alive after this call.  For read ops, i2c_op_t.data is ignored.  Any combination of reads
[49] // and writes can be specified.  At least the last op must have the stop flag set.
[50] // The results of the operations are returned asynchronously via the transact_cb.
[51] // The cookie parameter can be used to pass your own private data to the transact_cb callback.
```
 

Finally, we see the actual generated code for the three methods:  最后，我们看到了三种方法的实际生成的代码：

```c
[52] static inline void i2c_transact(const i2c_protocol_t* proto, const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie) {
[53]     proto->ops->transact(proto->ctx, op_list, op_count, callback, cookie);
[54] }
[55] // Returns the maximum transfer size for read and write operations on the channel.
[56] static inline zx_status_t i2c_get_max_transfer_size(const i2c_protocol_t* proto, size_t* out_size) {
[57]     return proto->ops->get_max_transfer_size(proto->ctx, out_size);
[58] }
[59] static inline zx_status_t i2c_get_interrupt(const i2c_protocol_t* proto, uint32_t flags, zx_handle_t* out_irq) {
[60]     return proto->ops->get_interrupt(proto->ctx, flags, out_irq);
[61] }
```
 

 
### Prefixes and paths  前缀和路径 

Notice how the prefix `i2c_` (from the interface name, `.banjo` file line `[20]`) got added to the method names; thus, `Transact` became `i2c_transact`, and so on.This is part of the mapping between `.banjo` names and their C equivalents. 注意如何在方法名称中添加前缀“ i2c _”（来自接口名称“ .banjo”文件行“ [20]”）；因此，“ Transact”变成了“ i2c_transact”，依此类推。这是“ .banjo”名称与其C等效项之间映射的一部分。

Also, the `library` name (line `[05]` in the `.banjo` file) is transformed into the include path: so `library ddk.protocol.i2c` implies a path of `<ddk/protocol/i2c.h>`. 同样，库名称（.banjo文件中的行[05]）被转换为包含路径：因此库ddk.protocol.i2c隐含路径<ddk / protocol / i2c。 h>`。

 
## C++  C ++ 

The C++ code is slightly more complex than the C version. Let's take a look. C ++代码比C版本稍微复杂一些。让我们来看看。

The Banjo transpiler generates three files: the first is the C file discussed above, and the other two are under`//zircon/build-`_TARGET_`/system/banjo/ddk-protocol-i2c/gen/include/ddktl/protocol/`: Banjo编译器生成三个文件：第一个是上面讨论的C文件，另外两个在// zircon / build-_TARGET_ / system / banjo / ddk-protocol-i2c / gen / include / ddktl / protocol下/`：

 
* `i2c.h` &mdash; the file your program should include, and  *`i2c.h` mdash;您的程序应包含的文件，以及
* `i2c-internal.h` &mdash; an internal file, included by `i2c.h`  *`i2c-internal.h` mdash;内部文件，包含在“ i2c.h”中

As usual, _TARGET_ is the build target architecture (e.g., `x64`).  与往常一样，_TARGET_是构建目标架构（例如x64）。

The "internal" file contains declarations and assertions, which we can safely skip.  “内部”文件包含声明和断言，我们可以安全地跳过它们。

The C++ version of `i2c.h` is fairly long, so we'll look at it in smaller pieces. Here's an overview "map" of what we'll be looking at, showing the starting linenumber of each piece: C2版的“ i2c.h”相当长，因此我们将对其进行较小的讨论。这是我们将要查看的内容的概述“地图”，显示了每个片段的起始行号：

Line | Section --------------|---------------------------- 线|第-------------- || ----------------------------
1    | [boilerplate](#a-simple-example-c-boilerplate-2)  1 | [样板]（a-simple-example-c-boilerplate-2）
20   | [auto generated usage comments](#auto_generated-comments)  20 | [自动生成的用法注释]（auto_generation-comments）
55   | [class I2cProtocol](#the-i2cprotocol-mixin-class)  55 | [class I2cProtocol]（the-i2cprotocol-mixin-class）
99   | [class I2cProtocolClient](#the-i2cprotocolclient-wrapper-class)  99 | [class I2cProtocolClient]（the-i2cprotocolclient-wrapper-class）

 
### Boilerplate  样板 

The boilerplate is pretty much what you'd expect:  样板几乎是您所期望的：

```c++
[001] // Copyright 2018 The Fuchsia Authors. All rights reserved.
[002] // Use of this source code is governed by a BSD-style license that can be
[003] // found in the LICENSE file.
[004]
[005] // WARNING: THIS FILE IS MACHINE GENERATED. DO NOT EDIT.
[006] //          MODIFY system/banjo/ddk-protocol-i2c/i2c.banjo INSTEAD.
[007]
[008] #pragma once
[009]
[010] #include <ddk/driver.h>
[011] #include <ddk/protocol/i2c.h>
[012] #include <ddktl/device-internal.h>
[013] #include <zircon/assert.h>
[014] #include <zircon/compiler.h>
[015] #include <zircon/types.h>
[016] #include <lib/zx/interrupt.h>
[017]
[018] #include "i2c-internal.h"
```
 

It `#include`s a bunch of DDK and OS headers, including:  它包含一堆DDK和OS标头，包括：

 
* the C version of the header (line `[011]`, which means that everything discussed [above in the C section](#a-simple-example-c-1) applies here as well), and *标头的C版本（第[011]行，这意味着[C部分以上]（a-simple-example-c-1）讨论的所有内容也都适用于此），以及
* the generated `i2c-internal.h` file (line `[018]`).  *生成的“ i2c-internal.h”文件（第[018]行）。

Next is the "auto generated usage comments" section; we'll come back to that [later](#auto_generated-comments) as it will make more sense once we've seenthe actual class declarations. 接下来是“自动生成的使用情况注释”部分；我们将回到[稍后]（auto_generation-comments），因为一旦我们看到了实际的类声明，它将变得更有意义。

The two class declarations are wrapped in the DDK namespace:  这两个类声明包装在DDK名称空间中：

```c++
[053] namespace ddk {
...
[150] } // namespace ddk
```
 

 
### The I2cProtocolClient wrapper class  I2cProtocolClient包装器类 

The `I2cProtocolClient` class is a simple wrapper around the `i2c_protocol_t` structure (defined in the C include file, line `[41]` which we discussed in[Protocol structures](#protocol-structures), above). I2cProtocolClient类是围绕i2c_protocol_t结构的简单包装（在C包含文件第[41]行中定义，我们在上面的[协议结构]（协议结构）中进行了讨论）。

```c++
[099] class I2cProtocolClient {
[100] public:
[101]     I2cProtocolClient()
[102]         : ops_(nullptr), ctx_(nullptr) {}
[103]     I2cProtocolClient(const i2c_protocol_t* proto)
[104]         : ops_(proto->ops), ctx_(proto->ctx) {}
[105]
[106]     I2cProtocolClient(zx_device_t* parent) {
[107]         i2c_protocol_t proto;
[108]         if (device_get_protocol(parent, ZX_PROTOCOL_I2C, &proto) == ZX_OK) {
[109]             ops_ = proto.ops;
[110]             ctx_ = proto.ctx;
[111]         } else {
[112]             ops_ = nullptr;
[113]             ctx_ = nullptr;
[114]         }
[115]     }
[116]
[117]     void GetProto(i2c_protocol_t* proto) const {
[118]         proto->ctx = ctx_;
[119]         proto->ops = ops_;
[120]     }
[121]     bool is_valid() const {
[122]         return ops_ != nullptr;
[123]     }
[124]     void clear() {
[125]         ctx_ = nullptr;
[126]         ops_ = nullptr;
[127]     }
[128]     // Writes and reads data on an i2c channel. Up to I2C_MAX_RW_OPS operations can be passed in.
[129]     // For write ops, i2c_op_t.data points to data to write.  The data to write does not need to be
[130]     // kept alive after this call.  For read ops, i2c_op_t.data is ignored.  Any combination of reads
[131]     // and writes can be specified.  At least the last op must have the stop flag set.
[132]     // The results of the operations are returned asynchronously via the transact_cb.
[133]     // The cookie parameter can be used to pass your own private data to the transact_cb callback.
[134]     void Transact(const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie) const {
[135]         ops_->transact(ctx_, op_list, op_count, callback, cookie);
[136]     }
[137]     // Returns the maximum transfer size for read and write operations on the channel.
[138]     zx_status_t GetMaxTransferSize(size_t* out_size) const {
[139]         return ops_->get_max_transfer_size(ctx_, out_size);
[140]     }
[141]     zx_status_t GetInterrupt(uint32_t flags, zx::interrupt* out_irq) const {
[142]         return ops_->get_interrupt(ctx_, flags, out_irq->reset_and_get_address());
[143]     }
[144]
[145] private:
[146]     i2c_protocol_ops_t* ops_;
[147]     void* ctx_;
[148] };
```
 

There are three constructors:  有三个构造函数：

 
* the default one (`[101]`) that sets `ops_` and `ctx_` to `nullptr`,  *将`ops_`和`ctx_`设置为`nullptr`的默认值（`[101]`），
* an initializer (`[103]`) that takes a pointer to an `i2c_protocol_t` structure and populates the `ops_` and `ctx`_ fields from their namesakes in the structure, and *初始化程序（[[103]`），它使用指向i2c_protocol_t结构的指针，并从结构中的同名字段中填充ops_和ctx_字段，以及
* another initializer (`[106]`) that extracts the `ops`_ and `ctx_` information from a `zx_device_t`. *另一个初始化程序（`[106]`）从`zx_device_t`中提取`ops__和`ctx_`信息。

The last constructor is the preferred one, and can be used like this:  最后一个构造函数是首选的构造函数，可以这样使用：

```c++
ddk::I2cProtocolClient i2c(parent);
if (!i2c.is_valid()) {
  return ZX_ERR_*; // return an appropriate error
}
```
 

Three convenience member functions are provided:  提供了三个便捷成员功能：

 
* `[117]` **GetProto()** fetches the `ctx_` and `ops_` members into a protocol structure,  *`[117]`** GetProto（）**将`ctx_`和`ops_`成员获取到协议结构中，
* `[121]` **is_valid()** returns a `bool` indicating if the class has been initialized with a protocol, and *`[121]`** is_valid（）**返回一个`bool`，指示类是否已使用协议初始化，并且
* `[124]` **clear()** invalidates the `ctx_` and `ops_` pointers.  *`[124]`** clear（）**使`ctx_`和`ops_`指针无效。

Next we find the three member functions that were specified in the `.banjo` file:  接下来，我们找到.banjo文件中指定的三个成员函数：

 
* `[134]` **Transact()**,  *`[134]`** Transact（）**，
* `[138]` **GetMaxTransferSize()**, and  *`[138]`** GetMaxTransferSize（）**，和
* `[141]` **GetInterrupt()**.  *`[141]`** GetInterrupt（）**。

These work just liked the three wrapper functions from the C version of the include file &mdash; that is, they pass their arguments into a call through the respective function pointer. 这些工作就像包含文件mdash的C版本中的三个包装函数一样。也就是说，它们通过各自的函数指针将其参数传递给调用。

In fact, compare **i2c_get_max_transfer_size()** from the C version:  实际上，请比较C版本中的** i2c_get_max_transfer_size（）**：

```c
[56] static inline zx_status_t i2c_get_max_transfer_size(const i2c_protocol_t* proto, size_t* out_size) {
[57]     return proto->ops->get_max_transfer_size(proto->ctx, out_size);
[58] }
```
 

with the C++ version above:  使用上述C ++版本：

```c++
[138] zx_status_t GetMaxTransferSize(size_t* out_size) const {
[139]   return ops_->get_max_transfer_size(ctx_, out_size);
[140] }
```
 

As advertised, all that this class does is store the operations and context pointers for later use, so that the call through the wrapper is more elegant. 正如所宣传的那样，该类所做的只是存储操作和上下文指针以供以后使用，从而使通过包装器进行的调用更加优雅。

> You'll also notice that the C++ wrapper function doesn't have any name mangling &mdash; > to use a tautology, **GetMaxTransferSize()** is **GetMaxTransferSize()**. >您还将注意到，C ++包装函数没有任何名称修饰mdash； >要使用重言式，** GetMaxTransferSize（）**是** GetMaxTransferSize（）**。

 
### The I2cProtocol mixin class  I2cProtocol mixin类 

Ok, that was the easy part. For this next part, we're going to talk about [mixins](https://en.wikipedia.org/wiki/Mixin)and [CRTPs &mdash; or Curiously Recurring TemplatePatterns](https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern). 好的，那是容易的部分。在下一部分中，我们将讨论[mixins]（https://en.wikipedia.org/wiki/Mixin）和[CRTP短划线；或“好奇地重复使用模板模式”]（https://en.wikipedia.org/wiki/Curiously_recurring_template_pattern）。

Let's understand the "shape" of the class first (comment lines deleted for outlining purposes): 首先让我们了解类的“形状”（为了概述目的删除注释行）：

```c++
[055] template <typename D, typename Base = internal::base_mixin>
[056] class I2cProtocol : public Base {
[057] public:
[058]     I2cProtocol() {
[059]         internal::CheckI2cProtocolSubclass<D>();
[060]         i2c_protocol_ops_.transact = I2cTransact;
[061]         i2c_protocol_ops_.get_max_transfer_size = I2cGetMaxTransferSize;
[062]         i2c_protocol_ops_.get_interrupt = I2cGetInterrupt;
[063]
[064]         if constexpr (internal::is_base_proto<Base>::value) {
[065]             auto dev = static_cast<D*>(this);
[066]             // Can only inherit from one base_protocol implementation.
[067]             ZX_ASSERT(dev->ddk_proto_id_ == 0);
[068]             dev->ddk_proto_id_ = ZX_PROTOCOL_I2C;
[069]             dev->ddk_proto_ops_ = &i2c_protocol_ops_;
[070]         }
[071]     }
[072]
[073] protected:
[074]     i2c_protocol_ops_t i2c_protocol_ops_ = {};
[075]
[076] private:
...
[083]     static void I2cTransact(void* ctx, const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie) {
[084]         static_cast<D*>(ctx)->I2cTransact(op_list, op_count, callback, cookie);
[085]     }
...
[087]     static zx_status_t I2cGetMaxTransferSize(void* ctx, size_t* out_size) {
[088]         auto ret = static_cast<D*>(ctx)->I2cGetMaxTransferSize(out_size);
[089]         return ret;
[090]     }
[091]     static zx_status_t I2cGetInterrupt(void* ctx, uint32_t flags, zx_handle_t* out_irq) {
[092]         zx::interrupt out_irq2;
[093]         auto ret = static_cast<D*>(ctx)->I2cGetInterrupt(flags, &out_irq2);
[094]         *out_irq = out_irq2.release();
[095]         return ret;
[096]     }
[097] };
```
 

The `I2CProtocol` class inherits from a base class, specified by the second template parameter. If it's left unspecified, it defaults to `internal::base_mixin`, and no special magic happens.If, however, the base class is explicitly specified, it should be `ddk::base_protocol`,in which case additional asserts are added (to double check that only one mixin is the base protocol).In addition, special DDKTL fields are set to automatically register this protocol as thebase protocol when the driver triggers **DdkAdd()**. I2CProtocol类继承自第二个模板参数指定的基类。如果未指定，则默认为`internal :: base_mixin`，并且不会发生任何特殊的魔术操作。但是，如果显式指定了基类，则应将其指定为`ddk :: base_protocol`，在这种情况下将添加其他断言（再次检查是否只有一个mixin是基本协议。此外，特殊的DDKTL字段设置为在驱动程序触发** DdkAdd（）**时自动将该协议注册为基本协议。

The constructor calls an internal validation function, **CheckI2cProtocolSubclass()** `[059]` (defined in the generated `i2c-internal.h` file), which has several **static_assert()** calls.The class `D` is expected to implement the three member functions (**I2cTransact()**,**I2cGetMaxTransferSize()**, and **I2cGetInterrupt()**) in order for the static methods to work.If they're not provided by `D`, then the compiler would (in the absence of the staticasserts) produce gnarly templating errors.The static asserts serve to produce diagnostic errors that are understandable by mere humans. 构造函数调用内部验证函数** CheckI2cProtocolSubclass（）** [059]（在生成的i2c-internal.h文件中定义），该函数具有多个static_assert（）调用。 D`应该实现三个成员函数（** I2cTransact（）**，** I2cGetMaxTransferSize（）**和** I2cGetInterrupt（）**）以使静态方法起作用。由`D`提供的，则编译器将（在没有静态断言的情况下）产生粗糙的模板错误。静态断言用于产生仅人类可以理解的诊断错误。

Next, the three pointer-to-function operations members (`transact`, `get_max_transfer_size`, and `get_interrupt`) are bound (lines `[060` .. `062]`). 接下来，绑定三个指向函数的指针操作成员（“事务”，“ get_max_transfer_size”和“ get_interrupt”）（“ [060” ..“ 062]”行）。

Finally, the `constexpr` expression provides a default initialization if required.  最后，如果需要，`constexpr`表达式提供默认的初始化。

 
### Using the mixin class  使用mixin类 

The `I2cProtocol` class can be used as follows (from [`//zircon/system/dev/bus/platform/platform-proxy.h`](/zircon/system/dev/bus/platform/platform-proxy.h)): I2cProtocol类可以如下使用（来自[`//zircon/system/dev/bus/platform/platform-proxy.h]](/zircon/system/dev/bus/platform/platform/platform-proxy.h ））：

```c++
[01] class ProxyI2c : public ddk::I2cProtocol<ProxyI2c> {
[02] public:
[03]     explicit ProxyI2c(uint32_t device_id, uint32_t index, fbl::RefPtr<PlatformProxy> proxy)
[04]         : device_id_(device_id), index_(index), proxy_(proxy) {}
[05]
[06]     // I2C protocol implementation.
[07]     void I2cTransact(const i2c_op_t* ops, size_t cnt, i2c_transact_callback transact_cb,
[08]                      void* cookie);
[09]     zx_status_t I2cGetMaxTransferSize(size_t* out_size);
[10]     zx_status_t I2cGetInterrupt(uint32_t flags, zx::interrupt* out_irq);
[11]
[12]     void GetProtocol(i2c_protocol_t* proto) {
[13]         proto->ops = &i2c_protocol_ops_;
[14]         proto->ctx = this;
[15]     }
[16]
[17] private:
[18]     uint32_t device_id_;
[19]     uint32_t index_;
[20]     fbl::RefPtr<PlatformProxy> proxy_;
[21] };
```
 

Here we see that `class ProxyI2c` inherits from the DDK's `I2cProtocol` and provides itself as the argument to the template &mdash; this is the "mixin" concept.This causes the `ProxyI2c` type to be substituted for `D` in the template definitionof the class (from the `i2c.h` header file above, lines `[084]`, `[088]`, and `[093]`). 在这里，我们看到ProxyI2c类是从DDK的I2cProtocol继承而来的，并提供了自己作为模板mdash的参数。这就是“ mixin”的概念。这将导致在类的模板定义中将“ ProxyI2c”类型替换为“ D”（来自上面的“ i2c.h”头文件，第[084]行，第[088]行） ]`和`[093]`）。

Taking a look at just the **I2cGetMaxTransferSize()** function as an example, it's effectively as if the source code read: 以** I2cGetMaxTransferSize（）**函数为例，它就像源代码一样有效地读取：

```c++
[087] static zx_status_t I2cGetMaxTransferSize(void* ctx, size_t* out_size) {
[088]     auto ret = static_cast<ProxyI2c*>(ctx)->I2cGetMaxTransferSize(out_size);
[089]     return ret;
[090] }
```
 

This ends up eliminating the cast-to-self boilerplate in your code. This casting is necessary because the type information is erased at the DDK boundary &mdash;recall that the context `ctx` is a `void *` pointer. 最终消除了代码中的强制转换样板。这种转换是必需的，因为在DDK边界上抹去了类型信息，请记住上下文“ ctx”是“ void *”指针。

 
### Auto-generated comments  自动产生的评论 

Banjo automatically generates comments in the include file that basically summarize what we talked about above: Banjo在包含文件中自动生成注释，这些注释基本上总结了我们上面讨论的内容：

```c++
[020] // DDK i2c-protocol support
[021] //
[022] // :: Proxies ::
[023] //
[024] // ddk::I2cProtocolClient is a simple wrapper around
[025] // i2c_protocol_t. It does not own the pointers passed to it
[026] //
[027] // :: Mixins ::
[028] //
[029] // ddk::I2cProtocol is a mixin class that simplifies writing DDK drivers
[030] // that implement the i2c protocol. It doesn't set the base protocol.
[031] //
[032] // :: Examples ::
[033] //
[034] // // A driver that implements a ZX_PROTOCOL_I2C device.
[035] // class I2cDevice;
[036] // using I2cDeviceType = ddk::Device<I2cDevice, /* ddk mixins */>;
[037] //
[038] // class I2cDevice : public I2cDeviceType,
[039] //                   public ddk::I2cProtocol<I2cDevice> {
[040] //   public:
[041] //     I2cDevice(zx_device_t* parent)
[042] //         : I2cDeviceType(parent) {}
[043] //
[044] //     void I2cTransact(const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie);
[045] //
[046] //     zx_status_t I2cGetMaxTransferSize(size_t* out_size);
[047] //
[048] //     zx_status_t I2cGetInterrupt(uint32_t flags, zx::interrupt* out_irq);
[049] //
[050] //     ...
[051] // };
```
 

 
# Using Banjo  使用班卓琴 

> Suraj says: >> We also need something in-between a FIDL tutorial and a driver writing tutorial,>> in order to describe banjo usage.>> Basically, writing a simple protocol, and then describing a driver that emits>> it, and another driver that binds on top of it and makes use of that protocol.>> If it makes sense, the existing driver writing tutorial could just be modified>> to have more fleshed out details on banjo usage.>> I think the current driver tutorial is focused on C usage as well, and getting>> a C++ version (using ddktl) would probably bring the most value [this is>> already on my work queue, "Tutorial on using ddktl (C++ DDK wrappers)" -RK]. > Suraj说：>>为了描述banjo的用法，我们还需要FIDL教程和驱动程序编写教程之间的>>。基本上，编写一个简单的协议，然后描述发出>>的驱动程序，以及绑定在该协议之上并使用该协议的另一个驱动程序。>>如果有意义，可以对现有的驱动程序编写教程进行修改>>，以更详细地了解班卓琴用法。>>我认为当前的驱动程序教程也专注于C的用法，并且>>获得C ++版本（使用ddktl）可能会带来最大的价值[这已经>>在我的工作队列中，“使用ddktl教程（C ++ DDK包装器）” -RK]。

Now that we've seen the generated code for the I2C driver, let's take a look at how we would use it. 现在，我们已经看到了I2C驱动程序的生成代码，让我们看一下如何使用它。

> @@@ to be completed  > @@@待完成

 
# Reference  参考 

> @@@ This is where we should list all builtin keywords and primitve types  > @@@这是我们应该列出所有内置关键字和原始类型的地方

 
## Attributes  属性 

Recall from the example above that the `protocol` section had two attributes; a `[Layout]` and an `[Async]` attribute. 回顾上面的示例，“ protocol”部分具有两个属性；一个[Layout]和一个[Async]属性。

 
### The Layout attribute  布局属性 

The line just before the `protocol` is the `[Layout]` attribute:  协议之前的那一行是[Layout]属性：

```banjo
[19] [Layout = "ddk-protocol"]
[20] protocol I2c {
```
 

The attribute applies to the next item; so in this case, the entire `protocol`. Only one layout is allowed per interface. 该属性适用于下一项；因此，在这种情况下，整个协议都是如此。每个接口仅允许一种布局。

There are in fact 3 `Layout` attribute types currently supported:  实际上，目前支持3种“布局”属性类型：

 
* `ddk-protocol`  *`ddk-protocol`
* `ddk-interface`  *`ddk-interface`
* `ddk-callback`  *`ddk-callback`

In order to understand how these layout types work, let's assume we have two drivers, `A` and `B`.Driver `A` spawns a device, which `B` then attaches to, (making `B` a child of `A`). 为了理解这些布局类型的工作方式，我们假设我们有两个驱动程序A和B.驱动程序A产生一个设备，然后将设备B附加到设备上（使B成为`的子代。 A`）。

If `B` then queries the DDK for its parent's "protocol" via **device_get_protocol()**, it'll get a `ddk-protocol`.A `ddk-protocol` is a set of callbacks that a parent provides to its child. 如果`B`然后通过** device_get_protocol（）**向DDK查询其父级的“协议”，它将得到一个ddk-protocol。ddk-protocol是父级提供给它的一组回调。它的孩子。

One of the protocol functions can be to register a "reverse-protocol", whereby the child provides a set of callbacks for the parent to trigger instead.This is a `ddk-interface`. 协议功能之一是注册“反向协议”，子代提供一组回调供父代触发。这是一个“ ddk-interface”。

From a code generation perspective, these two (`ddk-protocol` and `ddk-interface`) look almost identical, except for some slight naming differences (`ddk-protocol`automatically appends the word "protocol" to the end of generated structs / classes,whereas `ddk-interface` doesn't). 从代码生成的角度来看，这两者（ddk-protocol和ddk-interface）看起来几乎相同，除了一些微小的命名差异（ddk-protocol自动将单词“ protocol”附加到生成的结构的末尾） /类，而“ ddk-interface”则没有）。

`ddk-callback` is a slight optimization over `ddk-interface`, and is used when an interface has just one single function.Instead of generating two structures, like: ddk-callback是对ddk-interface的略微优化，用于接口仅具有一个功能的情况，而不是生成两个结构，例如：

```c
struct interface {
   void* ctx;
   inteface_function_ptr_table* callbacks;
};

struct interface_function_ptr_table {
   void (*one_function)(...);
}
```
 

a `ddk-callback` will generate a single structure with the function pointer inlined:  一个ddk-callback会生成一个带有内联函数指针的单一结构：

```c
struct callback {
  void* ctx;
  void (*one_function)(...);
};
```
 

 
### The Async attribute  异步属性 

Within the `protocl` section, we see another attribute: the `[Async]` attribute:  在“协议”部分中，我们看到了另一个属性：[[Async]`属性：

```banjo
[20] protocl I2c {
...      /// comments (removed)
[27]     [Async]
```
 

The `[Async]` attribute is a way to make protocol messages not be synchronous. It autogenerates a callback type in which the output arguments are inputs to the callback.The original method will not have any of the output parameters specified in its signatures. “ [Async]”属性是一种使协议消息不同步的方法。它会自动生成一个回调类型，在该类型中将输出参数输入到该回调中。原始方法的签名中将没有指定任何输出参数。

Recall from the example above that we had a `Transact` method:  回想一下上面的示例，我们有一个Transact方法：

```banjo
[27] [Async]
[28] Transact(vector<I2cOp> op) -> (zx.status status, vector<I2cOp> op);
```
 

When used (as above) in conjunction with the `[Async]` attribute, it means that we want Banjo to invoke a callback function, so that we can handle the output data (the second`vector<I2cOp>` above, representing the data from the I2C bus). 与上面的[Async]属性结合使用时，这意味着我们希望Banjo调用回调函数，以便我们可以处理输出数据（上面的第二个vector <I2cOp>代表来自I2C总线的数据）。

Here's how it works. We send data to the I2C bus via the first `vector<I2cOp>` argument.Some time later, the I2C bus may generate data in response to our request.Because we specified `[Async]`, Banjo generates the functions to take a callback functionas input. 运作方式如下。我们通过第一个`vector <I2cOp>`参数将数据发送到I2C总线。一段时间后，I2C总线可能会响应我们的请求生成数据。由于我们指定了[Async]，Banjo生成了将回调函数作为输入。

In C, these two lines (from the `i2c.h` file) are important:  在C语言中，这两行（来自`i2c.h`文件）很重要：

```c
[19] typedef void (*i2c_transact_callback)(void* ctx, zx_status_t status, const i2c_op_t* op_list, size_t op_count);
...
[36] void (*transact)(void* ctx, const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie);
```
 

In C++, we have two place where the callback is referenced:  在C ++中，我们在两个地方引用了回调：

```c++
[083] static void I2cTransact(void* ctx, const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie) {
[084]     static_cast<D*>(ctx)->I2cTransact(op_list, op_count, callback, cookie);
[085] }
```
 

and  和

```c++
[134] void Transact(const i2c_op_t* op_list, size_t op_count, i2c_transact_callback callback, void* cookie) const {
[135]     ops_->transact(ctx_, op_list, op_count, callback, cookie);
[136] }
```
 

Notice how the C++ is similar to the C: that's because the generated code includes the C header file as part of the C++ header file. 请注意，C ++与C：相似，这是因为生成的代码包括C头文件，并将其作为C ++头文件的一部分。

The transaction callback has the following arguments:  事务回调具有以下参数：

Argument   | Meaning -----------|----------------------------------------`ctx`      | the cookie`status`   | status of the asynchronous response (provided by callee)`op_list`  | the data from the transfer`op_count` | the number of elements in the transfer 争论含义----------- || ------------------------------------- --`ctx` | cookie的状态|异步响应的状态（由被调用方提供）来自op_count转移的数据|传输中的元素数

How is this different than just using the `ddk-callback` `[Layout]` attribute we discussed above? 这与仅使用我们上面讨论的`ddk-callback``[Layout]`属性有何不同？

First, there's no `struct` with the callback and cookie value in it, they're inlined as arguments instead. 首先，没有包含回调和cookie值的`struct`，而是将它们作为参数内联。

Second, the callback provided is a "one time use" function. That is to say, it should be called once, and only once, for each invocation of theprotocol method it was supplied to.For contrast, a method provided by a `ddk-callback` is a "register once, callmany times" type of function (similar to `ddk-interface` and `ddk-protocol`).For this reason, `ddk-callback` and `ddk-interface` structures usually havepaired **register()** and **unregister()** calls in order to tell the parent devicewhen it should stop calling those callbacks. 其次，提供的回调是“一次性使用”功能。也就是说，对于每次提供给协议方法的调用，都应该调用一次，并且只能调用一次。相比之下，“ ddk-callback”提供的方法是“注册一次，多次调用”类型的。因此（ddk-callback和ddk-interface结构通常具有配对的** register（）**和** unregister（）**）调用以告知父设备何时应停止调用这些回调。

> One more caveat with `[Async]` is that its callback *MUST* be called for each > protocol method invocation, and the accompanying cookie must be provided.> Failure to do so will result in undefined behavior (likely a leak, deadlock,> timeout, or crash). > [Async]的另一个警告是每次协议方法调用都必须调用其回调*必须*，并且必须提供附带的cookie。>否则将导致不确定的行为（可能是泄漏，死锁，>超时或崩溃）。

Although not the case currently, C++ and future language bindings (like Rust) will provide "future" / "promise" style based APIs in the generated code, built on top ofthese callbacks in order to prevent mistakes. 尽管目前情况并非如此，但C ++和将来的语言绑定（如Rust）将在生成的代码中提供基于“未来” /“承诺”样式的API，这些API建立在这些回调的基础之上，以防止出错。

> Ok, one more caveat with `[Async]` &mdash; the `[Async]` attribute applies *only* > to the immediately following method; not any other methods. >好的，再用[[Async]`mdash告诫； `[Async]`属性仅适用于紧随其后的方法；没有其他方法。

 
# Banjo Mocks  班卓琴 

Banjo generates a C++ mock class for each protocol. This mock can be passed to protocol users in tests. Banjo为每种协议生成一个C ++模拟类。可以在测试中将此模拟传递给协议用户。

 
## Building  建造 

Tests in Zircon get the mock headers automatically. Tests outsize of Zircon must depend on the protocol target with a `_mock` suffix, e.g.`//zircon/public/banjo/ddk.protocol.gpio:ddk.protocol.gpio_mock`. Zircon中的测试会自动获取模拟标头。要测试Zircon的大小，必须取决于带有“ _mock”后缀的协议目标，例如，// zircon / public / banjo / ddk.protocol.gpio：ddk.protocol.gpio_mock。

 
## Using the mocks  使用模拟 

Test code must include the protocol header with a `mock/` prefix, e.g. `#include <mock/ddktl/protocol/gpio.h>`. 测试代码必须包含带有“ mock /”前缀的协议标头，例如包括<mock / ddktl / protocol / gpio.h>。

Consider the following Banjo protocol snippet:  请考虑以下Banjo协议代码段：

```banjo
[021] [Layout = "ddk-protocol"]
[022] protocol Gpio {
 ...
[034]     /// Gets an interrupt object pertaining to a particular GPIO pin.
[035]     GetInterrupt(uint32 flags) -> (zx.status s, handle<interrupt> irq);
 ...
[040] };
```
 

Here are the corresponding bits of the mock class generated by Banjo:  这是Banjo生成的模拟类的相应位：

```c++
[034] class MockGpio : ddk::GpioProtocol<MockGpio> {
[035] public:
[036]     MockGpio() : proto_{&gpio_protocol_ops_, this} {}
[037]
[038]     const gpio_protocol_t* GetProto() const { return &proto_; }
 ...
[065]     virtual MockGpio& ExpectGetInterrupt(zx_status_t out_s, uint32_t flags, zx::interrupt out_irq) {
[066]         mock_get_interrupt_.ExpectCall({out_s, std::move(out_irq)}, flags);
[067]         return *this;
[068]     }
 ...
[080]     void VerifyAndClear() {
 ...
[086]         mock_get_interrupt_.VerifyAndClear();
 ...
[089]     }
 ...
[117]     virtual zx_status_t GpioGetInterrupt(uint32_t flags, zx::interrupt* out_irq) {
[118]         std::tuple<zx_status_t, zx::interrupt> ret = mock_get_interrupt_.Call(flags);
[119]         *out_irq = std::move(std::get<1>(ret));
[120]         return std::get<0>(ret);
[121]     }
```
 

The MockGpio class implements the GPIO protocol. `ExpectGetInterrupt` is used to set expectations on how `GpioGetInterrupt` is called. `GetProto` is used to get the`gpio_protocol_t` that can be passed to the code under test. This code will call `GpioGetInterrupt`which will ensure that it got called with the correct arguments and will return the value specifiedby `ExpectGetInterrupt`. Finally, the test can call `VerifyAndClear` to verify that all expectationswere satisfied. Here is an example test using this mock: MockGpio类实现GPIO协议。 “ ExpectGetInterrupt”用于设置对如何调用“ GpioGetInterrupt”的期望。 GetProto用于获取gpio_protocol_t，该gpio_protocol_t可以传递给被测代码。这段代码将调用`GpioGetInterrupt`，以确保使用正确的参数调用它，并返回`ExpectGetInterrupt`指定的值。最后，测试可以调用“ VerifyAndClear”来验证是否满足所有期望。这是使用此模拟的示例测试：

```c++
TEST(SomeTest, SomeTestCase) {
    ddk::MockGpio gpio;

    zx::interrupt interrupt;
    gpio.ExpectGetInterrupt(ZX_OK, 0, zx::move(interrupt))
        .ExpectGetInterrupt(ZX_ERR_INTERNAL, 100, zx::interrupt());

    CodeUnderTest dut(gpio.GetProto());
    EXPECT_OK(dut.DoSomething());

    ASSERT_NO_FATAL_FAILURES(gpio.VerifyAndClear());
}
```
 

 
### Equality operator overrides  等号运算符覆盖 

Tests using Banjo mocks with structure types will have to define equality operator overrides. For example, for a struct type `some_struct_type` the test will have to define a function with thesignature 使用具有结构类型的Banjo模拟进行的测试必须定义相等运算符覆盖。例如，对于结构类型为“ some_struct_type”的测试，测试将必须定义一个具有签名的函数

```c++
bool operator==(const some_struct_type& lhs, const some_struct_type& rhs);
```
 

in the top-level namespace.  在顶级名称空间中。

 
### Custom mocks  自定义模拟 

It is expected that some tests may need to alter the default mock behavior. To help with this, all expectation and protocol methods are `virtual`, and all `MockFunction` members are `protected`. 预期某些测试可能需要更改默认的模拟行为。为了解决这个问题，所有期望和协议方法都是“虚拟”的，所有“ MockFunction”成员都是“受保护的”。

 
### Async methods  异步方法 

