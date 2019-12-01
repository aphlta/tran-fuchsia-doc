 
# C++ in Zircon  Zircon中的C ++ 

A subset of the C++17 language is used in the Zircon tree.  This includes both the kernel and userspace code.  C++ is mixed with C (and some assembly) inboth places.  Some C++ language features are avoided or prohibited.  Use ofthe C++ standard library features is very circumspect. Zircon树中使用了C ++ 17语言的子集。这包括内核代码和用户空间代码。 C ++在两个地方都与C（和某些汇编）混合在一起。避免或禁止某些C ++语言功能。使用C ++标准库功能非常谨慎。

 
## Language features  语言特征 

 
- Not allowed  - 不允许
  - Exceptions  -例外
  - RTTI and `dynamic_cast`  -RTTI和dynamic_cast
  - Operator overloading  -操作员超载
  - Virtual inheritance  -虚拟继承
  - Statically constructed objects  -静态构造的对象
  - Trailing return type syntax  -尾随返回类型语法
    - Exception: when necessary for lambdas with otherwise unutterable return types  -例外：对于具有其他无法说明的返回类型的Lambda而言是必要的
  - Initializer lists  -初始化列表
  - `thread_local` in kernel code  -内核代码中的`thread_local`
- Allowed  -允许
  - Pure interface inheritance  -纯接口继承
  - Lambdas  -Lambdas
  - `constexpr`  -`constexpr`
  - `nullptr`  -`nullptr`
  - `enum class`es  -`枚举类`es
  - `template`s  -`template`s
  - Default parameters  -默认参数
    - But use judgment. One optional out parameter at the end is probably fine. Four optional bool arguments, probably not. -但是要运用判断力。最后一个可选的out参数可能很好。四个可选的布尔参数，可能不是。
  - Plain old classes  -普通的旧班
  - `auto`  -`auto`
  - Multiple implementation inheritance  -多重实现继承
    - But be judicious. This is used widely for e.g. intrusive container mixins. -但要明智。这被广泛用于例如侵入式容器mixins。
- Needs more ruling TODO(cpu)  -需要更多裁决TODO（cpu）
  - Global constructors  -全局构造函数
    - Currently we have these for global data structures.  -目前，我们拥有用于全局数据结构的这些。

**TODO:** pointer to style guide(s)?  ** TODO：**指向样式指南的指针？

 
## C++ Standard Edition (17 vs 14)  C ++标准版（17 vs 14） 

