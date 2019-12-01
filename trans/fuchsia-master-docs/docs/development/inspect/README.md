Fuchsia Component Inspection ===== 紫红色成分检查=====

Components in Fuchsia may expose structured information about themselves conforming to the Inspect API. This document describes the concepts ofComponent Inspection, the interface, the C++ language implementationof the interface, and user-facing tools for interacting with componentsthat expose information. 紫红色中的组件可能会暴露符合Inspect API的有关其自身的结构化信息。本文档介绍了组件检查，接口，接口的C ++语言实现以及与暴露信息的组件进行交互的面向用户的工具的概念。

[TOC]  [目录]

 
# Quick Links  快速链接 

**Not sure where to start? [Quick Start](quickstart.md)**  **不知道从哪里开始？ [快速入门]（quickstart.md）**

 
* [iquery](iquery.md) &mdash; The userspace tool for inspecting components.  * [iquery]（iquery.md）mdash;用于检查组件的用户空间工具。
* [Getting started with Inspect](gsw-inspect.md) &mdash; A quick start guide.  * [Inspect入门]（gsw-inspect.md）mdash;快速入门指南。
* [VMO format](vmo-format/README.md) &mdash; Describes the Inspect VMO File Format.  * [VMO格式]（vmo-format / README.md）mdash;描述检查VMO文件格式。
* [Health checks](health.md) &mdash; Describes the health check subsystem.  * [健康检查]（health.md）–描述健康检查子系统。

 
# Concepts  概念 

Components may expose a tree of **Nodes**, each of which has a set of **Properties**. 组件可能会公开一棵“节点”树，每个节点都有一组“属性”。

![Figure: A tree of **Nodes**s](tree.png)  ！[图：一棵**节点**的树]（tree.png）

 
## Node  节点 

A node is an exported entity within a component that may have 0 or more children. Each node has a name, and each child of a nodemust have a unique name among the children. 节点是组件中可能有0个或多个子代的导出实体。每个节点都有一个名称，节点的每个子节点在子节点中必须具有唯一的名称。

![Figure: A **Node**](node.png)  ！[图：一个** Node **]（node.png）

 
## Property  属性 

Nodes may have any number of properties. A property has a string key and a value which may be any one of a number of types: 节点可以具有任意数量的属性。属性具有字符串键和值，该值可以是多种类型中的任何一种：

 
### Numeric Types  数值类型 

 
- `UintProperty` - 64-bit unsigned integer.  -`UintProperty`-64位无符号整数。
- `IntProperty` - 64-bit signed integer.  -`IntProperty`-64位有符号整数。
- `DoubleProperty` - 64-bit floating point value.  -DoubleProperty-64位浮点值。

 
### String Types  字符串类型 

 
- `StringProperty` - UTF-8 string.  -`StringProperty`-UTF-8字符串。
- `ByteVectorProperty` - Vector of bytes.  -`ByteVectorProperty`-字节向量。

 
### Array Types  数组类型 

 
- `UintArray`, `IntArray`, `DoubleArray` - An array of the corresponding numeric type.  -`UintArray`，`IntArray`，`DoubleArray`-相应数值类型的数组。

 
### Histogram Types  直方图类型 

 
- `LinearUintHistogram`, `LinearIntHistogram`, `LinearDoubleHistogram`  -`LinearUintHistogram`，`LinearIntHistogram`，`LinearDoubleHistogram`

A histogram with fixed-size buckets stored in an array.  存储在数组中的固定大小桶的直方图。

 
- `ExponentialUintHistogram`, `ExponentialIntHistogram`, `ExponentialDoubleHistogram`  -`ExponentialUintHistogram`，`ExponentialIntHistogram`，`ExponentialDoubleHistogram`

A histogram with exponentially sized buckets stored in an array.  阵列中存储着指数大小的存储桶的直方图。

 
## Inspect File Format  检查文件格式 

The [Inspect File Format](vmo-format/README.md) is a binary format that supports efficient insertion, modification, and deletion of Nodes andProperties at runtime. Readers take a consistent snapshot of the contentswithout communicating with writers. [检查文件格式]（vmo-format / README.md）是一种二进制格式，支持在运行时高效地插入，修改和删除节点和属性。读者无需与作者沟通即可对内容进行一致的快照。

 
## Filesystem Interface  文件系统接口 

Components by default obtain a reference to their `out/` directory in their hub. 默认情况下，组件在其集线器中获取对其“ out /”目录的引用。

*Top-level* nodes are exposed as VmoFiles in the Hub ending in the extension `.inspect`. It is customary for components to expose their primary or root tree as`out/objects/root.inspect`. *顶级*节点在集线器中以VmoFiles的形式公开，扩展名为`.inspect`。通常，组件将其主树或根树公开为out / objects / root.inspect。

The manager for a component's environment may expose its own information about the component to the hub. For instance, appmgr exposes`system_objects` for each component. 组件环境的管理器可以向集线器公开其有关组件的信息。例如，appmgr为每个组件公开“ system_objects”。

 
# Language Libraries  语言图书馆 

 
## [C++](/zircon/system/ulib/inspect)  [C ++]（/ zircon / system / ulib / inspect） 

