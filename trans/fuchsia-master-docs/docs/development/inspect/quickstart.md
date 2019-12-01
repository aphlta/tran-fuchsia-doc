Inspect Quick Start ===== 检查快速入门=====

 

[TOC]  [目录]

This document is a guide on how to get started with [Component Inspection](README.md) depending on your needs: 本文档是有关如何根据需要开始使用[Component Inspection]（README.md）的指南：

**I want to learn more about Inspect concepts**  **我想了解有关Inspect概念的更多信息**

Read [Getting Started with Inspect](gsw-inspect.md) and the [README](README.md). 阅读[Inspect入门]（gsw-inspect.md）和[README]（README.md）。

**I want to know how to use the iquery tool**  **我想知道如何使用iquery工具**

Read the [iquery manual](iquery.md). For detailed examples of usage, see [Getting Started with Inspect](gsw-inspect.md). 阅读[iquery手册]（iquery.md）。有关用法的详细示例，请参见[Inspect入门]（gsw-inspect.md）。

This document provides a simplified example of iquery below.  本文档在下面提供了iquery的简化示例。

**I have an existing or new component, and I want to support inspection.**  **我有一个现有或新组件，我想支持检查。**

Continue reading this document.  继续阅读本文档。

 
# Quick Start  快速开始 

See below for the quick start guide in your language of choice.  请参阅以下有关您选择的语言的快速入门指南。

 
## C++  C ++ 

 
### Setup  设定Note: If you need to support dynamic values, see [Dynamic Value Support](#dynamic-value-support). If you are unsure, keep reading. 注意：如果需要支持动态值，请参阅[动态值支持]（动态值支持）。如果不确定，请继续阅读。

This section assumes you are writing an asynchronous component and that some part of your component (typically `main.cc`) looks like this: 本节假定您正在编写一个异步组件，并且该组件的某些部分（通常是“ main.cc”）如下所示：

```
async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
auto component_context = sys::ComponentContext::Create();
// ...
loop.Run();
```
 

This sets up an async loop, creates a `ComponentContext` wrapping handles provided by the runtime, and then runs that loop following some otherinitialization work. 这将建立一个异步循环，创建一个由运行时提供的“ ComponentContext”包装句柄，然后在执行其他一些初始化工作之后运行该循环。

**Add the following include**  **添加以下内容**

```
#include <lib/sys/inspect/cpp/component.h>
```
 

**Change your initialization code to look like the following:**  **将您的初始化代码更改为如下所示：**

```
async::Loop loop(&kAsyncLoopConfigAttachToCurrentThread);
auto component_context = sys::ComponentContext::Create();
auto inspector =
      std::make_unique<sys::ComponentInspector>(component_context.get());
inspect::Node& root_node = inspector->root();
// ...
loop.Run();
```
 

You are now using Inspect! To add some data and see it in action, try adding the following:  您现在正在使用Inspect！要添加一些数据并查看实际效果，请尝试添加以下内容：

```
// Important: Make sure to hold on to hello_world_property and don't let it go out of scope.
auto hello_world_property = root_node.CreateStringProperty("hello", "world");
```
 