Zircon code is built with `-std=c++17` and in general can use C++ 17 language and library features freely (subject to style/feature constraints described[above](#language-features) and library use guidelines described[below](#standard-library)).  There is no *general* concern with stayingcompatible with C++ 14 or earlier versions.  When a standard C++ 17 feature isthe cleanest way to do something, do it that way. Zircon代码是使用-std = c ++ 17构建的，通常可以自由使用C ++ 17语言和库功能（受描述的样式/功能约束[上面]（语言功能）和描述的库使用准则[下面] （标准库））。保持与C ++ 14或更早版本的兼容性没有*一般*的问题。当标准的C ++ 17功能是做某事的最干净的方法时，请这样做。

**However** any library that is **published to the SDK** must be compatible with SDK users building in **both** C++ 14 and C++ 17 modes.  So, anylibraries exported to the SDK must have public header files that are*compatible with both `-std=c++14` and `-std=c++17`*.  If a library isexported to the SDK as source code rather than as a binary, then its *sourcecode must also be completely compatible with both `-std=c++14` and`-std=c++17`* (and not require other special options). **TODO(mcgrathr):**_pointer to build-system docs about maintaining code to be exported to SDK_ **然而，**任何发布到SDK的库都必须与以** C ++ 14和C ++ 17模式构建的SDK用户兼容。因此，导出到SDK的任何库都必须具有与-std = c ++ 14和-std = c ++ 17 **兼容的公共头文件。如果将库作为源代码而不是二进制文件导出到SDK，则其*源代码还必须与`-std = c ++ 14`和`-std = c ++ 17` *完全兼容（而不是需要其他特殊选项）。 ** TODO（mcgrathr）：** _指向有关维护要导出到SDK_的代码的系统文档

All pure C code (`.c` source files and headers used by them) is C 11.  Some special exceptions are made for code meant to be reused by out-of-tree bootloaders, which stick to a conservative C 89 subset for embedded code. 所有纯C代码（它们使用的`.c`源文件和头文件）都是C11。一些特殊的例外情况是打算供树外引导程序重用的代码，这些引导程序坚持使用保守的C 89子集进行嵌入式码。

 
## Standard Library  标准图书馆 

The C++ standard library API has many interfaces of widely varying characteristics.  We subdivide the standard library API into severalcategories below, based on the predictability and complexity of eachparticular interface's code generation and use of machine and OS facilities.These can be thought of as widening concentric circles of the API from themost minimal C-like subset out to the full C++ 17 API. C ++标准库API具有许多特性各异的接口。根据每个特定接口的代码生成以及使用机器和OS设备的可预测性和复杂性，我们将标准库API细分为以下几类：可以将这些API的同心圆从最小的类C子集扩展到完整的C ++ 17 API。

 
#### Context Matters  上下文事项 

This section gives guidelines for how to think about the impact of using a particular standard C++ library API on the system as a whole.  There are nohard and fast rules, except for the kernel (see the next section)--and exceptfor implementation constraints, which one always hopes should be temporary. 本节提供了有关如何考虑使用特定标准C ++库API对整个系统的影响的指南。除了内核（请参阅下一节）以外，没有硬性和快速的规则，除了实现约束，人们总是希望这是临时的。

The overwhelming rule is **be circumspect**.  压倒一切的规则是“谨慎”。

 
 * Consider how well you understand the time and space complexity, the dynamic allocation behavior (if any), and the failure modes of *each API you use*. *考虑一下您对使用的每个API *的时间和空间复杂性，动态分配行为（如果有）以及失败模式的了解程度。

 
 * Then consider the specific *context* where it's being used, and how sensitive that context is to those various kinds of concerns. *然后考虑使用的特定* context *，以及该上下文对各种问题的敏感程度。

 
 * Be especially wary about **input-dependent** behavior that can quickly become far harder to predict when using nontrivial library facilities. *特别注意“依赖输入”的行为，这种行为在使用非平凡的库工具时可能很快变得难以预测。

If you're writing the main I/O logic in a driver, or anything that's in a hot path for latency, throughput, or reliability, in any kind of system service,then you should be pretty conservative in what library facilities you rely on.They're all technically available to you in userspace (though far fewer in thekernel; see the next section).  But there's not so many you actually shoulduse.  You probably don't want to lean on a lot of `std` containers that dofancy dynamic allocation behind the scenes.  They will make it hard for you tounderstand, predict, and control the storage/memory footprint, allocationbehavior, performance, and reliability of your service. 如果您要在驱动程序中编写主要的I / O逻辑，或者在任何类型的系统服务中为延迟，吞吐量或可靠性提供热销的任何东西，那么您应该对所依赖的库工具非常保守从技术上讲，它们都可以在用户空间中使用（尽管内核中的数量要少得多；请参阅下一节）。但是实际上您应该使用的并不多。您可能不想依靠很多隐藏动态分配的`std`容器。它们将使您难以理解，预测和控制存储/内存占用量，分配行为，性能以及服务的可靠性。

Nonetheless, even a driver is a userspace program that starts up and parses configuration files or arguments and so on.  For all those nonessential orstart-time functions that are not part of the hot path, using more complexlibrary facilities is probably fine when that makes the work easier.  Justremember to pay attention to overall metrics for your code, such asminimal/total/peak runtime memory use, code bloat (which uses both devicestorage and runtime memory), and resilience to unexpected failure modes.Maybe don't double the code size and memory footprint of your driver just toleverage that fancy configuration-parsing library. 但是，即使驱动程序也是一个用户空间程序，它会启动并解析配置文件或参数等。对于不属于热路径的所有那些不必要的或启动时函数，使用更复杂的库工具可能会很好，因为这样会使工作更轻松。请记住，要注意代码的总体指标，例如最小/总/峰值运行时内存使用情况，代码膨胀（同时使用设备存储和运行时内存）以及对意外故障模式的恢复力。也许不要将代码大小和内存加倍驱动程序的占用空间只是利用了这个精美的配置分析库。

 
#### No `std` in kernel  内核中没有`std` 

The C++ `std` namespace **cannot** be used in [kernel](/zircon/kernel) code, which also includes [bootloader](/zircon/bootloader).  The few C++ standard libraryheaders that don't involve `std::` APIs can still be used directly.  See thenext section. 不能在[kernel]（/ zircon / kernel）代码中使用C ++ std名称空间**，该代码还包括[bootloader]（/ zircon / bootloader）。少数不涉及`std ::`API的C ++标准库头仍然可以直接使用。参见下一节。

No other C++ standard headers should be used in kernel code.  Instead, any library facilities worthwhile to have in the kernel (such as`std::move`) are provided via kernel-specific APIs (such as`ktl::move`).  The kernel's implementations of these APIs may in factrely on toolchain headers providing `std::` implementations that arealiased to kernel API names.  But only those API implementations andvery special cases in certain library headers should ever use `std::`in source code built into the kernel. 内核代码中不应使用其他C ++标准标头。取而代之的是，通过内核特定的API（例如ktl :: move）来提供内核中值得拥有的任何库功能（例如std :: move）。实际上，这些API的内核实现可能在工具链标头上，提供了类似于内核API名称的`std ::`实现。但是，只有那些API实现和某些库头中的很多特殊情况才应该在内核内置的源代码中使用“ std ::”。

 
#### Universal headers  通用接头 

These header APIs are safe to use everywhere, even in the kernel.  这些标头API可以在任何地方使用，即使在内核中也可以安全使用。

They include the C++ wrappers on the subset of standard C interfaces that the kernel supports: 它们在内核支持的标准C接口子集上包括C ++包装器：

 
 * [`<cstdarg>`](https://en.cppreference.com/w/cpp/header/cstdarg)  * [`<cstdarg>`]（https://en.cppreference.com/w/cpp/header/cstdarg）
 * [`<cstddef>`](https://en.cppreference.com/w/cpp/header/cstddef)  * [`<cstddef>`]（https://en.cppreference.com/w/cpp/header/cstddef）
 * [`<climits>`](https://en.cppreference.com/w/cpp/header/climits)  * [`<climits>`]（https://en.cppreference.com/w/cpp/header/climits）
 * [`<cstdint>`](https://en.cppreference.com/w/cpp/header/cstdint)  * [`<cstdint>`]（https://en.cppreference.com/w/cpp/header/cstdint）
 * [`<cinttypes>`](https://en.cppreference.com/w/cpp/header/cinttypes)  * [`<cinttypes>`]（https://en.cppreference.com/w/cpp/header/cinttypes）
 * [`<cassert>`](https://en.cppreference.com/w/cpp/header/cassert)  * [`<cassert>`]（https://en.cppreference.com/w/cpp/header/cassert）
 * [`<cstring>`](https://en.cppreference.com/w/cpp/header/cstring)  * [`<cstring>`]（https://en.cppreference.com/w/cpp/header/cstring）

The `std` namespace aliases for C library APIs from these headers should not be used in kernel code. 这些标头中C库API的`std`名称空间别名不应在内核代码中使用。

One pure C++ header is also available even in the kernel:  即使在内核中，也可以使用一个纯C ++头文件：

 
 * [`<new>`](https://en.cppreference.com/w/cpp/header/new)  * [`<new>`]（https://en.cppreference.com/w/cpp/header/new）

   The vanilla non-placement `operator new` and `operator new[]` are not available in the kernel.  Use [`fbl::AllocChecker``new`](/zircon/system/ulib/fbl/include/fbl/alloc_checker.h) instead. 内核中不提供香草非放置的“ operator new”和“ operator new []”。改用[`fbl :: AllocChecker``new`]（/ zircon / system / ulib / fbl / include / fbl / alloc_checker.h）。

 
#### Conservative userspace  保守的用户空间 

These header APIs are safe to use everywhere.  They're not allowed in the kernel because they're all entirely in the `std` namespace.  But subsets ofthese APIs are likely candidates to get an in-kernel API alias if there is agood case for using such an API in kernel code. 这些标头API可以在任何地方安全使用。不允许在内核中使用它们，因为它们全部都在`std`命名空间中。但是，如果存在在内核代码中使用此类API的良好情况，则这些API的子集很可能会获得内核内API别名。

These are pure header-only types and templates.  They don't do any dynamic allocation of their own.  The time and space complexity of each functionshould be clear from its description. 这些是纯仅标头的类型和模板。他们自己不做任何动态分配。每个功能的时间和空间复杂度应从其描述中清楚看出。

 
 * [`<algorithm>`](https://en.cppreference.com/w/cpp/header/algorithm)  * [`<algorithm>`]（https://en.cppreference.com/w/cpp/header/algorithm）
 * [`<array>`](https://en.cppreference.com/w/cpp/header/array)  * [`<array>`]（https://en.cppreference.com/w/cpp/header/array）
 * [`<atomic>`](https://en.cppreference.com/w/cpp/header/atomic)  * [`<atomic>`]（https://en.cppreference.com/w/cpp/header/atomic）
 * [`<bitset>`](https://en.cppreference.com/w/cpp/header/bitset)  * [`<bitset>`]（https://en.cppreference.com/w/cpp/header/bitset）
 * [`<initializer_list>`](https://en.cppreference.com/w/cpp/header/initializer_list)  * [`<initializer_list>`]（https://en.cppreference.com/w/cpp/header/initializer_list）
 * [`<iterator>`](https://en.cppreference.com/w/cpp/header/iterator)  * [`<iterator>`]（https://en.cppreference.com/w/cpp/header/iterator）
 * [`<limits>`](https://en.cppreference.com/w/cpp/header/limits)  * [`<limits>`]（https://en.cppreference.com/w/cpp/header/limits）
 * [`<optional>`](https://en.cppreference.com/w/cpp/header/optional)  * [`<optional>`]（https://en.cppreference.com/w/cpp/header/optional）
 * [`<tuple>`](https://en.cppreference.com/w/cpp/header/tuple)  * [`<tuple>`]（https://en.cppreference.com/w/cpp/header/tuple）
 * [`<type_traits>`](https://en.cppreference.com/w/cpp/header/type_traits)  * [`<type_traits>`]（https://en.cppreference.com/w/cpp/header/type_traits）
 * [`<utility>`](https://en.cppreference.com/w/cpp/header/utility)  * [`<utility>`]（https://en.cppreference.com/w/cpp/header/utility）
 * [`<variant>`](https://en.cppreference.com/w/cpp/header/variant)  * [`<variant>`]（https://en.cppreference.com/w/cpp/header/variant）

These involve some dynamic allocation, but only what's explicit:  这些涉及一些动态分配，但是仅是明确的：

 
 * [`<any>`](https://en.cppreference.com/w/cpp/header/any)  * [`<any>`]（https://en.cppreference.com/w/cpp/header/any）
 * [`<memory>`](https://en.cppreference.com/w/cpp/header/memory)  * [`<memory>`]（https://en.cppreference.com/w/cpp/header/memory）

   The `std::shared_ptr`, `std::weak_ptr`, and `std::auto_ptr` APIs should **never** be used.  Use `std::unique_ptr` and `fbl::RefPtr` instead. 绝对不要使用std :: shared_ptr，std :: weak_ptr和std :: auto_ptr API。请改用`std :: unique_ptr`和`fbl :: RefPtr`。

 
##### Userspace-only  仅限用户空间 

These are not things that would ever be available at all or by any similar API or name in the kernel.  But they are generally harmless everywhere inuserspace.  They do not involve dynamic allocation. 这些根本不是全部可用，也不是内核中任何类似的API或名称都无法使用的东西。但是它们通常在用户空间中的任何地方都是无害的。它们不涉及动态分配。

 
 * Floating-point is never available in kernel code, but can be used (subject to performance considerations) in all userspace code. *浮点数在内核代码中永远不可用，但可以在所有用户空间代码中使用（视性能而定）。
   * [`<cfenv>`](https://en.cppreference.com/w/cpp/header/cfenv)  * [`<cfenv>`]（https://en.cppreference.com/w/cpp/header/cfenv）
   * [`<cfloat>`](https://en.cppreference.com/w/cpp/header/cfloat)  * [`<cfloat>`]（https://en.cppreference.com/w/cpp/header/cfloat）
   * [`<cmath>`](https://en.cppreference.com/w/cpp/header/cmath)  * [`<cmath>`]（https://en.cppreference.com/w/cpp/header/cmath）
   * [`<complex>`](https://en.cppreference.com/w/cpp/header/complex)  * [`<complex>`]（https://en.cppreference.com/w/cpp/header/complex）
   * [`<numeric>`](https://en.cppreference.com/w/cpp/header/numeric)  * [`<numeric>`]（https://en.cppreference.com/w/cpp/header/numeric）
   * [`<ratio>`](https://en.cppreference.com/w/cpp/header/ratio)  * [`<ratio>`]（https://en.cppreference.com/w/cpp/header/ratio）
   * [`<valarray>`](https://en.cppreference.com/w/cpp/header/valarray)  * [`<valarray>`]（https://en.cppreference.com/w/cpp/header/valarray）

 
 * Full C 11 standard library, via C++ wrappers or in standard C `<*.h>`.  *完整的C 11标准库，通过C ++包装程序或在标准C`<*。h>`中提供。
   * [`<csetjmp>`](https://en.cppreference.com/w/cpp/header/csetjmp)  * [`<csetjmp>`]（https://en.cppreference.com/w/cpp/header/csetjmp）
   * [`<cstdlib>`](https://en.cppreference.com/w/cpp/header/cstdlib)  * [`<cstdlib>`]（https://en.cppreference.com/w/cpp/header/cstdlib）
   * [Standard C11 interfaces](https://en.cppreference.com/w/c/header)  * [标准C11接口]（https://en.cppreference.com/w/c/header）

 
 * Synchronization and threads.  These standard APIs are safe to use in all userspace code with appropriate discretion.  But it may often be better touse Zircon's own library APIs for similar things, such as[<lib/sync/...>](/zircon/system/ulib/sync/include). *同步和线程。这些标准API可以适当地酌情在所有用户空间代码中安全使用。但是，使用Zircon自己的库API进行类似操作通常会更好，例如[<lib / sync /...>](/ zircon / system / ulib / sync / include）。
   * [`<condition_variable>`](https://en.cppreference.com/w/cpp/header/condition_variable)  * [`<condition_variable>`]（https://en.cppreference.com/w/cpp/header/condition_variable）
   * [`<execution>`](https://en.cppreference.com/w/cpp/header/execution)  * [`<execution>`]（https://en.cppreference.com/w/cpp/header/execution）
   * [`<mutex>`](https://en.cppreference.com/w/cpp/header/mutex)  * [`<mutex>`]（https://en.cppreference.com/w/cpp/header/mutex）
   * [`<shared_mutex>`](https://en.cppreference.com/w/cpp/header/shared_mutex)  * [`<shared_mutex>`]（https://en.cppreference.com/w/cpp/header/shared_mutex）
   * [`<thread>`](https://en.cppreference.com/w/cpp/header/thread)  * [`<thread>`]（https://en.cppreference.com/w/cpp/header/thread）

 
#### Kitchen sink  厨房水槽 

These involve dynamic allocation that is hard to predict and is generally out of your control.  The exact runtime behavior and memory requirements are oftenhard to reason about.  Think very hard before using these interfaces in anycritical path for reliability or performance or in any component that is meantto be lean and space-efficient. 这些涉及动态分配，这种动态分配很难预测，而且通常无法控制。确切的运行时行为和内存需求通常很难推理。在将这些接口用于任何关键路径以提高可靠性或性能，或将其用于任何精益且节省空间的组件之前，都要三思而行。

 
 * The entire [Containers library](https://en.cppreference.com/w/cpp/container)  *整个[容器库]（https://en.cppreference.com/w/cpp/container）

 
 * [`<functional>`](https://en.cppreference.com/w/cpp/header/functional)  * [`<functional>`]（https://en.cppreference.com/w/cpp/header/functional）

   See [`<lib/fit/function.h>`](/zircon/system/ulib/fit/include/lib/fit/function.h) for a homegrown alternative. 请参阅[`<lib / fit / function.h>`]（/ zircon / system / ulib / fit / include / lib / fit / function.h）以了解本地替代方法。

 
 * [`<memory_resource>`](https://en.cppreference.com/w/cpp/header/memory_resource)  * [`<memory_resource>`]（https://en.cppreference.com/w/cpp/header/memory_resource）
 * [`<scoped_allocator>`](https://en.cppreference.com/w/cpp/header/scoped_allocator)  * [`<scoped_allocator>`]（https://en.cppreference.com/w/cpp/header/scoped_allocator）

 
 * [`<filesystem>`](https://en.cppreference.com/w/cpp/header/filesystem)  * [`<文件系统>`]（https://en.cppreference.com/w/cpp/header/filesystem）
 * [`<regex>`](https://en.cppreference.com/w/cpp/header/regex)  * [`<regex>`]（https://en.cppreference.com/w/cpp/header/regex）

 
## FBL  FBL 

FBL is the Fuchsia Base Library, which is shared between kernel and userspace. As a result, FBL has very strict dependencies.  For example, FBL cannot dependon the syscall interface because the syscall interface is not available withinthe kernel.  Similarly, FBL cannot depend on C library features that are notavailable in the kernel. FBL是Fuchsia Base Library，在内核和用户空间之间共享。结果，FBL具有非常严格的依赖性。例如，FBL不能依赖syscall接口，因为syscall接口在内核中不可用。同样，FBL不能依赖内核中不可用的C库功能。

 
1. [system/ulib/fbl](/zircon/system/ulib/fbl) which is usable from both kernel and userspace. 1. [system / ulib / fbl]（/ zircon / system / ulib / fbl）可以从内核和用户空间使用。
2. [kernel/lib/fbl](/zircon/kernel/lib/fbl) which is usable only from the kernel. 2. [kernel / lib / fbl]（/ zircon / kernel / lib / fbl），仅可从内核使用。

Note: Some FBL interfaces below that overlap with standard C++ library interfaces will probably be either removed entirely or made kernel-only (andperhaps renamed inside the kernel) once userspace code has migrated to usingstandard C++ library facilities where appropriate. 注意：在适当的情况下，如果用户空间代码已迁移到使用标准C ++库工具，则某些与标准C ++库接口重叠的FBL接口可能会被完全删除或变为仅内核（可能在内核内部重命名）。

FBL provides:  FBL提供：

 
- utility code  -实用代码
  - [basic algorithms](/zircon/system/ulib/fbl/include/fbl/algorithm.h)  -[基本算法]（/ zircon / system / ulib / fbl / include / fbl / algorithm.h）
  - [alloc checking new](/zircon/system/ulib/fbl/include/fbl/alloc_checker.h)  -[分配新的检查]（/ zircon / system / ulib / fbl / include / fbl / alloc_checker.h）
- allocators  -分配器
  - [slab allocation](/zircon/system/ulib/fbl/include/fbl/slab_allocator.h)  -[平板分配]（/ zircon / system / ulib / fbl / include / fbl / slab_allocator.h）
  - [slab malloc](/zircon/system/ulib/fbl/include/fbl/slab_malloc.h)  -[slab malloc]（/ zircon / system / ulib / fbl / include / fbl / slab_malloc.h）
- arrays  -数组
  - [fixed sized arrays](/zircon/system/ulib/fbl/include/fbl/array.h)  -[固定大小的数组]（/ zircon / system / ulib / fbl / include / fbl / array.h）
  - [fixed sized arrays](/zircon/kernel/lib/fbl/include/fbl/inline_array.h), which stack allocates small arrays -[固定大小的数组]（/ zircon / kernel / lib / fbl / include / fbl / inline_array.h），该堆栈分配小数组
- inline containers  -嵌入式容器
  - [doubly linked list](/zircon/system/ulib/fbl/include/fbl/intrusive_double_list.h)  -[双向链接列表]（/ zircon / system / ulib / fbl / include / fbl / intrusive_double_list.h）
  - [hash table](/zircon/system/ulib/fbl/include/fbl/intrusive_hash_table.h)  -[哈希表]（/ zircon / system / ulib / fbl / include / fbl / intrusive_hash_table.h）
  - [singly linked list](/zircon/system/ulib/fbl/include/fbl/intrusive_single_list.h)  -[单链列表]（/ zircon / system / ulib / fbl / include / fbl / intrusive_single_list.h）
  - [wavl trees](/zircon/system/ulib/fbl/include/fbl/intrusive_wavl_tree.h)  -[wavl树]（/ zircon / system / ulib / fbl / include / fbl / intrusive_wavl_tree.h）
- smart pointers  -智能指针
  - [intrusive refcounted mixin](/zircon/system/ulib/fbl/include/fbl/ref_counted.h)  -[侵入式引用混合]（/ zircon / system / ulib / fbl / include / fbl / ref_counted.h）
  - [intrusive refcounting pointer](/zircon/system/ulib/fbl/include/fbl/ref_ptr.h)  -[侵入式计数指针]（/ zircon / system / ulib / fbl / include / fbl / ref_ptr.h）
- raii utilities  -raii实用程序
  - [auto call](/zircon/system/ulib/fbl/include/fbl/auto_call.h) to run code upon leaving scope -[自动调用]（/ zircon / system / ulib / fbl / include / fbl / auto_call.h）在离开范围时运行代码
  - [AutoLock](/zircon/system/ulib/fbl/include/fbl/auto_lock.h)  -[自动锁定]（/ zircon / system / ulib / fbl / include / fbl / auto_lock.h）

FBL has strict controls on memory allocation.  Memory allocation should be explicit, using an AllocChecker to let clients recover from allocationfailures.  In some cases, implicit memory allocation is permitted, butfunctions that implicitly allocate memory must be #ifdef'ed to be unavailablein the kernel. FBL对内存分配有严格的控制。内存分配应该是明确的，使用AllocChecker让客户端从分配失败中恢复。在某些情况下，允许隐式内存分配，但是必须ifif定义隐式分配内存的功能在内核中不可用。

FBL not available outside the Platform Source Tree.  FBL在平台源代码树之外不可用。

 
## ZX  中兴 

ZX contains C++ wrappers for the Zircon [objects](/docs/concepts/objects/objects.md) and [syscalls](/docs/reference/syscalls/README.md).  These wrappers provide type safety and move semanticsfor handles but offer no opinion beyond what's in syscalls.abigen.  At somepoint in the future, we might autogenerate ZX from syscalls.abigen, similar tohow we autogenerate the syscall wrappers in other languages. ZX包含Zircon [objects]（/ docs / concepts / objects / objects.md）和[syscalls]（/ docs / reference / syscalls / README.md）的C ++包装。这些包装器提供了类型安全性并为句柄移动了语义，但除了syscalls.abigen中的内容外，没有提供其他任何意见。在将来的某个时候，我们可能会从syscalls.abigen自动生成ZX，类似于我们以其他语言自动生成syscall包装器的方式。

ZX is part of the Fuchsia SDK.  ZX是Fuchsia SDK的一部分。

 
## FZL  FZL 

FZL is the Fuchsia Zircon Library.  This library provides value-add for common operations involving kernel objects and is free to have opinions about how tointeract with the Zircon syscalls.  If a piece of code has no dependency onZircon syscalls, the code should go in FBL instead. FZL是紫红色锆石图书馆。该库为涉及内核对象的常见操作提供了增值服务，并且可以自由选择如何与Zircon syscall交互。如果一段代码不依赖Zircon系统调用，则该代码应改为FBL。

FZL not available outside the Platform Source Tree.  FZL在平台源代码树之外不可用。

 
## Hermetic C++  封闭C ++ 

We encourage using C++ rather than C as the implementation language throughout Fuchsia.  However, in many instances we require a narrow ABI bottleneck tosimplify the problem of preventing, tracking, or adapting to ABI drift.  Thefirst key way to keep the ABI simple is to base it on a pure C API (which canbe used directly from C++, and via foreign-function interfaces from many otherlanguages) rather than a C++ API.  When we link together a body of code into amodule with a pure C external API and ABI but using C++ internally for itsimplementation, we call that _hermetic C++_. 我们鼓励在整个紫红色中使用C ++而不是C作为实现语言。但是，在许多情况下，我们需要狭窄的ABI瓶颈来简化预防，跟踪或适应ABI漂移的问题。保持ABI简单的第一个关键方法是基于纯C API（可以直接从C ++使用，也可以通过许多其他语言的外函数接口使用它）而不是C ++ API。当我们使用纯C外部API和ABI将代码主体链接到一个模块中，但内部使用C ++来实现时，我们将其称为_hermetic C ++ _。

 
 * The kernel itself could be said to be implemented in hermetic C++.  *内核本身可以说是在封闭C ++中实现的。
 * The [vDSO](/docs/concepts/kernel/vdso.md) is a shared library implemented in hermetic C++.  * [vDSO]（/ docs / concepts / kernel / vdso.md）是使用Hermetic C ++实现的共享库。
 * Fuchsia's [standard C library](/zircon/system/ulib/c), while largely implemented in C, also uses hermetic C++ in its implementation. *紫红色的[标准C库]（/ zircon / system / ulib / c）虽然主要用C实现，但在其实现中也使用了封闭C ++。
 * Most Fuchsia device drivers are implemented in hermetic C++.  *大多数Fuchsia设备驱动程序都是在封闭的C ++中实现的。

It's a hard and fast rule for binaries exported in the Fuchsia's public SDK that **shared libraries must have a pure C API and ABI**.  Such libraries can_and should_ use C++ rather than C in their implementations, and they can useother *statically-linked* libraries with C++ APIs as long as ABI aspects ofthose internal C++ APIs don't leak out into the shared library's public ABI. 对于在Fuchsia的公共SDK中导出的二进制文件，一条硬性规定是**共享库必须具有纯C API和ABI **。这样的库在实现中可以并且应该使用C ++而不是C，并且只要内部C ++ API的ABI方面不会泄漏到共享库的公共ABI中，它们就可以将其他*静态链接*库与C ++ API一起使用。

A "loadable module" (sometimes called a "plug-in" module) is very similar to a shared library.  The same rules about pure a C ABI bottleneck apply forloadable module ABIs.  Fuchsia device drivers are just such loadable modulesthat must meet the driver (pure C) ABI.  Hence, every driver implemented inC++ must use hermetic C++. “可加载模块”（有时称为“插件”模块）与共享库非常相似。关于纯C ABI瓶颈的相同规则适用于可加载模块ABI。紫红色的设备驱动程序就是这样的可加载模块，必须满足驱动程序（纯C）的ABI。因此，在C ++中实现的每个驱动程序都必须使用封闭C ++。

The Fuchsia C++ toolchain provides the full C++17 standard library using the [libc++](https://libcxx.llvm.org/) implementation.  In C++ executables (andshared libraries with a C++ ABI) this is usually dynamically linked, andthat's the default behavior of the compiler.  The toolchain also provides`libc++` for *hermetic static linking* via the `-static-libstdc++` switch tothe compiler (`clang++`).  In the Zircon GN build system, a linking targetsuch as `executable()`, `test()`, or `library()` (with `shared = true`), usesthis line to request the hermetic C++ standard library: 紫红色的C ++工具链使用[libc ++]（https://libcxx.llvm.org/）实现提供了完整的C ++ 17标准库。在C ++可执行文件（以及具有C ++ ABI的共享库）中，这通常是动态链接的，这是编译器的默认行为。该工具链还提供了“ libc ++”，用于通过“ -static-libstdc ++”开关到编译器（“ clang ++”）的“静态静态链接”。在Zircon GN构建系统中，链接目标（例如`executable（）`，`test（）`或`library（）`（具有`shared = true`））使用以下行来请求封闭的C ++标准库：

```gn
    configs += [ "$zx/public/gn/config:static-libc++" ]
```
 

This is **required** in each `library()` that is exported to the public SDK _in binary form_ via `sdk = "shared"`. 这是在每个“ library（）”中“必需”的，这些库通过`sdk =“ shared”以二进制形式导出到公共SDK。

Every `driver()` automatically uses hermetic C++ and so this line is not required for them.  (Drivers cannot depend on their own shared libraries, onlythe dynamic linking environment provided by the driver ABI.) 每个`driver（）`自动使用封闭的C ++，因此它们不需要此行。 （驱动程序不能依赖于它们自己的共享库，而只能依赖于驱动程序ABI提供的动态链接环境。）