The C++ Inspect Library provides full [writing][cpp-1] and [reading][cpp-2] support for the Inspect File Format. C ++ Inspect库为Inspect文件格式提供了完整的[writing] [cpp-1]和[reading] [cpp-2]支持。

Components that write inspect data should refrain from reading that data. Reading requires traversing the entire buffer, which is very expensive. 编写检查数据的组件应避免读取该数据。读取需要遍历整个缓冲区，这非常昂贵。

The `Inspector` class provides a wrapper around creating a new buffer with one root Node that can be added to. Nodes and Properties have typed[wrappers][cpp-3] that automatically delete the underlying data from thebuffer when they go out of scope. Inspector类提供了一个包装，该包装使用一个可以添加到其中的根节点来创建新缓冲区。节点和属性的类型为[wrappers] [cpp-3]，当它们超出范围时会自动从缓冲区中删除基础数据。

The [sys\_inspect][cpp-4] library provides a simple `ComponentInspector` singleton interface to help with the common case of exposing a singlehierarchy from the component. [sys \ _inspect] [cpp-4]库提供了一个简单的`ComponentInspector`单例接口，以帮助解决从组件公开单层次结构的常见情况。

The [health][cpp-5] feature supports exposing structured health information in a format known by health checking tools. [health] [cpp-5]功能支持以健康检查工具已知的格式公开结构化的健康信息。

The [test matchers][cpp-6] library provides GMock matchers for verifying data that is read out of an Inspect hierarchy in tests. [test matchers] [cpp-6]库提供了GMock匹配器，用于验证从测试中从Inspect层次结构中读取的数据。

[cpp-1]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/inspect.h [cpp-2]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/reader.h[cpp-3]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/vmo/types.h[cpp-4]: /sdk/lib/sys/inspect[cpp-5]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/health.h[cpp-6]: /sdk/lib/inspect/testing [cpp-1]：/ zircon / system / ulib / inspect / include / lib / inspect / cpp / inspect.h [cpp-2]：/ zircon / system / ulib / inspect / include / lib / inspect / cpp / reader .h [cpp-3]：/zircon/system/ulib/inspect/include/lib/inspect/cpp/vmo/types.h[cpp-4]：/ sdk / lib / sys / inspect [cpp-5]： /zircon/system/ulib/inspect/include/lib/inspect/cpp/health.h[cpp-6]：/ sdk / lib / inspect / testing

 
### Reading Support  阅读支持 

The [reading library][cpp-reading-1] supports parsing an Inspect File into a [Hierarchy][cpp-reading-2]. `Hierarchy`s contain `NodeValue`sand `PropertyValues`, which are the parsed versions of `Node`s and`Property`s respectively. [阅读库] [cpp-reading-1]支持将检查文件解析为[层次结构] [cpp-reading-2]。 “层次结构”包含“ NodeValue”和“ PropertyValues”，它们分别是“ Node”和“ Property”的解析版本。

The `Hierarchy`'s `NodeValue` is returned by `node()` and child `Hierarchy`s are returned in a vector by `children()`. The `GetByPath`function supports reading a specific child hierarchy by path. “层级”的“ NodeValue”由“ node（）”返回，子级“子层次”由“ children（）”在向量中返回。 GetByPath函数支持按路径读取特定的子层次。

The properties for a particular `NodeValue` are available through the `properties()` accessor. You may determine if a property contains acertain type by passing the corresponding `PropertyValue` type as thetemplate parameter to the `Contains<T>()` method: 通过“ properties（）”访问器可以使用特定“ NodeValue”的属性。您可以通过将相应的“ PropertyValue”类型作为模板参数传递给“ Contains <T>（）”方法来确定属性是否包含某些类型：

```
// Returns true if the first property of the hierarchy's node is an INT value.
if (hierarchy.node().properties()[0].Contains<IntPropertyValue>()) {
  // ...
}
```
 

Use the `Get<T>()` method to obtain the property:  使用`Get <T>（）`方法获取属性：

```
// Get the IntPropertyValue of the first property on the node.
// Note: This causes a runtime exception if the property does not contain
// the given type, crashing the program.
hierarchy.node().properties()[0].Get<IntPropertyValue>();
```
 

You may also switch based on the different possible format types:  您还可以根据不同的可能格式类型进行切换：

```
const auto& property = hierarchy.node().properties()[0];
switch (property.format()) {
  case FormatType::INT:
    const auto& value = property.Get<IntPropertyValue>();
    /* ... */
    break;
  /* ... */
}

Array types may be specially formatted to contain histograms. The
`GetBuckets()` method supports returning an array of histogram buckets
from `{Int,Uint,Double}ArrayValue` types. The array will be empty if
the underlying array is not a specially formatted histogram.
```
 

 

