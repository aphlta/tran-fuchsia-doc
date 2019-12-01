SDK Standards ============= SDK标准==============

This document describes the standards for how we develop the Fuchsia SDK within the Platform Source Tree. Some of the information in this document might be ofinterest to clients of the Fuchsia SDK, but the primary focus of the document ishow the Fuchsia project develops the SDK. 本文档介绍了我们如何在平台源代码树中开发Fuchsia SDK的标准。 Fuchsia SDK的客户可能会对本文档中的某些信息感兴趣，但是该文档的主要重点是Fuchsia项目如何开发SDK。

 
## Governance  管治 

The contents of the Fuchsia SDK are governed by the [Fuchsia API Council]. The SDK does not contain libraries developed outside the Fuchsia project becausethose libraries are not subject to the governance of the Fuchsia API Council. Fuchsia SDK的内容受[Fuchsia API委员会]管辖。 SDK不包含在Fuchsia项目之外开发的库，因为这些库不受Fuchsia API委员会的管理。

Client libraries in the SDK do not depend on libraries outside the SDK unless the external library has been approved by the Fuchsia API Council. Typically,the council will not approve a dependency unless the dependency has strictevolution criteria (e.g., the standard libraries for the various supportedlanguages). 除非Fuchsia API委员会批准了外部库，否则SDK中的客户端库不依赖于SDK外部的库。通常，除非该依赖项具有严格的演变标准（例如，各种受支持语言的标准库），否则理事会不会批准该依赖项。

 
### Example: Google Test  示例：Google测试 

The Fuchsia SDK does not include the _Google Test_ library because the governance for the _Google Test_ library is provided by Google, not by theFuchsia API Council. Fuchsia SDK不包含_Google Test_库，因为_Google Test_库的管理是由Google提供的，而不是由Fuchsia API委员会提供的。

