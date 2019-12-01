 
# C language FIDL tutorial  C语言FIDL教程 

[TOC]  [目录]

 
## About this tutorial  关于本教程 

This tutorial describes how to make client calls and write servers in C using the FIDL InterProcess Communication (**IPC**) system in Fuchsia. 本教程介绍了如何使用紫红色的FIDL InterProcess Communication（** IPC **）系统以C语言进行客户端调用和编写服务器。

Refer to the [main FIDL page](../README.md) for details on the design and implementation of FIDL, as well as the[instructions for getting and building Fuchsia](/docs/getting_started.md). 有关FIDL的设计和实现以及[获取和构建紫红色的说明]（/ docs / getting_started.md）的详细信息，请参见[FIDL主页]（../README.md）。

The [reference](#reference) section documents the bindings.  [reference]（参考）部分记录了绑定。

 
# Getting started  入门 

We'll use the `echo.test.fidl` sample that we discussed in the [FIDL Tutorial](README.md) introduction section, by opening[//garnet/examples/fidl/services/echo.test.fidl](/garnet/examples/fidl/services/echo.test.fidl). 我们将通过打开[//garnet/examples/fidl/services/echo.test.fidl]（在[FIDL教程]（README.md）简介部分中讨论过的`echo.test.fidl`示例）来使用（ /garnet/examples/fidl/services/echo.test.fidl）。

<!-- NOTE: the code snippets here need to be kept up to date manually by copy-pasting from the actual source code. Please update a snippetif you notice it's out of date. --> <！-注意：此处的代码段需要通过从实际源代码中粘贴粘贴来手动保持最新。如果发现片段已过时，请更新。 ->

 

```fidl
library fidl.examples.echo;

[Discoverable]
protocol Echo {
    EchoString(string? value) -> (string? response);
};
```
 

 
## Build  建立 

Use the following steps to build:  使用以下步骤进行构建：

(@@@ to be completed)  （@@@ 要完成的）

 
## `Echo` server  回声服务器 

The example server code is in [//garnet/examples/fidl/echo_server_c/echo_server.c][server]:  示例服务器代码在[//garnet/examples/fidl/echo_server_c/echo_server.c] [服务器]中：

```c
[01] // Copyright 2018 The Fuchsia Authors. All rights reserved.
[02] // Use of this source code is governed by a BSD-style license that can be
[03] // found in the LICENSE file.
[04]
[05] #include <lib/async-loop/loop.h>
[06] #include <lib/fdio/fd.h>
[07] #include <lib/fdio/fdio.h>
[08] #include <lib/fdio/directory.h>
[09] #include <lib/svc/dir.h>
[10] #include <stdio.h>
[11] #include <zircon/process.h>
[12] #include <zircon/processargs.h>
[13] #include <zircon/status.h>
[14] #include <zircon/syscalls.h>
[15]
[16] static void connect(void* context, const char* service_name,
[17]                     zx_handle_t service_request) {
[18]   printf("Incoming connection for %s.\n", service_name);
[19]   // TODO(abarth): Implement echo server once FIDL C bindings are available.
[20]   zx_handle_close(service_request);
[21] }
[22]
[23] int main(int argc, char** argv) {
[24]   zx_handle_t directory_request = zx_take_startup_handle(PA_DIRECTORY_REQUEST);
[25]   if (directory_request == ZX_HANDLE_INVALID) {
[26]     printf("error: directory_request was ZX_HANDLE_INVALID\n");
[27]     return -1;
[28]   }
[29]
[30]   async_loop_t* loop = NULL;
[31]   zx_status_t status =
[32]       async_loop_create(&kAsyncLoopConfigAttachToCurrentThread, &loop);
[33]   if (status != ZX_OK) {
[34]     printf("error: async_loop_create returned: %d (%s)\n", status,
[35]            zx_status_get_string(status));
[36]     return status;
[37]   }
[38]
[39]   async_dispatcher_t* dispatcher = async_loop_get_dispatcher(loop);
[40]
[41]   svc_dir_t* dir = NULL;
[42]   status = svc_dir_create(dispatcher, directory_request, &dir);
[43]   if (status != ZX_OK) {
[44]     printf("error: svc_dir_create returned: %d (%s)\n", status,
[45]            zx_status_get_string(status));
[46]     return status;
[47]   }
[48]
[49]   status = svc_dir_add_service(dir, "public", "fidl.examples.echo.Echo", NULL, connect);
[50]   if (status != ZX_OK) {
[51]     printf("error: svc_dir_add_service returned: %d (%s)\n", status,
[52]            zx_status_get_string(status));
[53]     return status;
[54]   }
[55]
[56]   status = async_loop_run(loop, ZX_TIME_INFINITE, false);
[57]   if (status != ZX_OK) {
[58]     printf("error: async_loop_run returned: %d (%s)\n", status,
[59]            zx_status_get_string(status));
[60]     return status;
[61]   }
[62]
[63]   svc_dir_destroy(dir);
[64]   async_loop_destroy(loop);
[65]
[66]   return 0;
[67] }
```
 

 
### main()  主要（） 

**main()**:  **主要（）**：

 
1. creates a startup handle (`[24` .. `28]`),  1.创建一个启动句柄（[[24` ..`28]`），
2. initializes the asynchronous loop (`[30` .. `37]`),  2.初始化异步循环（`[30`..`37]`），
3. adds the **connect()** function to handle the echo service (`[49]`), and finally 3.添加** connect（）**函数来处理回显服务（`[49]`），最后
4. runs the asychronous loop in the foreground via **async_loop_run()** (`[56]`). 4.通过** async_loop_run（）**（`[56]`）在前台运行异步循环。

When the async loop returns, we clean up (`[63]` and `[64]`) and exit.  当异步循环返回时，我们清理（“ [63]”和“ [64]”）并退出。

 
### connect()  connect（） 

> The **connect()** function is waiting for `abarth` to implement it (`[19]`) :-)  > ** connect（）**函数正在等待`abarth`来实现它（`[19]`）:-)

 
## `Echo` client  回声客户端 

(@@@ to be completed)  （@@@ 要完成的）

 
# Reference  参考 

This section describes the FIDL implementation for C, including the libraries and code generator. 本节介绍C的FIDL实现，包括库和代码生成器。

Consult the [C Family Comparison](c-family-comparison.md) document for an overview of the similarities and differences between the C and C++ bindings. 请查阅[C系列比较]（c-family-comparison.md）文档，以概述C和C ++绑定之间的相似之处和不同之处。

 
## Design  设计 

 
### Goals  目标 

 
 * Support encoding and decoding FIDL objects with C11.  *支持使用C11编码和解码FIDL对象。
 * Generate headers which are compatible with C11 and C++14.  *生成与C11和C ++ 14兼容的标头。
 * Small, fast, efficient.  *小型，快速，高效。
 * Depend only on a small subset of the standard library.  *仅取决于标准库的一小部分。
 * Minimize code expansion through table-driven encoding and decoding.  *通过表驱动的编码和解码最大程度地减少代码扩展。
 * Support two usage styles: raw and simple.  *支持两种用法：原始和简单。

 
### Raw Usage Style  原始用法样式 

 
 * Optimized to meet the needs of low-level systems programming.  *经过优化以满足底层系统编程的需求。
 * Represent data structures whose memory layout coincides with the wire format.  *表示其内存布局与连线格式一致的数据结构。
 * Support in-place access and construction of FIDL objects.  *支持就地访问和FIDL对象的构造。
 * Defer all memory allocation decisions to the client.  *将所有内存分配决策推迟到客户端。
 * Code generator only produces type declarations, data tables, and simple inline functions.  *代码生成器仅生成类型声明，数据表和简单的内联函数。
 * Client is fully responsible for dispatching incoming method calls on protocols (write their own switch statement and invoke argument decodefunctions). *客户端完全负责在协议上分派传入的方法调用（编写自己的switch语句并调用参数解码功能）。

 
### Simple Usage Style  简单用法 

 
 * Optimized to meet the needs of driver developers.  *经过优化，可以满足驱动程序开发人员的需求。
 * Supports only a simple subset of the FIDL language.  *仅支持FIDL语言的简单子集。
 * Represent data structures whose memory layout coincides with the wire format.  *表示其内存布局与连线格式一致的数据结构。
 * Defer all memory allocation decisions to the client.  *将所有内存分配决策推迟到客户端。
 * Code generator produces simple C functions for sending, receiving, and dispatching messages. 代码生成器产生简单的C函数，用于发送，接收和调度消息。

 
### Encoding Tables  编码表 

To avoid generating any non-inline code whatsoever, the C language bindings instead produce encoding tables which describe how objects are encoded. 为了避免生成任何非内联代码，C语言绑定将生成描述对象编码方式的编码表。

 
### Introspection Tables  内省表 

To allow for objects to be introspected (eg. printed), the C language bindings produce introspection tables which describe the name and type signature of eachmethod of each protocol and data structure. 为了允许对对象进行自省（例如打印），C语言绑定会产生自省表，这些表描述了每种协议和数据结构的每种方法的名称和类型签名。

Although small, introspection tables will be stripped out by the linker if unused. 尽管内省表很小，但是如果未使用，则链接器会删除它。

 
### Mapping FIDL Types to C Types  将FIDL类型映射到C类型 

This is the mapping from FIDL types to C types which the code generator produces. 这是代码生成器生成的从FIDL类型到C类型的映射。

| FIDL                                           | C Type                     | |------------------------------------------------|----------------------------|| `bits`                                         | typedef to underlying type || `bool`                                         | `bool`                     || `int8`                                         | `int8_t`                   || `uint8`                                        | `uint8_t`                  || `int16`                                        | `int16_t`                  || `uint16`                                       | `uint16_t`                 || `int32`                                        | `int32_t`                  || `uint32`                                       | `uint32_t`                 || `int64`                                        | `int64_t`                  || `uint64`                                       | `uint64_t`                 || `float32`                                      | `float`                    || `float64`                                      | `double`                   || `handle`, `handle?`, `handle<T>`, `handle<T>?` | `zx_handle_t`              || `string`, `string?`                            | `fidl_string_t`            || `vector`, `vector?`                            | `fidl_vector_t`            || `array<T>:N`                                   | `T[N]`                     || `protocol`, `protocol?`                        | typedef to `zx_handle_t`   || `request<I>`, `request<I>?`                    | typedef to `zx_handle_t`   || `struct`                                       | `struct Struct`            || `struct?`                                      | `struct Struct*`           || `union`                                        | `struct Union`             || `union?`                                       | `struct Union*`            || `xunion`                                       | (not yet supported)        || `xunion?`                                      | (not yet supported)        || `table`                                        | (not yet supported)        || `enum`                                         | typedef to underlying type | | FIDL | C型| | ------------------------------------------------ | ---------------------------- ||位|将typedef转换为基础类型|| `bool` | `bool` || `int8` | `int8_t` || `uint8` | `uint8_t` || `int16` | `int16_t` || `uint16` | `uint16_t` || `int32` | `int32_t` || `uint32` | `uint32_t` || `int64` | `int64_t` || `uint64` | `uint64_t` || `float32` | `float` || `float64` | `double` || `handle`，`handle？`，`handle <T>`，`handle <T>？`| `zx_handle_t` || `string`，`string？`| `fidl_string_t` || `vector`，`vector？`| `fidl_vector_t` || `array <T>：N` | `T [N]`|| `protocol`，`protocol？将typedef设为`zx_handle_t` || `request <I>`，`request <I>？`|将typedef设为`zx_handle_t` || `struct` | `struct Struct` || `struct？`| `struct Struct *`|| `联合`| `struct Union` ||联盟？ `struct Union *`|| `xunion` | （尚不支持）|| “ xunion？” | （尚不支持）|| `table` | （尚不支持）|| `枚举`|从typedef到基础类型|

 
## zircon/fidl.h  锆石/fidl.h 

The `zircon/fidl.h` header defines the basic constructs of the FIDL wire format. The header is part of the Zircon system headers and depends only on other Zirconsystem headers and a small portion of the C standard library. zircon / fidl.h标头定义了FIDL有线格式的基本结构。标头是Zircon系统标头的一部分，并且仅取决于其他Zirconsystem标头和C标准库的一小部分。

 
### fidl_message_header_t  fidl_message_header_t 

```c
typedef struct fidl_message_header {
    zx_txid_t txid;
    uint32_t reserved0;
    uint32_t flags;
    uint32_t ordinal;
} fidl_message_header_t;
```
 

Defines the initial part of every FIDL message sent over a channel. The header is immediately followed by the body of the payload. Currently, there are noflags to be set, and so `flags` must be zero. 定义通过通道发送的每个FIDL消息的初始部分。标头后紧跟有效内容的主体。当前，没有标志可以设置，因此“标志”必须为零。

 
### fidl_string_t  fidl_string_t 

```c
typedef struct fidl_string {
    // Number of UTF-8 code units (bytes), must be 0 if |data| is null.
    uint64_t size;

    // Pointer to UTF-8 code units (bytes) or null
    char* data;
} fidl_string_t;
```
 

Holds a reference to a variable-length string.  保存对可变长度字符串的引用。

When decoded, **data** points to the location within the buffer where the string content lives, or **NULL** if the reference is null. 解码时，** data **指向缓冲区中字符串内容所在的位置；如果引用为null，则指向NULL。

When encoded, **data** is replaced by **FIDL_ALLOC_PRESENT** when the reference is non-null or **FIDL_ALLOC_ABSENT** when the reference is null. The location ofthe string's content is determined by the depth-first traversal order of themessage during decoding. 编码后，当引用为非空时，数据被** FIDL_ALLOC_PRESENT **替换；当引用为空时，** FIDL_ALLOC_ABSENT **。字符串内容的位置由解码期间消息的深度优先遍历顺序确定。

 
### fidl_vector_t  fidl_vector_t 

```c
typedef struct fidl_vector {
    // Number of elements, must be 0 if |data| is null.
    uint64_t count;

    // Pointer to element data or null.
    void* data;
} fidl_vector_t;
```
 

Holds a reference to a variable-length vector of elements.  保存对元素的可变长度向量的引用。

When decoded, **data** points to the location within the buffer where the elements live, or **NULL** if the reference is null. 解码时，** data **指向元素所在的缓冲区中的位置；如果引用为null，则指向NULL。

When encoded, **data** is replaced by **FIDL_ALLOC_PRESENT** when the reference is non-null or **FIDL_ALLOC_ABSENT** when the reference is null. The location ofthe vector's content is determined by the depth-first traversal order of themessage during decoding. 编码后，当引用为非空时，数据被** FIDL_ALLOC_PRESENT **替换；当引用为空时，** FIDL_ALLOC_ABSENT **。向量内容的位置由解码期间消息的深度优先遍历顺序确定。

 
### fidl_msg_t  fidl_msg_t 

```c
typedef struct fidl_msg {
    // The bytes of the message.
    //
    // The bytes of the message might be in the encoded or decoded form.
    // Functions that take a |fidl_msg_t| as an argument should document whether
    // the expect encoded or decoded messages.
    //
    // See |num_bytes| for the number of bytes in the message.
    void* bytes;

    // The handles of the message.
    //
    // See |num_bytes| for the number of bytes in the message.
    zx_handle_t* handles;

    // The number of bytes in |bytes|.
    uint32_t num_bytes;

    // The number of handles in |handles|.
    uint32_t num_handles;
} fidl_msg_t;
```
 

Represents a FIDL message, including both `bytes` and `handles`. The message might be in the encoded or decoded format. The ownership semantics for thememory referred to by `bytes` and `handles` is defined by the context in whichthe `fidl_msg_t` struct is used. 表示FIDL消息，包括“ bytes”和“ handles”。该消息可能采用编码或解码格式。由“字节”和“句柄”引用的主题的所有权语义是由使用“ fidl_msg_t”结构的上下文定义的。

 
### fidl_txn_t  fidl_txn_t 

```c
typedef struct fidl_txn fidl_txn_t;
struct fidl_txn {
    // Replies to the outstanding request and complete the FIDL transaction.
    //
    // Pass the |fidl_txn_t| object itself as the first paramter. The |msg|
    // should already be encoded. This function always consumes any handles
    // present in |msg|.
    //
    // Call |reply| only once for each |txn| object. After |reply| returns, the
    // |txn| object is considered invalid and might have been freed or reused
    // for another purpose.
    zx_status_t (*reply)(fidl_txn_t* txn, const fidl_msg_t* msg);
};
```
 

Represents a outstanding FIDL transaction that requires a reply. Used by the simple C bindings to route replies to the correct transaction on the correctchannel. 代表需要答复的未完成FIDL交易。由简单的C绑定用于将答复路由到正确通道上的正确事务。

 
## Raw Bindings  原始绑定 

 
### fidl_encode / fidl_encode_msg  fidl_encode / fidl_encode_msg 

```c
zx_status_t fidl_encode(const fidl_type_t* type, void* bytes, uint32_t num_bytes,
                        zx_handle_t* handles, uint32_t max_handles,
                        uint32_t* out_actual_handles, const char** out_error_msg);
zx_status_t fidl_encode_msg(const fidl_type_t* type, fidl_msg_t* msg,
                            uint32_t* out_actual_handles, const char** out_error_msg);
```
 

Declared in [lib/fidl/coding.h](/zircon/system/ulib/fidl/include/lib/fidl/coding.h),defined in[encoding.cc](/zircon/system/ulib/fidl/encoding.cc). 在[lib / fidl / coding.h]（/ zircon / system / ulib / fidl / include / lib / fidl / coding.h）中声明，在[encoding.cc]（/ zircon / system / ulib / fidl / encoding中定义.cc）。

Encodes and validates exactly **num_bytes** of the object in **bytes** in-place by performing a depth-first traversal of the encoding data from **type**to fix up internal references. Replaces internal pointers references with`FIDL_ALLOC_ABSENT` or `FIDL_ALLOC_PRESENT` to indicate presence.Extracts non-zero internal handle references out of **bytes**, stores up to**max_handles** of them sequentially in **handles**, and replaces their locationin **bytes** with `FIDL_HANDLE_PRESENT` to indicate their presence. Sets**out_actual_handles** to the number of handles stored in **handles**. 通过执行来自“类型”的编码数据的深度优先遍历以固定内部引用，以就地“字节”形式对对象的精确“ num_bytes”进行编码和验证。用FIDL_ALLOC_ABSENT或FIDL_ALLOC_PRESENT替换内部指针引用以指示存在状态。从**字节中提取非零内部句柄引用，在** handles **中依次存储最多** max_handles **个，并用FIDL_HANDLE_PRESENT替换它们在**字节中的位置以表示它们的存在。将** out_actual_handles **设置为** handles **中存储的句柄数。

To prevent handle leakage, this operation ensures that either all handles within **bytes** are moved into **handles** in case of success or they are all closed incase of an error. 为防止句柄泄漏，此操作可确保在成功的情况下将“字节”内的所有句柄都移入“句柄”中，或者在出现错误的情况下将它们全部关闭。

If a recoverable error occurs, such as encountering a null pointer for a required sub-object, **bytes** remains in an unusable partially modified state. 如果发生可恢复的错误，例如遇到所需子对象的空指针，则** bytes **保持不可用的部分修改状态。

All handles in **bytes** which were already been consumed up to the point of the error are closed and **out_actual_handles** is set to zero. Depth-first traversal ofthe object then continues to completion, closing all remaining handles in **bytes**. 关闭所有已消耗到错误点的字节（字节）句柄，并将out_actual_handles **设置为零。然后，对象的深度优先遍历将继续完成，关闭所有剩余句柄（以字节为单位）。

If an unrecoverable error occurs, such as exceeding the bound of the buffer, exceeding the maximum nested complex object recursion depth, encounteringinvalid encoding table data, or a dangling pointer, the behavior is undefined. 如果发生不可恢复的错误（例如，超出缓冲区的界限，超过最大的嵌套复杂对象递归深度），遇到无效的编码表数据或悬空指针，则该行为是不确定的。

On success, **bytes** and **handles** describe an encoded object ready to be sent using `zx_channel_send()`. 成功的时候，“字节”和“句柄”描述了一个准备好使用zx_channel_send（）发送的编码对象。

If anything other than `ZX_OK` is returned, **error_msg_out** will be set.  如果返回的内容不是ZX_OK，则将设置error_msg_out。

Result is...  结果是...

 
*   `ZX_OK`: success  *`ZX_OK`：成功
*   `ZX_ERR_INVALID_ARGS`:  *`ZX_ERR_INVALID_ARGS`：
    *   **type** is null  * **类型**为空
    *   **bytes** is null  * **字节**为空
    *   **actual_handles_out** is null  * ** actual_handles_out **为空
    *   **handles** is null and **max_handles** != 0  * ** handles **为空并且** max_handles **！= 0
    *   **type** is not a FIDL struct  * **类型**不是FIDL结构
    *   there are more than **max_handles** in **bytes**  * **个字节中的** max_handles **个以上**
    *   the total length of the object in **bytes** determined by the traversal does not equal precisely **num_bytes** *由遍历确定的对象的总长度（以字节为单位）与num_bytes（精确度）不完全相等
    *   **bytes** contains an invalid union field, according to **type**  * **字节**包含无效的联合字段，根据**类型**
    *   a required pointer reference in **bytes** was null  *以**字节为单位的必需指针引用为空
    *   a required handle reference in **bytes** was `ZX_HANDLE_INVALID`  *必需的句柄引用（以“字节”为单位）为`ZX_HANDLE_INVALID`
    *   a bounded string or vector in **bytes** is too large, according to **type** *根据** type **类型，以**字节为单位的有界字符串或向量太大。
    *   a pointer reference in **bytes** does not have the expected value according to the traversal *根据遍历，以字节为单位的指针引用没有预期值
    *   `FIDL_RECURSION_DEPTH` was exceeded (see [wire format](../reference/wire-format/README.md)) *超过了FIDL_RECURSION_DEPTH（请参阅[有线格式]（../ reference / wire-format / README.md））

This function is effectively a simple interpreter of the contents of the type. Unless the object encoding includes internal references whichmust be fixed up, the only work amounts to checking the object size and theranges of data types such as enums and union tags. 此功能实际上是类型内容的简单解释器。除非对象编码包含必须固定的内部引用，否则唯一的工作就是检查对象大小和数据类型（例如枚举和联合标记）的范围。

 
### fidl_decode / fidl_decode_msg  fidl_decode / fidl_decode_msg 

```c
zx_status_t fidl_decode(const fidl_type_t* type, void* bytes, uint32_t num_bytes,
                        const zx_handle_t* handles, uint32_t num_handles,
                        const char** error_msg_out);
zx_status_t fidl_decode_msg(const fidl_type_t* type, fidl_msg_t* msg,
                            const char** out_error_msg);
```
 

Declared in [lib/fidl/coding.h](/zircon/system/ulib/fidl/include/lib/fidl/coding.h),defined in[decoding.cc](/zircon/system/ulib/fidl/decoding.cc). 在[lib / fidl / coding.h]（/ zircon / system / ulib / fidl / include / lib / fidl / coding.h）中声明，在[decoding.cc]（/ zircon / system / ulib / fidl / decoding中定义.cc）。

Decodes and validates the object in **bytes** in-place by performing a depth-first traversal of the encoding data from **type** to fix up internalreferences. Patches internal pointers within **bytes** whose value is`FIDL_ALLOC_PRESENT` to refer to the address of the out-of-line data theyreference later in the buffer. Populates internal handles within **bytes**whose value is `FIDL_HANDLE_PRESENT` to their corresponding handle takensequentially from **handles**. 通过执行来自** type **的编码数据的深度优先遍历以固定内部引用，就地解码并验证** bytes **中的对象。在“字节”内修补内部指针，其内部值为“ FIDL_ALLOC_PRESENT”，以引用其稍后在缓冲区中引用的离线数据的地址。将内部句柄（其值为FIDL_HANDLE_PRESENT）填充到它们从** handle **依次获取的相应句柄中。

To prevent handle leakage, this operation ensures that either all handles in **handles** from **handles[0]** to **handles[num_handles - 1]** are moved into**bytes** in case of success or they are all closed in case of an error. 为防止句柄泄漏，此操作可确保将** handles **中的所有句柄从** handles [0] **到** handles [num_handles-1] **中的任何一个都成功移入字节**中或在发生错误时将它们全部关闭。

The **handles** array is not modified by the operation.  ** handles **数组未被该操作修改。

If a recoverable error occurs, a result is returned, **bytes** remains in an unusable partially modified state, and all handles in **handles** are closed. 如果发生可恢复的错误，则返回结果，**字节**保持不可使用的部分修改状态，并且**句柄**中的所有句柄都将关闭。

If an unrecoverable error occurs, such as encountering an invalid **type**, the behavior is undefined. 如果发生不可恢复的错误，例如遇到无效的**类型**，则该行为是不确定的。

If anything other than `ZX_OK` is returned, **error_msg_out** will be set.  如果返回的内容不是ZX_OK，则将设置error_msg_out。

Result is...  结果是...

 
*   `ZX_OK`: success  *`ZX_OK`：成功
*   `ZX_ERR_INVALID_ARGS`:  *`ZX_ERR_INVALID_ARGS`：
    *   **type** is null  * **类型**为空
    *   **bytes** is null  * **字节**为空
    *   **handles** is null but **num_handles** != 0.  * ** handles **为空，但** num_handles **！= 0。
    *   **handles** is null but **bytes** contained at least one valid handle reference * ** handles **为空，但** bytes **至少包含一个有效的句柄引用
    *   **type** is not a FIDL struct  * **类型**不是FIDL结构
    *   the total length of the object determined by the traversal does not equal precisely **num_bytes** *由遍历确定的对象的总长度不完全相等** num_bytes **
    *   the total number of handles determined by the traversal does not equal precisely **num_handles** *由遍历确定的句柄总数与num_handles不完全相等
    *   **bytes** contains an invalid union field, according to **type**  * **字节**包含无效的联合字段，根据**类型**
    *   a required pointer reference in **bytes** is `FIDL_ALLOC_ABSENT`.  *以字节为单位的必需指针引用是FIDL_ALLOC_ABSENT。
    *   a required handle reference in **bytes** is `ZX_HANDLE_INVALID`.  *必需的句柄引用（以字节为单位）为ZX_HANDLE_INVALID。
    *   **bytes** contains an optional pointer reference which is marked as `FIDL_ALLOC_ABSENT` but has size > 0. * **字节**包含一个可选的指针引用，该引用被标记为“ FIDL_ALLOC_ABSENT”，但大小大于0。
    *   a bounded string or vector in **bytes** is too large, according to **type** *根据** type **类型，以**字节为单位的有界字符串或向量太大。
    *   a pointer reference in **bytes** has a value other than `FIDL_ALLOC_ABSENT` or `FIDL_ALLOC_PRESENT`. *以“字节”为单位的指针引用具有“ FIDL_ALLOC_ABSENT”或“ FIDL_ALLOC_PRESENT”以外的值。
    *   a handle reference in **bytes** has a value other than `ZX_HANDLE_INVALID` or `FIDL_HANDLE_PRESENT`. *句柄引用（以字节为单位）的值不是ZX_HANDLE_INVALID或FIDL_HANDLE_PRESENT。
    *   `FIDL_RECURSION_DEPTH` was exceeded (see [wire format](../reference/wire-format/README.md)) *超过了FIDL_RECURSION_DEPTH（请参阅[有线格式]（../ reference / wire-format / README.md））

This function is effectively a simple interpreter of the contents of the type. Unless the object encoding includes internal references whichmust be fixed up, the only work amounts to checking the object size and theranges of data types such as enums and union tags. 此功能实际上是类型内容的简单解释器。除非对象编码包含必须固定的内部引用，否则唯一的工作就是检查对象大小和数据类型（例如枚举和联合标记）的范围。

 
### fidl_validate  fidl_validate 

```c
zx_status_t fidl_validate(const fidl_type_t* type, const void* bytes, uint32_t num_bytes,
                          uint32_t num_handles, const char** error_msg_out);
zx_status_t fidl_validate_msg(const fidl_type_t* type, const fidl_msg_t* msg,
                              const char** out_error_msg);
```
 

Declared in [system/ulib/fidl/include/lib/fidl/coding.h](/zircon/system/ulib/fidl/include/lib/fidl/coding.h),defined in[system/ulib/fidl/validating.cc](/zircon/system/ulib/fidl/validating.cc). 在[system / ulib / fidl / include / lib / fidl / coding.h]中声明（/zircon/system/ulib/fidl/include/lib/fidl/coding.h），在[system / ulib / fidl / validating中定义.cc]（/ zircon / system / ulib / fidl / validating.cc）。

Validates the object in **bytes** in-place by performing a depth-first traversal of the encoding data from **type** to fix up internalreferences. This performs the same validation as **fidl_decode()**, butdoes not modify any passed-in data. 通过执行来自** type **的编码数据的深度优先遍历以固定内部引用，就地验证** bytes **中的对象。这执行与** fidl_decode（）**相同的验证，但是不修改任何传入的数据。

The **bytes** buffer is not modified by the operation.  该操作未修改“字节”缓冲区。

If anything other than `ZX_OK` is returned, **error_msg_out** will be set.  如果返回的内容不是ZX_OK，则将设置error_msg_out。

Result is the same as for **fidl_encode()** above.  结果与上面的** fidl_encode（）**相同。

This function is effectively a simple interpreter of the contents of the type. Unless the object encoding includes internal references whichmust be fixed up, the only work amounts to checking the object size and theranges of data types such as enums and union tags. 此功能实际上是类型内容的简单解释器。除非对象编码包含必须固定的内部引用，否则唯一的工作就是检查对象大小和数据类型（例如枚举和联合标记）的范围。

 
### fidl_epitaph_write  fidl_epitaph_write 

```c
zx_status_t fidl_epitaph_write(zx_handle_t channel, zx_status_t error);
```
 

Declared in [lib/fidl/epitaph.h](/zircon/system/ulib/fidl/include/lib/fidl/epitaph.h),defined in[epitaph.c](/zircon/system/ulib/fidl/epitaph.c). 在[lib / fidl / epitaph.h]（/ zircon / system / ulib / fidl / include / lib / fidl / epitaph.h）中声明，在[epitaph.c]（/ zircon / system / ulib / fidl / epitaph中定义。C）。

This function sends an epitaph with the given error number down the given channel.  An epitaph is a special message, with ordinal 0xFFFFFFFF, whichcontains an error code.  The epitaph must be the last thing sent down thechannel before it is closed. 此功能在给定通道下发送带有给定错误编号的墓志铭。墓志铭是一条特殊消息，顺序为0xFFFFFFFF，其中包含错误代码。墓志铭必须是在关闭之前沿通道发送的最后一件事。

 
### Sending Messages  传送讯息 

The client performs the following operations to send a message through a channel. 客户端执行以下操作以通过通道发送消息。

 
*   Obtain a buffer large enough to hold the entire message.  *获得足够大的缓冲区以容纳整个消息。
*   Write the message header into the buffer, which includes the transaction id and method ordinal. *将消息标头写入缓冲区，其中包含事务ID和方法序数。
*   Write the message body into the buffer, which includes the method arguments and any secondary objects (see[wire format](../reference/wire-format/README.md)for a definition of secondary objects). *将消息主体写入缓冲区，其中包括方法参数和任何辅助对象（有关辅助对象的定义，请参见[wire format]（../ reference / wire-format / README.md））。
*   Call **fidl_encode()** to encode the message and handles for transfer, taking care to pass a pointer to the **encoding table** of themessage. *调用** fidl_encode（）**来编码消息和传输句柄，注意将指针传递给主题的**编码表**。
*   Call **zx_channel_write()** to send the message buffer and its associated handles. *调用** zx_channel_write（）**发送消息缓冲区及其关联的句柄。
*   Discard or reuse the buffer. (No need to release handles since they were transferred.) *丢弃或重新使用缓冲区。 （由于手柄已转移，因此无需释放手柄。）

For especially simple messages, it may be possible to skip the encoding step altogether (or do it manually). 对于特别简单的消息，可能会完全跳过编码步骤（或手动执行）。

 
### Receiving Messages  接收讯息 

The client performs the following operations to receive a message through a channel. 客户端执行以下操作以通过通道接收消息。

 
*   Obtain a buffer large enough to hold the largest possible message which can be received by this protocol. (May dynamically allocate the buffer aftergetting the incoming message size from the channel.) *获得足够大的缓冲区以容纳该协议可以接收的最大可能消息。 （在从通道中获取传入消息的大小之后，可以动态分配缓冲区。）
*   Call **zx_channel_read()** to read the message into the buffer and its associated handles. *调用** zx_channel_read（）**将消息读入缓冲区及其关联的句柄。
*   Dispatch the message based on the method ordinal stored in the message header. If the message is invalid, close the handles and skip to the laststep. *根据存储在消息头中的方法序号发送消息。如果消息无效，请关闭句柄并跳至最后一步。
*   Call **fidl_decode()** to decode and validate the message and handles for access, taking care to pass a pointer to the **encoding table** of themessage. *调用** fidl_decode（）**来解码和验证消息以及用于访问的句柄，注意将指针传递给主题的**编码表**。
*   If the message is invalid, skip to last step. (No need to release handles since they will be closed automatically by the decoder.) *如果消息无效，请跳至最后一步。 （无需释放句柄，因为它们将被解码器自动关闭。）
*   Consume the message.  *消费信息。
*   Discard or reuse the buffer.  *丢弃或重新使用缓冲区。

For especially simple messages, it may be possible to skip the encoding step altogether (or do it manually). 对于特别简单的消息，可能会完全跳过编码步骤（或手动执行）。

 
### Closing Channels  关闭频道 

The C language bindings do not provide any special affordances for closing channels.  Per the FIDL specification, an epitaph must be sent as the lastmessage prior to closing a channel.  Code should call **fidl_epitaph_write()**prior to closing a channel. C语言绑定没有为关闭频道提供任何特殊功能。根据FIDL规范，必须在关闭通道之前将墓志作为最后消息发送。在关闭通道之前，代码应调用** fidl_epitaph_write（）**。

 
### Dispatching Messages  派发消息 

The C language bindings do not provide any special affordances for dispatching protocol method calls. The client should dispatch manually based on theprotocol method ordinal, such as by using a **switch** statement. C语言绑定没有为分发协议方法调用提供任何特殊功能。客户端应基于协议方法的序号手动调度，例如使用** switch **语句。

 
## Simple Bindings  简单绑定 

The simple C bindings provide easy-to-use C bindings for a subset of the FIDL language. 简单的C绑定为FIDL语言的子集提供了易于使用的C绑定。

 
### Simple Layout  简单的布局 

In order to generate simple C bindings for a protocol, the protocol must have the `[Layout="Simple"]` attribute. This attribute enforces that the protocol,including the types referenced by it, conform to the language subsetsupported by FIDL. 为了为协议生成简单的C绑定，协议必须具有`[Layout =“ Simple”]`属性。此属性强制协议（包括其引用的类型）符合FIDL支持的语言子集。

Specifically, every message in the protocol (including both requests and response) must not have any secondary objects except strings and vectors ofhandles or primitives (see[wire format](../reference/wire-format/README.md)for a definition of secondary objects). This invariant simplifies the memoryownership semantics. Additionally, all strings and vectors must have explicitnon-maximal length bounds. `vector<int64>:64` is a vector with such a bound, while`vector<int64>` lacks an explicit non-maximal bound. This requirement simplifiesbuffer management for clients that receive these values. 具体来说，协议中的每个消息（包括请求和响应）都不得具有任何次要对象，但句柄或原语的字符串和向量除外（有关定义，请参见[有线格式]（../ reference / wire-format / README.md）第二对象）。该不变性简化了存储器所有权的语义。此外，所有字符串和向量必须具有明确的非最大长度范围。 vector <int64>：64`是具有这样的界限的向量，而`vector <int64>`缺乏明确的非最大界限。此要求简化了接收这些值的客户端的缓冲区管理。

For example, structs and unions can embed other structs and unions, but they cannot contain nullable references to other structs or unions because nullablestructs and unions are stored out-of-line in secondary objects. Nullable handlesand protocols are allowed because they're stored inline as `ZX_HANDLE_INVALID`. 例如，结构和联合可以嵌入其他结构和联合，但是它们不能包含对其他结构或联合的可空引用，因为可空结构和联合离线存储在辅助对象中。允许使用空句柄和协议，因为它们以ZX_HANDLE_INVALID内联存储。

Below is an example of a protocol that meets these requirements:  以下是满足这些要求的协议示例：

```fidl
library unn.fleet;

struct SolarPosition {
    array<int64>:3 coord;
};

enum Alert {
    GREEN = 1;
    YELLOW = 2;
    RED = 3;
};

[Layout="Simple"]
protocol SpaceShip {
    AdjustHeading(SolarPosition destination) -> (int8 result);
    ScanForLifeforms() -> (vector<uint32>:64 life_signs);
    SetDefenseCondition(Alert alert);
};
```
 

 
### Client  客户 

For clients, the simple C bindings generate a function for each method that takes a channel as its first parameter. These functions are safe to use from anythread and do not require any coordination: 对于客户端，简单的C绑定会为每个方法生成一个以通道为第一个参数的函数。这些函数可从任何线程安全使用，并且不需要任何协调：

```c
zx_status_t unn_fleet_SpaceShipSetDefenseCondition(
    zx_handle_t channel,
    const unn_fleet_Alert* alert);
```
 

If the method has a response, the generated function will wait synchronously for the server to reply. If the response contains any data, the data is returned tothe caller through out parameters: 如果该方法有响应，则生成的函数将同步等待服务器答复。如果响应中包含任何数据，则数据将通过out参数返回给调用方：

```c
zx_status_t unn_fleet_SpaceShipAdjustHeading(
    zx_handle_t channel,
    const unn_fleet_SolarPosition* destination,
    int8_t* result);
```
 

The `zx_status_t` returned by these functions indicates whether the transport was successful. Protocol-level status is communicated through out parameters. 这些函数返回的`zx_status_t`表示传输是否成功。协议级别状态通过out参数传达。

 
### Server  服务器 

For servers, the simple C bindings generate an ops table that contains a function pointer for every method in the protocol and a dispatch method thatdecodes the `fidl_msg_t` and calls the appropriate function pointer: 对于服务器，简单的C绑定会生成一个ops表，该表包含协议中每个方法的函数指针和一个对`fidl_msg_t`进行解码并调用适当的函数指针的调度方法：

```c
typedef struct unn_fleet_SpaceShip_ops {
    zx_status_t (*AdjustHeading)(void* ctx,
                                 const unn_fleet_SolarPosition* destination,
                                 fidl_txn_t* txn);
    zx_status_t (*ScanForLifeforms)(void* ctx, fidl_txn_t* txn);
    zx_status_t (*SetDefenseCondition)(void* ctx, const unn_fleet_Alert* alert);
} unn_fleet_SpaceShip_ops_t;

zx_status_t unn_fleet_SpaceShip_dispatch(
    void* ctx,
    fidl_txn_t* txn,
    fidl_msg_t* msg,
    const unn_fleet_SpaceShip_ops_t* ops);
```
 

The `ctx` parameter is an opaque parameter that is passed through the dispatch function to the appropriate function pointer. You can use the `ctx` parameter topass contextual information to the method implementations. ctx参数是一个不透明的参数，它通过分派函数传递给适当的函数指针。您可以使用`ctx`参数将上下文信息传递给方法实现。

The `txn` parameter is passed through the dispatch function to function pointers for methods that have responses. To reply to a message, the implementation ofthat method should call the appropriate reply function: txn参数通过调度功能传递给具有响应的方法的函数指针。要回复消息，该方法的实现应调用相应的回复函数：

```c
zx_status_t unn_fleet_SpaceShipScanForLifeforms_reply(
    fidl_txn_t* txn,
    const uint32_t* life_signs_data,
    size_t life_signs_count);
```
 

For example, `ScanForLifeforms` might be implemented as follows:  例如，`ScanForLifeforms`可以如下实现：

```c
static zx_status_t SpaceShip_ScanForLifeforms(void* ctx, fidl_txn_t* txn) {
    uint32_t life_signs[4] = {42u, 32u, 79u, 23u};
    return unn_fleet_SpaceShipScanForLifeforms_reply(txn, life_signs, 4);
}
```
 

These reply functions encode the reply and call through the `reply` function pointer on `fidl_msg_t`. 这些答复函数对答复进行编码，并通过fidl_msg_t上的答复函数指针进行调用。

 
### Binding  捆绑 

FIDL also provides `fidl_bind`, defined in [lib/fidl/bind.h](/zircon/system/ulib/fidl-async/include/lib/fidl-async/bind.h),that binds a generated dispatch function to an `async_dispatcher_t`.The `fidl_bind` function creates an `async_wait_t` that waits for messages onthe channel and calls through the given dispatcher (and ops table) when theyarrive. FIDL还提供了在[lib / fidl / bind.h]（/ zircon / system / ulib / fidl-async / include / lib / fidl-async / bind.h）中定义的`fidl_bind`，它将生成的分派函数绑定到fidl_bind函数创建一个async_wait_t，它等待通道上的消息并在到达时通过给定的调度程序（和ops表）进行调用。

<!-- xrefs --> [server]: /garnet/examples/fidl/echo_server_c/echo_server.c <！-外部参照-> [服务器]：/garnet/examples/fidl/echo_server_c/echo_server.c

