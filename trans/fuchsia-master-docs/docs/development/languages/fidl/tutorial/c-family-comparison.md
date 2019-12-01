 

 
# Comparing C, Low-Level C++, and High-Level C++ Language Bindings  比较C，低级C ++和高级C ++语言绑定 

[TOC]  [目录]

 
## C Bindings  C绑定 

 
*   Optimized to meet the needs of low-level systems programming, plus tight constraints around dependencies and toolchains. The compiler, bindingslibrary, and code-generator are written in C++, while exposing a pure Cinterface to clients. *经过优化以满足底层系统编程的需求，以及对依赖项和工具链的严格约束。编译器，绑定库和代码生成器使用C ++编写，同时向客户端公开纯C接口。
*   Represent data structures whose memory layout coincides with the wire format. *表示其内存布局与连线格式一致的数据结构。
*   Support in-place access and construction of FIDL messages.  *支持就地访问和FIDL消息的构造。
*   Generated structures are views of an underlying buffer; they do not own memory. *生成的结构是基础缓冲区的视图；他们没有自己的记忆。
*   Provide convenience wrappers for message construction and calling for a limited subset of FIDL messages([[Layout = "Simple"]](/docs/development/languages/fidl/reference/attributes.md#layout) types). *为消息构造和调用FIDL消息的有限子集提供便利包装（[[Layout =“ Simple”]] [/ docs / development / languages / fidl / reference / attributes.mdlayout）类型）。
*   Client is synchronous only. Two-way method calls will block.  *客户端仅是同步的。双向方法调用将阻塞。
*   As the Low-Level C++ Bindings mature, there are plans to re-implement the C bindings as a light-weight wrapper around the C++ bindings. *随着低级C ++绑定的成熟，计划将C绑定重新实现为C ++绑定的轻量级包装。

 
## Low-Level C++ Bindings  低级C ++绑定 

 
*   Optimized to meet the needs of low-level systems programming while providing slightly more safety and features than the C bindings. *经过优化，可以满足低级系统编程的需求，同时提供比C绑定稍高的安全性和功能。
*   Represent data structures whose memory layout coincides with the wire format, i.e. satisfying C++ Standard Layout. This opens the door toin-place encoding and decoding. *表示其内存布局与有线格式相符的数据结构，即满足C ++标准布局。这为就地编码和解码打开了大门。
*   Support in-place access and construction of FIDL messages.  *支持就地访问和FIDL消息的构造。
*   Generated structures are views of an underlying buffer; they do not own memory. *生成的结构是基础缓冲区的视图；他们没有自己的记忆。
*   Use owned handle types such as `zx::handle`. Note that since generated structures are views of an underlying buffer, a parent structure will onlyown child handles if it also owns their underlying buffer. For example, aFIDL struct owns all the handles stored inline, but a FIDL vector of structscontaining handles will be represented as a vector view, which will not ownthe out-of-line handles. *使用拥有的句柄类型，例如`zx :: handle`。请注意，由于生成的结构是基础缓冲区的视图，因此，如果父结构也拥有其基础缓冲区，则其父结构将只有其子句柄。例如，FIDL结构拥有内联存储的所有句柄，但是包含句柄的结构的FIDL向量将表示为矢量视图，而该视图将不具有离线句柄。
*   Defer all memory allocation decisions to the client.  *将所有内存分配决策推迟到客户端。
*   Code generator produces only type declarations, coding tables, simple inline functions, and pure virtual server interfaces. *代码生成器仅生成类型声明，编码表，简单的内联函数和纯虚拟服务器接口。
*   Client may manually dispatch incoming method calls on protocols (write their own switch statement and invoke argument decode functions). *客户端可以在协议上手动调度传入的方法调用（编写自己的switch语句并调用参数解码功能）。
*   Similar to the C language bindings but using zero-cost C++ features such as namespaces, string views, and array containers. *与C语言绑定类似，但使用零成本的C ++功能，例如名称空间，字符串视图和数组容器。
*   Client is synchronous only. However, async client support is planned.  *客户端仅是同步的。但是，计划了异步客户端支持。

 
## High-Level C++ Bindings  高级C ++绑定 

 
*   Optimized to meet the needs of high-level service programming.  *经过优化以满足高级服务编程的需求。
*   Represent data structures using idiomatic C++ types such as `std::vector`, `std::optional`, and `std::string`. *使用惯用的C ++类型表示数据结构，例如`std :: vector`，`std :: optional`和`std :: string`。
*   Use smart pointers to manage heap allocated objects.  *使用智能指针来管理堆分配的对象。
*   Use `zx::handle` (libzx) to manage handle ownership.  *使用`zx :: handle`（libzx）管理句柄所有权。
*   Can convert data from in-place FIDL buffers to idiomatic heap allocated objects. *可以将数据从就地FIDL缓冲区转换为惯用堆分配的对象。
*   Can convert data from idiomatic heap allocated objects (e.g. `std::string`) to in-place buffers (e.g. as a `fidl::StringView`). *可以将数据从惯用的堆分配对象（例如，std :: string`）转换为就地缓冲区（例如，作为`fidl :: StringView`）。
*   Code generator produces more code compared to the low-level C++ bindings, and much more than the C bindings. This includes constructors, destructors,protocol proxies, protocol stubs, copy/move functions, andconversions to/from in-place buffers. *与低级C ++绑定相比，代码生成器生成的代码更多，并且比C绑定更多。这包括构造函数，析构函数，协议代理，协议存根，复制/移动函数以及到/从就地缓冲区的转换。
*   Client performs protocol dispatch by subclassing a provided stub and implementing the virtual methods for each operation. *客户端通过子类化提供的存根并为每个操作实现虚拟方法来执行协议调度。
*   Both async and synchronous clients are supported. However, the async clients are not thread-safe. *支持异步和同步客户端。但是，异步客户端不是线程安全的。

 
## Summary  摘要 

Category                           | Simple C                          | Low-level C++                                 | High-level C++ -----------------------------------|-----------------------------------|-----------------------------------------------|--------------------**audience**                       | drivers                           | drivers and performance-critical applications | high-level services**abstraction overhead**           | almost zero                       | almost zero                                   | heap allocation, construction, destruction**type safe types**                | enums, structs, unions            | enums, structs, unions, handles, protocols    | enums, structs, unions, handles, protocols**storage**                        | stack                             | stack, in-place buffer, or heap               | heap**lifecycle**                      | manual free (POD)                 | manual free memory; own handles via RAII [1]  | automatic free (RAII)**receive behavior**               | copy                              | copy or decode in-place                       | decode then move to heap**send behavior**                  | copy                              | copy or encode in-place                       | move to buffer then encode**calling protocol methods**       | free functions                    | free functions or proxy                       | call through proxies, register callbacks**implementing protocol methods**  | manual dispatch or via ops table  | manual dispatch or implement stub interface   | implement stub object, invoke callbacks**async client**                   | no                                | no (planned)                                  | yes**async server**                   | limited [2]                       | yes (unbounded) [3]                           | yes (unbounded)**generated code footprint**       | small                             | moderate                                      | large 分类|简单C |低级C ++高级C ++ ----------------------------------- | ---------- ------------------------- | ------------------------ ----------------------- | -------------------- **观众** |驱动程序|驱动程序和对性能至关重要的应用程序|高级服务**抽象开销** |几乎为零|几乎为零|堆分配，构造，销毁**类型安全类型** |枚举，结构，联合|枚举，结构，联合，句柄，协议|枚举，结构，联合，句柄，协议**存储** |堆叠堆栈，就地缓冲区或堆堆**生命周期** |免提（POD）|手动可用内存；通过RAII自己处理[1] |自动免费（RAII）**接收行为** |复制|就地复制或解码|解码然后移到堆**发送行为** |复制|就地复制或编码|移至缓冲区，然后进行编码**调用协议方法** |免费功能|免费功能或代理|通过代理调用，注册回调**实现协议方法** |手动调度或通过操作表|手动调度或实现存根接口|实现存根对象，调用回调**异步客户端** |没有否（计划中）|是**异步服务器** |限量[2]是（无界）[3] |是（无边界）**生成的代码占用量** |小|中度|大

Notes:  笔记：

 
1. Generated types own all handles stored inline. Out-of-line handles e.g. those behind a pointer indirection are not closed when the containing object of thepointer goes away. In thoses cases, the bindings provide a`fidl::DecodedMessage` object to manage all handles associated with a call. 1.生成的类型拥有所有内联存储的句柄。脱机手柄，例如当指针的包含对象消失时，那些在指针间接定向后面的对象不会关闭。在那种情况下，绑定提供一个fidl :: DecodedMessage对象来管理与调用关联的所有句柄。
2. The bindings library can dispatch at most one in-flight transaction.  2.绑定库最多可以调度一个进行中的事务。
3. The bindings library defined in [lib/fidl-async](/zircon/system/ulib/fidl-async) can dispatch an unbounded number of in-flight transactions via `fidl::AsyncBind` defined in [lib/fidl-async/cpp/async_bind.h](/zircon/system/ulib/fidl-async/include/lib/fidl-async/cpp/async_bind.h).  3. [lib / fidl-async]（/ zircon / system / ulib / fidl-async）中定义的绑定库可以通过[lib / fidl-a中定义的`fidl :: AsyncBind`调度无数的正在进行中的事务。异步/cpp/async_bind.h]（/zircon/system/ulib/fidl-async/include/lib/fidl-async/cpp/async_bind.h）。

 
## Migrating From C Bindings To Low-Level C++  从C绑定迁移到低级C ++ 