The Fuchsia SDK does not depend on the _Google Test_ library because the [promises made by the governing body](https://abseil.io/about/philosophy#upgrade-support)for the _Google Test_ library are not compatible with the model used by theFuchsia SDK. Fuchsia SDK不依赖_Google Test_库，因为_Google Test_库的[管理机构做出的承诺]（https://abseil.io/about/philosophyupgrade-support）与TheFuchsia使用的模型不兼容SDK。

 
## Fuchsia System Interface  紫红色系统接口 

The Fuchsia System Interface is defined in [Fuchsia System Interface](/docs/concepts/system/abi/system.md). Generally speaking, the binary interface to the systemis only the FIDL wireformat used by programs to communicate with the system and the syscalls exposedin `libzircon`. 紫红色系统界面在[紫红色系统界面]（/ docs / concepts / system / abi / system.md）中定义。一般来说，系统的二进制接口只是程序用来与系统通信的FIDL线格式，以及在libzircon中公开的系统调用。

 
## FIDL Protocol Definitions  FIDL协议定义 

 
### Binary stability  二元稳定性 

FIDL protocols are defined in `.fidl` files, which are contained in the SDK. All the FIDL definitions that have been published in an SDK should be consideredpublic ABI for the system. The system might also contain additional FIDLdefinitions that have not been published in an SDK. Those definitions aresubject to change without notice and programs that rely upon their ABI might notwork properly in future versions of the system. FIDL协议在SDK中包含的.fidl文件中定义。 SDK中已发布的所有FIDL定义均应被视为系统的公共ABI。系统可能还包含未在SDK中发布的其他FIDL定义。这些定义可能会随时更改，恕不另行通知，并且依赖于其ABI的程序在系统的将来版本中可能无法正常工作。

 
### Source stability  源稳定 

FIDL definitions in the SDK might evolve in source-incompatible ways. For example, we might rename a method in a protocol while maintaining its ordinaland semantics (the ordinal can be maintained by adding a `Selector` attributethat is set to the original name). Such a change preserves the ABI but breakssource compatibility. SDK中的FIDL定义可能会以与源不兼容的方式发展。例如，我们可以在协议中重命名方法，同时保持其序贯语义（可以通过添加设置为原始名称的“选择器”属性来维护序数）。这样的更改保留了ABI，但破坏了源兼容性。

We do not currently have any standards about when we should break source compatibility. 目前，我们尚无关于何时中断源兼容性的任何标准。

 
### Naming  命名 

Public FIDL definitions are located in the source tree under `//sdk/fidl/$LIBRARY_NAME`.The target name should be the name of the library. 公用FIDL定义位于源树中的“ // sdk / fidl / $ LIBRARY_NAME”下。目标名称应为库的名称。

 
### Style  样式 

FIDL definitions in the SDK should follow the [FIDL API style rubric].  SDK中的FIDL定义应遵循[FIDL API样式规范]。

 
## Client Libraries  客户图书馆 

The Fuchsia SDK contains a number of "client libraries" (libraries that clients of the SDK can link into their programs). All of these client libraries are optional and provided for the convenience ofclients, not for the convenience of the system. The system must not rely upon programs using anyspecific client libraries. Note that `libc` is a client library (not a system library). Fuchsia SDK包含许多“客户端库”（SDK的客户端可以链接到其程序的库）。所有这些客户端库都是可选的，并且提供它们是为了方便客户端，而不是为了系统方便。系统不得依赖使用任何特定客户端库的程序。注意，`libc`是一个客户端库（不是系统库）。

 
### Stability and Packaging  稳定性和包装 

Only the [Fuchsia System Interface](#fuchsia_system_interface) is ABI stable. Client libraries are neither API nor ABI stable. Binaries and libraries must be built against the same SDK version as theclient libraries they are linked with. 仅[Fuchsia系统接口]（fuchsia_system_interface）是ABI稳定的。客户端库既不是API也不是ABI稳定的。二进制文件和库必须与与其链接的客户端库使用相同的SDK版本构建。

All libraries a program links beyond the [Fuchsia System Interface](#fuchsia_system_interface), including client libraries, must be included inside the program's package. Dynamic libraries shouldbe placed in the `lib` directory of the program's package. 程序链接到[Fuchsia System Interface]（fuchsia_system_interface）之外的所有库，包括客户端库，都必须包含在程序包中。动态库应该放在程序包的`lib`目录中。

Packages are the unit of software mobility, delivery, and linkage. Different packages can contain different versions of the same library.  When running a program, the system provides that programthe libraries from its own package, preventing the different libraries used by different packagesfrom conflicting in the same program. 软件包是软件移动性，交付和链接的单位。不同的程序包可以包含同一库的不同版本。运行程序时，系统从其自己的程序包中为该程序提供库，以防止不同程序包使用的不同库在同一程序中发生冲突。

 

 

 
### Precompiled libraries  预编译库 

The Fuchsia SDK does not require clients to use a specific toolchain. For this reason, precompiled client libraries must have C linkage. For example, a precompiled client library cannot export C++symbols because C++ does not have a standard ABI across toolchains (or even toolchain versions). Fuchsia SDK不需要客户端使用特定的工具链。因此，预编译的客户端库必须具有C链接。例如，预编译的客户端库无法导出C ++符号，因为C ++在工具链（甚至工具链版本）中没有标准的ABI。

 
### Dependencies  依存关系 

A client that takes a dependency on a client library must also take a dependency on all the dependencies of that library. For this reason, client librariesshould have minimal dependencies. For example, client libraries should avoiddependencies on FBL, FXL, FSL, or other "base" libraries that are not inthe SDK. 依赖于客户端库的客户端也必须依赖于该库的所有依赖关系。因此，客户端库应具有最小的依赖性。例如，客户端库应避免依赖于SDK以外的FBL，FXL，FSL或其他“基础”库。

Client libraries that need to perform asynchronous operations should depend on `libasync.a` and `libasync-default.so`. However, these libraries should notassume the client is using any specific implementation of `async_dispatcher_t*`.For example, these libraries should not assume the `async_dispatcher_t*` isactually implemented by `libasync-loop.a`. Libraries that require`async_get_default_dispatcher` to be populated should state this requirement intheir documentation. 需要执行异步操作的客户端库应该依赖于`libasync.a`和`libasync-default.so`。但是，这些库不应该假定客户端正在使用async_dispatcher_t *的任何特定实现，例如，这些库不应该假设libasync-loop.a实际实现了async_dispatcher_t *。需要填充“ async_get_default_dispatcher”的库应在其文档中说明此要求。

Precompiled libraries can have more extensive dependencies if those dependencies are hidden from their client. For example, a precompiled shared library shouldnot export symbols from these dependencies and should not have headers thattransitively include headers from these dependencies. 如果预编译库从其客户端中隐藏，则它们可能具有更广泛的依赖关系。例如，预编译的共享库不应从这些依赖项中导出符号，并且不应具有包含这些依赖项的标头的头文件。

 
### Naming  命名 

Client libraries should be named according to the language they expect their clients to use.For example, the C++ variant of the `$NAME` library should be located in thesource tree under `//sdk/lib/$NAME/cpp`.The C variant should simply be under `//sdk/lib/$NAME`. 客户端库应该根据他们希望客户端使用的语言来命名。例如，$ NAME库的C ++变体应位于源树中的// sdk / lib / $ NAME / cpp下。 C变体应该只在`// sdk / lib / $ NAME`下。

 
### Style  样式 

Client libraries should follow the Fuchsia style guide for the language in which they are written. 客户库应遵循其紫红色风格指南来编写语言。

 
### Logging  记录中 

Client libraries should avoid logging messages. Instead, client libraries should return errors to their clients, who can decide whether to log the error. 客户端库应避免记录消息。相反，客户端库应该将错误返回给客户端，客户端可以决定是否记录错误。

 
### Assertions  断言 

C and C++ client libraries should use `ZX_DEBUG_ASSERT` and `ZX_ASSERT`, defined in `<zircon/assert.h>`, to assert invariants. Client libraries may also use the`_MSG` variants to provide a message when the assertion fails. C和C ++客户端库应使用在<zircon / assert.h>中定义的ZX_DEBUG_ASSERT和ZX_ASSERT来声明不变量。当断言失败时，客户端库也可以使用-MSG变体来提供消息。

 
## Recommendations for client code  客户代码建议 

 
### C  C 

The Fuchsia System Interface uses symbols with the `zx_` and `fuchsia_` prefixes and preprocessor macros with the `ZX_` and `FUCHSIA_` prefixes. To avoid collisions, theseprefixes are reserved for use by the Fuchsia SDK. Clients of the Fuchsia SDK should notdeclare symbols or preprocessor macros with these prefixes. 紫红色的系统界面使用前缀为zx_和fuchsia_的符号以及前缀为ZX_和FUCHSIA_的预处理器宏。为避免冲突，这些前缀保留供Fuchsia SDK使用。 Fuchsia SDK的客户端不应使用这些前缀声明符号或预处理器宏。

 
### C++  C ++ 

The FIDL protocols included in the Fuchsia System Interface resides in the top-level `fuchsia` namespace. To avoid collisions, this namespace is reserved for use by theFuchsia SDK. Clients of the Fuchsia SDK should not declare names in the top-level`fuchsia` namespace. 紫红色系统接口中包含的FIDL协议位于顶层“紫红色”命名空间中。为了避免冲突，该名称空间保留供TheFuchsia SDK使用。 Fuchsia SDK的客户端不应在顶级“ fuchsia”命名空间中声明名称。

