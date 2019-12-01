 
# C Library Readability Rubric  C库可读性规则 

This document describes heuristics and rules for writing C libraries that are published in the Fuchsia SDK. 本文档介绍了在Fuchsia SDK中发布的用于编写C库的试探法和规则。

A different document will be written for C++ libraries. While C++ is almost an extension of C, and has some influence in this document, thepatterns for writing C++ libraries will be quite different than for C. 将为C ++库编写其他文档。虽然C ++几乎是C的扩展，并且在本文档中有一定影响，但是编写C ++库的模式与C的模式将大不相同。

Most of this document is concerned with the description of an interface in a C header. This is not a full C style guide, and haslittle to say about the contents of C source files. Nor is this adocumentation rubric (though public interfaces should be welldocumented). 本文的大部分内容与C标头中的接口说明有关。这不是完整的C样式指南，并且几乎不用说C源文件的内容。该文档规范也没有（尽管应该对公共接口进行充分记录）。

Some C libraries have external constraints that contradict these rules. For instance, the C standard library itself does not followthese rules. This document should still be followed where applicable. 一些C库具有与这些规则相矛盾的外部约束。例如，C标准库本身不遵循这些规则。在适用的情况下，仍应遵循本文档。

[TOC]  [目录]

 
## Goals  目标 

 
### ABI Stability  ABI稳定性 

Some Fuchsia interfaces with a stable ABI will be published as C libraries. One goal of this document is to make it easy for Fuchsiadevelopers to write and to maintain a stable ABI. Accordingly, wesuggest not using certain features of the C language that havepotentially surprising or complicated implications on the ABI of aninterface. We also disallow nonstandard compiler extensions, since wecannot assume that third parties are using any particular compiler,with a handful of exceptions for the DDK described below. 一些具有稳定ABI的Fuchsia接口将作为C库发布。本文档的一个目标是使紫红色的开发人员可以轻松编写并维护稳定的ABI。因此，我们建议不要使用C语言的某些功能，这些功能可能会对接口的ABI带来令人惊讶或复杂的影响。我们也不允许非标准的编译器扩展，因为我们不能假定第三方正在使用任何特定的编译器，但以下描述的DDK有少数例外。

 
### Resource Management  资源管理 

Parts of this document describe best practices for resource management in C. This includes resources, Zircon handles, and any other type ofresource. 本文档的某些部分描述了C语言中资源管理的最佳做法。其中包括资源，Zircon句柄以及任何其他类型的资源。

 
### Standardization  标准化 

We would also like to adopt reasonably uniform standards for Fuchsia C libraries. This is especially true of naming schemes. Out parameterordering is another example of standardization. 我们还想为紫红色C库采用合理统一的标准。命名方案尤其如此。输出参数排序是标准化的另一个示例。

 
### FFI Friendliness  FFI友好 

Some amount of attention is paid to Foreign Function Interface (FFI) friendliness. Many non-C languages support C interfaces. Thesophistication of these FFI systems varies wildly, from essentiallysed to sophisticated libclang-based tooling. Some amount ofconsideration of FFI friendliness went into these decisions. 国外功能接口（FFI）的友好程度引起了很多关注。许多非C语言都支持C接口。这些FFI系统的复杂程度从本质上到复杂的基于libclang的工具都千差万别。这些决定对FFI的友好程度进行了一些考虑。

 
## Language versions  语言版本 

 
### C  C 

Fuchsia C libraries are written against the C11 standard (with a small set of exceptions, such as unix signal support, that are notparticularly relevant to our C library ABI). C99 compliance is not agoal. 紫红色的C库是根据C11标准编写的（有少量例外，例如unix信号支持，与我们的C库ABI无关）。 C99合规性不是过时的。

In particular, Fuchsia C code can use the `<threads.h>` and `<stdatomic.h>` headers from the C11 standard library, as well as the`_Thread_local` and alignment language features. 特别地，紫红色的C代码可以使用C11标准库中的<threads.h>和<stdatomic.h>头文件，以及_Thread_local和对齐语言功能。