[cpp-reading-1]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/reader.h [cpp-reading-2]: /zircon/system/ulib/inspect/include/lib/inspect/cpp/hierarchy.h [cpp-reading-1]：/ zircon / system / ulib / inspect / include / lib / inspect / cpp / reader.h [cpp-reading-2]：/ zircon / system / ulib / inspect / include / lib / inspect /cpp/hierarchy.h

 
## [Rust](/src/lib/inspect/rust/fuchsia-inspect)  [Rust]（/ src / lib / inspect / rust / fuchsia-inspect） 

The Rust Inspect Library provides full [writing][rust-1] and [reading][rust-2] support for the Inspect File Format. Rust Inspect库为Inspect文件格式提供了完整的[writing] [rust-1]和[reading] [rust-2]支持。

Components that write inspect data should refrain from reading that data. Reading requires traversing the entire buffer, which is very expensive. 编写检查数据的组件应避免读取该数据。读取需要遍历整个缓冲区，这非常昂贵。

The `Inspector` class provides a wrapper around creating a new buffer with one root Node that can be added to. Nodes and Properties have typed[wrappers][rust-3] that automatically delete the underlying data from thebuffer when they go out of scope. Inspector类提供了一个包装，该包装使用一个可以添加到其中的根节点来创建新缓冲区。节点和属性的类型为[wrappers] [rust-3]，当它们超出范围时会自动从缓冲区中删除基础数据。

The [component][rust-4] module supports a simple `inspector` function to handle the common use of exposing a single hierarchy from the component. [component] [rust-4]模块支持简单的“检查器”功能，以处理从组件公开单个层次结构的常见用法。

The [health][rust-5] module supports exposing structured health information in a format known by health checking tools. [health] [rust-5]模块支持以健康检查工具已知的格式公开结构化的健康信息。

The [testing][rust-6] module supports the `assert_inspect_tree!` macro to match Inspect data for testing. [testing] [rust-6]模块支持`assert_inspect_tree！`宏来匹配Inspect数据以进行测试。

[rust-1]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/struct.Inspector.html [rust-2]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/reader/index.html[rust-3]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html[rust-4]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/component/index.html[rust-5]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/health/index.html[rust-6]: https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/testing/index.html [rust-1]：https：//fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/struct.Inspector.html [rust-2]：https：//fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/reader /index.html[rust-3]：https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html[rust-4]：https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect /component/index.html[rust-5]：https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/health/index.html[rust-6]：https://fuchsia-docs.firebaseapp.com /rust/fuchsia_inspect/testing/index.html

 
## [Dart](https://fuchsia.googlesource.com/topaz/+/refs/heads/master/public/dart/fuchsia_inspect/)  [Dart]（https://fuchsia.googlesource.com/topaz/+/refs/heads/master/public/dart/fuchsia_inspect/） 

The Dart Inspect Library provides [write][dart-1] support for the Inspect File Format.  Dart Inspect库为Inspect文件格式提供[write] [dart-1]支持。

The `Inspect` class provides a wrapper around exposing and writing to named Inspect files on the Hub.  Nodes and Properties have typed[wrappers][dart-2]. Inspect类提供了一个包装器，用于暴露和写入集线器上命名的Inspect文件。节点和属性的类型为[包装器] [dart-2]。

Node children and properties are deduplicated automatically by the library, so creating the same named property twice simply returns areference to the previously existing property. 库将自动对节点子级和属性进行重复数据删除，因此，两次创建相同的命名属性只会简单地返回对先前存在的属性的引用。

[Deletion][dart-3] is manual, but it is compatible with Futures and callbacks in Dart:  [Deletion] [dart-3]是手动的，但与Dart中的Futures和callbacks兼容：

```
var item = parent.child('item');
itemDeletedFuture.then(() => item.delete());
```
 

[dart-1]: https://fuchsia-docs.firebaseapp.com/dart/package-fuchsia_inspect_inspect/Inspect-class.html [dart-2]: https://fuchsia-docs.firebaseapp.com/dart/package-fuchsia_inspect_inspect/package-fuchsia_inspect_inspect-library.html[dart-3]: https://fuchsia-docs.firebaseapp.com/dart/package-fuchsia_inspect_inspect/Node/delete.html [dart-1]：https：//fuchsia-docs.firebaseapp.com/dart/package-fuchsia_inspect_inspect/Inspect-class.html [dart-2]：https：//fuchsia-docs.firebaseapp.com/dart/package -fuchsia_inspect_inspect / package-fuchsia_inspect_inspect-library.html [dart-3]：https://fuchsia-docs.firebaseapp.com/dart/package-fuchsia_inspect_inspect/Node/delete.html

 
## Testing  测试中 

[Validator Architecture](/docs/development/inspect/validator/README.md) describes an integration test framework for Inspect language libraries. [Validator Architecture]（/docs/development/inspect/validator/README.md）描述了Inspect语言库的集成测试框架。

 
# Userspace Tools  用户空间工具 

The primary userspace tool is [iquery](iquery.md), which has its own manual page. 主要的用户空间工具是[iquery]（iquery.md），它具有自己的手册页。