See [Viewing Inspect Data](#viewing-inspect-data) below to view what you are now exporting.  请参阅下面的[查看检查数据]（viewing-inspect-data）以查看您现在要导出的内容。

See [Supported Data Types](#supported-data-types) for a full list of data types you can try.  有关可尝试使用的数据类型的完整列表，请参见[支持的数据类型]（支持的数据类型）。

Want to test your Inspect integration? Include [lib/inspect/testing/cpp/inspect.h][testing-header]in your unit test for a full set of matchers. See [this example][vmo-example] of how it is used. 是否想测试您的Inspect集成？在单元测试中包括[lib / inspect / testing / cpp / inspect.h] [testing-header]以获取一整套匹配器。有关用法，请参见[此示例] [vmo-example]。

[testing-header]: /sdk/lib/inspect/testing [vmo-example]: /src/sys/appmgr/integration_tests/inspect/test-vmo.cc [测试标题]：/ sdk / lib / inspect / testing [vmo-example]：/ src / sys / appmgr / integration_tests / inspect / test-vmo.cc

Read on to learn how Inspect is meant to be used in C++.  继续阅读以了解Inspect如何在C ++中使用。

 
#### Dynamic Value Support  动态价值支持 

Certain features, such as LazyProperty, LazyMetric, and ChildrenCallback are deprecated, but a replacement is on the way (CF-761). If you determinethat you need one of these data types, you may use the deprecated APIby replacing the setup code with the following: 某些功能（例如LazyProperty，LazyMetric和ChildrenCallback）已被弃用，但即将取代（CF-761）。如果确定需要这些数据类型之一，则可以使用不赞成使用的API，方法是将安装代码替换为以下内容：

```
#include "src/lib/inspect_deprecated/inspect.h"

// Legacy work required to expose an inspect hierarchy over FIDL.
auto root = component::ObjectDir::Make("root");
fidl::BindingSet<fuchsia::inspect::deprecated::Inspect> inspect_bindings_;
component_context->outgoing()->GetOrCreateDirectory("objects")->AddEntry(
    fuchsia::inspect::deprecated::Inspect::Name_,
    std::make_unique<vfs::Service>(
        inspect_bindings_.GetHandler(root.object().get())));
auto root_node = inspect::Node(root);
```
 

 
### C++ Library Concepts  C ++库概念 

Now that you have a `root_node` you may start building your hierarchy. This section describes some important concepts and patternsto help you get started. 现在您有了一个“ root_node”，您可以开始构建层次结构。本节介绍一些重要的概念和模式以帮助您入门。

 
* A Node may have any number of key/value pairs called **Properties**.  *节点可以具有任意数量的称为“属性”的键/值对。
* The key for a Value is always a UTF-8 string, the value may be one of the supported types below.  *值的键始终是UTF-8字符串，该值可能是以下受支持的类型之一。
* A Node may have any number of children, which are also Nodes.  *一个节点可以有任意数量的子节点，它们也是节点。

The code above gives you access to a single node named "root". `hello_world_property` is a Property that contains a string value(aptly called a **StringProperty**). 上面的代码使您可以访问名为“ root”的单个节点。 “ hello_world_property”是一个包含字符串值（通常称为** StringProperty **）的属性。

 
* Values and Nodes are created under a parent Node.  *值和节点在父节点下创建。

Class `Node` has creator methods for every type of supported value. `hello_world_property` was created using`CreateStringProperty`. You could create a child under the root nodeby calling `root_node.CreateChild("child name")`. Note that names mustalways be UTF-8 strings. Node类具有每种受支持值的创建者方法。 hello_world_property是使用CreateStringProperty创建的。您可以通过调用`root_node.CreateChild（“ child name”）`在根节点下创建一个子级。请注意，名称必须始终为UTF-8字符串。

 
* Values and Nodes have strict ownership semantics.  *值和节点具有严格的所有权语义。

`hello_world_property` owns the Property. When it is destroyed (goes out of scope) the underlying Property is deleted and no longer presentin your component's Inspect output. This is true for Metrics and childNodes as well. “ hello_world_property”拥有该财产。销毁（超出范围）时，基础属性将被删除，并且不再出现在组件的Inspect输出中。度量标准和childNode也是如此。

If you are creating a value that doesn't need to be modified, use a [`ValueList`](/zircon/system/ulib/inspect/include/lib/inspect/cpp/value_list.h)to keep them alive until they are no longer needed. 如果要创建不需要修改的值，请使用[`ValueList`]（/ zircon / system / ulib / inspect / include / lib / inspect / cpp / value_list.h）使它们保持活动状态，直到它们生效不再需要。

 
* Inspection is best-effort.  *检查是最大的努力。

Due to space limitations, the Inspect library may be unable to satisfy a `Create` request. This error is not surfaced to your code: you willreceive a Node/Metric/Property object for which the methods are no-ops. 由于篇幅所限，Inspect库可能无法满足“创建”请求。该错误不会在您的代码中浮出水面：您将收到一个Node / Metric / Property对象，其方法是无操作的。

 
* Pattern: Pass in child Nodes to child objects.  *模式：将子节点传递给子对象。

It is useful to add an `inspect::Node` argument to the constructors for your own classes. The parent object, which should own its own`inspect::Node`, may then pass in the result of `CreateChild(...)`to its children when they are constructed: 为自己的类的构造函数添加一个`inspect :: Node`参数是很有用的。父对象应该拥有自己的`inspect :: Node`，然后可以在构造子对象时将'CreateChild（...）`的结果传递给子对象：

```
class Child {
  public:
    Child(inspect::Node my_node) : my_node_(std::move(my_node)) {
      // Create a string that doesn't change, and emplace it in the ValueList
      my_node_.CreateString("version", "1.0", &values_);
      // Create metrics and properties on my_node_.
    }

  private:
    inspect::Node my_node_;
    inspect::StringProperty some_property_;
    inspect::ValueList values_;
    // ... more properties and metrics
};

class Parent {
  public:
    // ...

    void AddChild() {
      // Note: inspect::UniqueName returns a globally unique name with the specified prefix.
      children_.emplace_back(my_node_.CreateChild(inspect::UniqueName("child-")));
    }

  private:
    std::vector<Child> children_;
    inspect::Node my_node_;
};
```
 

 
## Rust  锈 

 
### Setup  设定 

This section assumes you are writing an asynchronous component and that some part of your component (typically main.rs) looks similar to this: 本节假定您正在编写一个异步组件，并且该组件的某些部分（通常是main.rs）看起来与此类似：

```
#[fasync::run_singlethreaded]
async fn main() -> Result<(), Error> {
  ...
  let mut fs = ServiceFs::new_local();
  ...
  Ok(())
}
```
 

Add the following to your initialization code:  将以下内容添加到您的初始化代码中：

```
// This creates the root of an inspect tree.
let inspector = inspect::Inspector::new();

// This serves the inspect Tree to the default path for reading at the standard
// location "/diagnostics/fuchsia.inspect.Tree".
inspector.serve(&mut fs)?;

// This will give you a reference to the root node of the inspect tree.
let root = inspector.root();
```
 

Don't forget to `use fuchsia_inspect as inspect;`!  不要忘记使用fuchsia_inspect作为检查对象！

Now you can use inspect! For example try the following:  现在您可以使用检查！例如，尝试以下操作：

```
let hello_world_property = inspect.create_string("hello", "world!");
```
 

See [this example](/garnet/examples/rust/inspect-rs/src/main.rs) for further learning of other types offered by the API. 请参阅[此示例]（/ garnet / examples / rust / inspect-rs / src / main.rs），以进一步了解API提供的其他类型。

To test your inspect code, you can use `assert_inspect_tree`:  要测试您的检查代码，可以使用`assert_inspect_tree`：

```
assert_inspect_tree!(inspector, root: {
  child1: {
    some_property_name: 1.0,
    another_property: "example",
    children: {},
  }
});
```
 

Learn more about [testing](/src/lib/inspect/rust/fuchsia-inspect/src/testing.rs) inspect.  了解有关[测试]（/ src / lib / inspect / rust / fuchsia-inspect / src / testing.rs）检查的更多信息。

See [the docs](https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html) to learn about other methods offered by the Rust API. 请参阅[docs]（https://fuchsia-docs.firebaseapp.com/rust/fuchsia_inspect/index.html），以了解Rust API提供的其他方法。

See [Viewing Inspect Data](#viewing-inspect-data) below to view what you are now exporting.  请参阅下面的[查看检查数据]（viewing-inspect-data）以查看您现在要导出的内容。

See [Supported Data Types](#supported-data-types) for a full list of data types you can try.  有关可尝试使用的数据类型的完整列表，请参见[支持的数据类型]（支持的数据类型）。

 
### Rust Library Concepts  锈库概念 

Refer to [C++ Library Concepts](#c_library-concepts), as similar concepts apply in Rust. 请参阅[C ++库概念]（c_library-concepts），因为类似的概念也适用于Rust。

 

 
## Dart  镖 

This example obtains and adds several data types and nested children to the root Inspect node. 本示例获取并向根Inspect节点添加几种数据类型和嵌套子代。

`BUILD.gn`:  `BUILD.gn`：

```
flutter_app("inspect_mod") {
[...]
  deps = [
    [...]
    "//topaz/public/dart/fuchsia_inspect",
    [...]
  ]
[...]

```
 

`root_intent_handler.dart`:  `root_intent_handler.dart`：

```dart {highlight="lines:6"}
import 'package:fuchsia_inspect/inspect.dart' as inspect;
[...]
class RootIntentHandler extends IntentHandler {
  @override
  void handleIntent(Intent intent) {
    var inspectNode = inspect.Inspect().root;
    runApp(InspectExampleApp(inspectNode));
  }
}
```
 

`inspect_example_app.dart`:  `inspect_example_app.dart`：

```dart {highlight="lines:4,7-10,16"}
import 'package:fuchsia_inspect/inspect.dart' as inspect;

class InspectExampleApp extends StatelessWidget {
  final inspect.Node _inspectNode;

  InspectExampleApp(this._inspectNode) {
    _inspectNode.stringProperty('greeting').setValue('Hello World');
    _inspectNode.doubleProperty('double down')..setValue(1.23)..add(2);
    _inspectNode.intProperty('interesting')..setValue(123)..subtract(5);
    _inspectNode.byteDataProperty('bytes').setValue(ByteData(4)..setUint32(0, 0x01020304));
  }
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: _InspectHomePage(
          inspectNode: _inspectNode.child('home-page')),
      [...]
  }
```
 

You can call `delete()` on a Node or Property when you're done with it. Deleting a node deletes everything under it. 完成操作后，您可以在节点或属性上调用`delete（）`。删除节点会删除其下的所有内容。

`delete()` can also be triggered by a Future completing or broadcast Stream closing: `delete（）`也可以由将来完成或广播流关闭来触发：

```dart
var answerFuture = _answerFinder.getTheAnswer();
var wait = _inspectNode.stringProperty('waiting')..setValue('for a hint');
answerFuture.whenComplete(wait.delete);

stream.listen((_) {}, onDone: node.delete);

// FIDL proxies contain a future that completes when the connection closes:
final _proxy = my_fidl_import.MyServiceProxy();
_proxy.ctrl.whenClosed.whenComplete(node.delete);
```
 

 
# Viewing Inspect Data  查看检查数据 

You can use the [`iquery`](iquery.md) tool to view the Inspect data you exported from your component by looking through the Hub. 您可以使用[`iquery`]（iquery.md）工具查看通过从集线器查看的从组件导出的Inspect数据。

This section assumes you have SSH access to your running Fuchsia system and that you started running your component. We will use the name`my_component.cmx` as a placeholder for the name of your component. 本部分假定您具有对正在运行的Fuchsia系统的SSH访问权限，并且已开始运行组件。我们将使用名称“ my_component.cmx”作为占位符代表您的组件名称。

 
## Find your Inspect endpoint  查找您的检查端点 

Try the following:  请尝试以下操作：

```
# This prints all Inspect endpoints on the system.
$ iquery --find /hub

# This filters the above list to only print your component.
$ iquery --find /hub | grep my_component.cmx
```
 

> Under the listed directories you will see some paths including > "system\_objects." This Inspect data is placed there by the Component Runtime> itself. >在列出的目录下，您将看到一些路径，包括>“ system \ _objects”。该检查数据由“组件运行时”本身放置在此处。

Your component's endpoint will be listed as `<path>/my_component.cmx/<id>/out/inspect/root.inspect`.  您组件的端点将列为“ <路径> /my_component.cmx/ <id> /out/inspect/root.inspect”。

Note: If you followed [Dynamic Value Support](#dynamic-value-support) above, "root.inspect" will be missing. 注意：如果您遵循上面的[动态值支持]（动态值支持），则“ root.inspect”将丢失。

 
## Read your Inspect data  读取您的检查数据 

Navigate to the `out/` directory that was printed above, and run:  导航到上面打印的`out /`目录，然后运行：

```
$ iquery --recursive root.inspect

# OR, if you used Dynamic Values:
$ iquery --recursive .
```
 

This will print out the following if you followed the suggested steps above:  如果按照上述建议的步骤进行操作，则会打印出以下内容：

```
root:
  hello = world
```
 

 
# Supported Data Types  支持的数据类型 

Type | Description | Notes -----|-------------|-------IntMetric | A metric containing a signed 64-bit integer. | All LanguagesUIntMetric | A metric containing an unsigned 64-bit integer. | Not supported in DartDoubleMetric | A metric containing a double floating-point number. | All Languages{Int,Double,UInt}Array | An array of metric types, includes typed wrappers for various histograms. | Same language support as base metric typeStringProperty | A property with a UTF-8 string value. | All LanguagesByteVectorProperty | A property with an arbitrary byte value. | All LanguagesNode | A node under which metrics, properties, and more nodes may be nested. | All LanguagesLink | Instantiates a complete tree of Nodes dynamically. | IN PROGRESS(CF-761): This will replace Lazy metrics, properties, and children 类型描述注释----- | ------------- | --- IntMetric |包含带符号的64位整数的度量。 |所有语言UIntMetric |包含无符号64位整数的指标。 | DartDoubleMetric不支持|包含双浮点数的指标。 |所有语言{Int，Double，UInt}数组|度量标准类型数组，包括各种直方图的类型化包装器。 |与基本度量标准类型相同的语言支持具有UTF-8字符串值的属性。 |所有语言ByteVectorProperty |具有任意字节值的属性。 |所有语言可以在其下嵌套度量，属性和更多节点的节点。 |所有语言链接|动态实例化完整的节点树。 |正在进行中（CF-761）：这将取代惰性指标，属性和子级