The thread locals should use the `thread_local` spelling from `<threads.h>`, rather than the built in `_Thread_local`. Similarly,prefer `alignas` and `alignof` from `<stdalign.h>`, rather than`_Alignas` and `_Alignof`. 线程本机应该使用<threads.h>中的thread_local拼写，而不是内置的_Thread_local。同样，最好从<stdalign.h>中选择“ alignas”和“ alignof”，而不要使用“ _Alignas”和“ _Alignof”。

Note that compilers support flags which may alter the ABI of the code. For instance, GCC has a `-m96bit-long-double` flag which altersthe size of a long double. We assume that such flags are not used. 请注意，编译器支持标志，这些标志可能会更改代码的ABI。例如，GCC具有一个`-m96bit-long-double`标志，该标志会改变long double的大小。我们假定不使用此类标志。

Finally, some libraries (such as Fuchsia's C standard library) in our SDK are a mix of externally defined interfaces and Fuchsia specificextensions. In these cases, we allow some pragmatism. For instance,libc defines functions like `thrd_get_zx_handle` and`dlopen_vmo`. These names are not strictly in accordance with therules below: the name of the library is not a prefix. Doing so wouldmake the names fit less well next to other functions like`thrd_current` and `dlopen`, and so we allow the exceptions. 最后，我们SDK中的某些库（例如Fuchsia的C标准库）是外部定义的接口和Fuchsia特定扩展的混合。在这种情况下，我们允许一些实用主义。例如，libc定义了诸如Thrd_get_zx_handle和dlopen_vmo之类的函数。这些名称与下面的规则并不完全一致：库的名称不是前缀。这样做会使名称不太适合其他函数，例如Thrd_current和dlopen，因此我们允许使用例外。

 
### C++  C ++ 

While C++ is not an exact superset of C, we still design C libraries to be usable from C++. Fuchsia C headers should be compatible with theC++11, C++14, and C++17 standards. In particular, functiondeclarations must be `extern "C"`, as described below. 尽管C ++并非C的确切父集，但我们仍将C库设计为可从C ++使用。紫红色的C标头应与C ++ 11，C ++ 14和C ++ 17标准兼容。特别是，函数声明必须是“ extern“ C”`，如下所述。

C and C++ interfaces should not be mixed in one header. Instead, create a separate `cpp` subdirectory and place C++ interfaces in theirown headers there. C和C ++接口不应混在一个标头中。而是创建一个单独的`cpp`子目录，并将C ++接口放在它们自己的标题中。

 
## Library Layout and Naming  库布局和命名 

A Fuchsia C library has a name. This name determines its include path (as described in the [library naming document]) as well as identifierswithin the library. 紫红色的C库有一个名称。此名称确定其包含路径（如[库命名文档]中所述）以及库中的标识符。

In this document, the library is always named `tag`, and is variously referred to as `tag` or `TAG` or `Tag` or `kTag` to reflect aparticular lexical convention. The `tag` should be a single identifierwithout underscores. The all-lowercase form of a tag is given by theregular expression `[a-z][a-z0-9]*`.  A tag can be replaced by a shorterversion of the library name, for example `zx` instead of `zircon`. 在本文档中，该库始终被命名为“标签”，并被不同地称为“标签”或“标签”或“标签”或“ kTag”以反映特定的词汇约定。标签应该是一个没有下划线的标识符。标签的全部小写形式由正则表达式[a-z] [a-z0-9] *给出。可以用一个较短的库名称版本来代替标签，例如用“ zx”代替“ zircon”。

The include path for a header `foo.h`, as described by the [library naming document], should be `lib/tag/foo.h`. 如[库命名文件]所述，标头`foo.h`的包含路径应​​为`lib / tag / foo.h`。

 
## Header Layout  标题布局 

A single header in a C library contains a few kinds of things.  C库中的单个标头包含几种东西。

 
- A copyright banner  -版权标语
- A header guard  -头球后卫
- A list of file inclusions  -文件包含列表
- Extern C guards  -外部C后卫
- Constant declarations  -常量声明
- Extern symbol declarations  -外部符号声明
  - Including extern function declarations  -包括外部函数声明
- Static inline functions  -静态内联函数
- Macro definitions  -宏定义

 
### Header Guards  标头护卫 

Use #ifndef guards in headers. These look like:  在标头中使用ifndef保护。这些看起来像：

```C
#ifndef SOMETHING_MUMBLE_H_
#define SOMETHING_MUMBLE_H_

// code
// code
// code

#endif // SOMETHING_MUMBLE_H_
```
 

The exact form of the define is as follows:  定义的确切形式如下：

 
- Take the canonical include path to the header  -选择标头的规范包含路径
- Replace all ., /, and - with _  -将所有。，/和-替换为_
- Convert all letters to UPPERCASE  -将所有字母转换为大写
- Add a trailing _  -添加尾随_

For example, the header located in the SDK at `lib/tag/object_bits.h` should have a header guard `LIB_TAG_OBJECT_BITS_H_`. 例如，SDK中位于lib / tag / object_bits.h的标头应具有标头保护LIB_TAG_OBJECT_BITS_H_。

 
### Inclusions  内含物 

Headers should include what they use. In particular, any public header in a library should be safe to include first in a source file. 标头应包括其使用的内容。特别是，库中的任何公共标头都应该安全地首先包含在源文件中。

Libraries can depend on the C standard library headers.  库可以取决于C标准库头。

Some libraries may also depend on a subset of POSIX headers. Exactly which are appropriate is pending a forthcoming libc API review. 一些库也可能依赖于POSIX标头的子集。确切合适的方法有待即将进行的libc API审查。

 
### Constant Definitions  常量定义 

Most constants in a library will be compile-time constants, created via a `#define`. There are also read-only variables, declared via`extern const TYPE NAME;`, as it sometimes is useful to have storagefor a constant (particularly for some forms of FFI). This sectiondescribes how to provide compile time constants in a header. 库中的大多数常量都是通过`define`创建的编译时常量。还有一些只读变量，它们是通过`extern const TYPE NAME;`声明的，因为有时存储一个常量很有用（特别是对于某些形式的FFI）。本节描述如何在标头中提供编译时间常数。

There are several types of compile time constants.  有几种类型的编译时间常数。

 
- Single integer constants  -单整数常量
- Enumerated integer constants  -枚举整数常量
- Floating point constants  -浮点常数

 
#### Single integer constants  单整数常量 

A single integer constants has some `NAME` in a library `TAG`, and its definition looks like the following. 一个整数常量在库“ TAG”中具有一些“ NAME”，其定义如下所示。

```C
#define TAG_NAME EXPR
```
 

where `EXPR` has one of the following forms (for a `uint32_t`)  其中`EXPR`具有以下格式之一（对于`uint32_t`）

 
- `((uint32_t)23)`  -`（（（uint32_t）23）`
- `((uint32_t)0x23)`  -`（（（uint32_t）0x23）`
- `((uint32_t)(EXPR | EXPR | ...))`  -`（（（uint32_t）（EXPR | EXPR | ...））`

 
#### Enumerated integer constants  枚举整数常量 

Given an enumerated set of integer constants named `NAME` in a library `TAG`, a related set of compile-time constants has the following parts. 给定一个名为“ TAG”的库中一个名为“ NAME”的枚举常量集合，一组相关的编译时常量具有以下部分。

First, a typedef to give the type a name, a size, and a signedness. The typedef should be of an explicitly sized integertype. For example, if `uint32_t` is used: 首先，使用typedef为类型赋予名称，大小和签名。 typedef应该是显式大小的整数类型。例如，如果使用`uint32_t`：

```C
typedef uint32_t tag_name_t;
```
 

Each constant then has the form  每个常数具有以下形式

```C
#define TAG_NAME_... EXPR
```
 

where `EXPR` is one of a handful of types of compile-time integer constants (always wrapped in parentheses): 其中，“ EXPR”是少数几种编译时整数常量之一（始终用括号括起来）：

 
- `((tag_name_t)23)`  -`（（（tag_name_t）23）`
- `((tag_name_t)0x23)`  -`（（（tag_name_t）0x23）`
- `((tag_name_t)(TAG_NAME_FOO | TAG_NAME_BAR | ...))`  -`（（（tag_name_t）（TAG_NAME_FOO | TAG_NAME_BAR | ...）））

Do not include a count of values, which is difficult to maintain as the set of constants grows. 不包括值的计数，随着常数集的增长，很难计数。

 
#### Floating point constants  浮点常数 

Floating point constants are similar to single integer constants, except that a different mechanism is used to describe the type. Floatconstants must end in `f` or `F`; double constants have no suffix;long double constants must end in `l` or `L`. Hexadecimal versions offloating point constants are allowed. 浮点常量类似于单个整数常量，不同之处在于使用不同的机制来描述类型。浮点常量必须以“ f”或“ F”结尾； double常量没有后缀； long double常量必须以“ l”或“ L”结尾。允许使用十六进制版本的浮点常量。

```C
// A float constant
#define TAG_FREQUENCY_LOW 1.0f

// A double constant
#define TAG_FREQUENCY_MEDIUM 2.0

// A long double constant
#define TAG_FREQUENCY_HIGH 4.0L
```
 

 
### Function Declarations  功能声明 

Function declarations should all have names beginning with `tag_...`.  函数声明均应以“ tag _...”开头。

Function declarations should be placed in `extern "C"` guards. These are canonically provided by using the `__BEGIN_CDECLS` and`__END_CDECLS` macros from [compiler.h]. 函数声明应放在“ extern“ C”防护中。通过使用[compiler.h]中的`__BEGIN_CDECLS`和`__END_CDECLS`宏可以规范地提供它们。

 
#### Function parameters  功能参数 

Function parameters must be named. For example,  功能参数必须命名。例如，

```C
// Disallowed: missing parameter name
zx_status_t tag_frob_vmo(zx_handle_t, size_t num_bytes);

// Allowed: all parameters named
zx_status_t tag_frob_vmo(zx_handle_t vmo, size_t num_bytes);
```
 

It should be clear which parameters are consumed and which are borrowed. Avoid interfaces in which clients may or may not own aresource after a function call. If this is infeasible, consider notingthe ownership hazard in the name of the function, or one of itsparameters. For example: 应该清楚哪些参数被消耗，哪些参数被借用。避免在函数调用后客户端可能拥有或不拥有aresource的接口。如果不可行，请考虑以功能名称或其参数之一的名义指出所有权风险。例如：

```C
zx_status_t tag_frobinate_subtle(zx_handle_t foo);
zx_status_t tag_frobinate_if_frobable(zx_handle_t foo);
zx_status_t tag_try_frobinate(zx_handle_t foo);
zx_status_t tag_frobinate(zx_handle_t maybe_consumed_foo);
```
 

By convention, out parameters go last in a function's signature, and should be named `out_*`. 按照惯例，out参数位于函数签名的最后，应命名为`out_ *`。

 
#### Variadic functions  可变函数 

Variadic functions should be avoided for everything except printf-like functions. Those functions should document their format stringcontract with the `__PRINTFLIKE` attribute from [compiler.h]. 除类似于printf的函数外，所有其他函数都应避免使用可变参数函数。这些函数应该使用来自[compiler.h]的`__PRINTFLIKE`属性来记录其格式stringcontract。

 
#### Static inline functions  静态内联函数 

Static inline functions are allowed, and are preferable to function-like macros. Inline-only (that is, not also `static`) Cfunctions have complicated linkage rules and few use cases. 允许使用静态内联函数，并且静态内联函数比类函数宏更可取。仅内联（即不是静态）函数具有复杂的链接规则，用例很少。

 
### Types  种类 

Prefer explicitly sized integer types (e.g. `int32_t`) to non-explicitly sized types (e.g. `int` or `unsigned long int`). Anexemption is made for `int` when referring to POSIX file descriptors,and for typedefs like `size_t` from the C or POSIX headers. 优先使用显式大小的整数类型（例如int32_t）而不是非显式大小的类型（例如int或unsigned long int）。当引用POSIX文件描述符时，对`int`进行豁免，对C或POSIX标头中的诸如`size_t`这样的typedef进行豁免。

When possible, pointer types mentioned in interfaces should refer to specific types. This includes pointers to opaque structs. `void*` isacceptable for referring to raw memory, and to interfaces that passaround opaque user cookies or contexts. 如果可能，接口中提到的指针类型应引用特定的类型。这包括指向不透明结构的指针。 “ void *”对于引用原始内存以及绕过不透明用户cookie或上下文的接口都是可以接受的。

 
#### Opaque/Explicit types  不透明/显式类型 

Defining an opaque struct is preferable to using `void*`. Opaque structs should be declared like: 定义一个不透明的结构比使用`void *`更可取。不透明结构应声明为：

```C
typedef struct tag_thing tag_thing_t;
```
 

Exposed structs should be declared like:  暴露的结构应声明为：

```C
typedef struct tag_thing {
} tag_thing_t;
```
 

 
#### Reserved fields  保留栏位 

Any reserved fields in a struct should be documented as to the purpose of the reservation. 结构中的任何保留字段都应记录有关保留目的的信息。

A future version of this document will give guidance as to how to describe string parameters in C interfaces. 本文档的将来版本将提供有关如何在C接口中描述字符串参数的指导。

 
#### Anonymous types  匿名类型 

Top-level anonymous types are not allowed. Anonymous structures and unions are allowed inside other structures, and inside functionbodies, as they are then not part of the top level namespace. Forinstance, the following contains an allowed anonymous union. 不允许使用顶级匿名类型。匿名结构和联合在其他结构和功能体内部是允许的，因为它们不属于顶级名称空间。例如，以下内容包含允许的匿名联合。

```C
typedef struct tag_message {
    tag_message_type_t type;
    union {
        message_foo_t foo;
        message_bar_t bar;
    };
} tag_message_t;
```
 

 
#### Function typedefs  函数类型 

Typedefs for function types are permitted.  允许使用函数类型的Typedef。

Functions should not overload return values with a `zx_status_t` on failure and a positive success value. Functions should not overloadreturn values with a `zx_status_t` that contains additional values notdescribed in [zircon/errors.h]. 函数不应在失败时使用“ zx_status_t”重载返回值，且成功值为正。函数不应使用`zx_status_t'重载返回值，该值包含[zircon / errors.h]中未描述的其他值。

 
#### Status return  状态返回 

Prefer `zx_status_t` as a return value to describe errors relating to Zircon primitives and to I/O. 最好使用zx_status_t作为返回值来描述与Zircon基元和I / O有关的错误。

 
## Resource Management  资源管理 

Libraries can traffic in several kinds of resources. Memory and Zircon handles are examples of resources common across manylibraries. Libraries may also define their own resources withlifetimes to manage. 图书馆可以贩运多种资源。内存和Zircon句柄是许多库中共有的资源示例。图书馆还可以定义自己的资源，并终身管理。

Ownership of all resources should be unambiguous. Transfer of resources should be explicit in the name of a function. For example,`create` and `take` connote a function transferring ownership. 所有资源的所有权应明确。资源的传递应在函数名称中明确。例如，“创建”和“获取”表示转移所有权的函数。

Libraries should be memory tight. Memory allocated by a function like `tag_thing_create` should released via `tag_thing_destroy` or somesuch, not via `free`. 库应保持良好的内存状态。由诸如“ tag_thing_create”之类的功能分配的内存应通过“ tag_thing_destroy”或类似方式释放，而不是通过“ free”释放。

Libraries should not expose global variables. Instead, provide functions to manipulate that state. Libraries with process-globalstate must be dynamically linked, not statically. A common pattern isto split a library into a stateless static part, containing almost allof the code, and a small dynamic library holding global state. 库不应公开全局变量。而是提供功能来操纵该状态。具有process-globalstate的库必须动态链接，而不是静态链接。一种常见的模式是将一个库分成几乎包含所有代码的无状态静态部分和一个具有全局状态的小型动态库。

In particular, the `errno` interface (which is a global thread-local global) should be avoided in new code. 特别是，在新代码中应避免使用errno接口（它是全局线程局部全局变量）。

 
## Linkage  连锁 

The default symbol visibility in a library should be hidden. Use either an allowlist of exported symbols, or explicit visibilityannotations on symbols to exported. 库中的默认符号可见性应隐藏。使用已导出符号的允许列表，或对要导出的符号使用显式可见性注释。

C libraries must not export C++ symbols.  C库不得导出C ++符号。

 
## Evolution  演化 

 
### Deprecation  弃用 

Deprecated functions should be marked with the __DEPRECATED attribute from [compiler.h]. They should also be commented with a descriptionabout what to do instead, and a bug tracking the deprecation. 不推荐使用的功能应使用[compiler.h]中的__DEPRECATED属性进行标记。还应该给他们提供注释，说明如何处理，以及跟踪弃用的错误。

 
## Disallowed or Discouraged Language Features  禁止或不鼓励使用的语言功能 

This section describes language features that cannot or should not be used in the interfaces to Fuchsia's C libraries, and the rationalesbehind the decisions to disallow them. 本节描述了在Fuchsia的C库的接口中不能使用或不应该使用的语言功能，以及禁止使用它们的决策依据。

 
### Enums  枚举 

C enums are banned. They are brittle from an ABI standpoint.  禁止使用枚举。从ABI的角度来看，它们很脆弱。

 
- The size of integer used to represent a constant of enum type is compiler (and compiler flag) dependent. -用于表示枚举类型常量的整数大小取决于编译器（和编译器标志）。
- The signedness of an enum is brittle, as adding a negative value to an enumeration can change the underlying type. -枚举的符号很脆弱，因为向枚举添加负值可以更改基础类型。

 
### Bitfields  位域 

C's bitfields are banned. They are brittle from an ABI standpoint, and have a lot of nonintuitive sharp edges. C位字段被禁止。从ABI的角度来看，它们很脆弱，并且具有很多不直观的尖锐边缘。

Note that this applies to the C language feature, not to an API which exposes bit flags. The C bitfield feature looks like: 请注意，这适用于C语言功能，不适用于公开位标志的API。 C位域功能如下所示：

```C
typedef struct tag_some_flags {
    // Four bits for the frob state.
    uint8_t frob : 4;
    // Two bits for the grob state.
    uint8_t grob : 2;
} tag_some_flags_t;
```
 

We instead prefer exposing bit flags as compile-time integer constants. 相反，我们更喜欢将位标志公开为编译时整数常量。

 
### Empty Parameter Lists  空参数列表 

C allows for function `with_empty_parameter_lists()`, which are distinct from `functions_that_take(void)`. The first means "take anynumber and type of parameters", while the second means "take zeroparameters". We ban the empty parameter list for being too dangerous. C允许使用函数`with_empty_parameter_lists（）`，这与`functions_that_take（void）`不同。第一个表示“采用任意数量和类型的参数”，第二个表示“采用零参数”。我们禁止空参数列表过于危险。

 
### Flexible Array Members  灵活阵列成员 

This is the C99 feature which allows declaring an incomplete array as the last member of a struct with more than one parameter. For example: 这是C99功能，它允许将不完整的数组声明为具有多个参数的结构的最后一个成员。例如：

```C
typedef struct foo_buffer {
    size_t length;
    void* elements[];
} foo_buffer_t;
```
 

As an exception, DDK structures are allowed to use this pattern when referring to an external layout that fits this header-plus-payloadpattern. 作为例外，在引用适合此header-plus-payloadpattern的外部布局时，允许DDK结构使用此模式。

The similar GCC extension of declaring a 0-sized array member is similarly disallowed. 类似地，不允许声明0大小的数组成员的类似GCC扩展。

 
### Module Maps  模块图 

These are a Clang extension to C-like languages which attempt to solve many of the issues with header-driven compilation. While the Fuchsiatoolchain team is very likely to invest in these in the future, wecurrently do not support them. 这些是C语言类的Clang扩展，它试图解决标头驱动的编译中的许多问题。虽然Fuchsiatoolchain团队很可能会在未来进行投资，但目前我们不支持它们。

 
### Compiler Extensions  编译器扩展 

These are, by definition, not portable across toolchains.  根据定义，这些工具不能跨工具链移植。

This in particular includes packed attributes or pragmas, with one exception for the DDK. 这特别包括打包的属性或实用说明，但DDK除外。

DDK structures often reflect an external layout that does not match the system ABI. For instance, it may refer to an integer field that isless aligned than required by the language. This can be expressed viacompiler extensions such as pragma pack. DDK结构通常反映的外部布局与系统ABI不匹配。例如，它可能引用一个整数字段，该整数字段的对齐方式比语言要求的对齐方式少。这可以通过编译器扩展（例如，pragma pack）来表示。

