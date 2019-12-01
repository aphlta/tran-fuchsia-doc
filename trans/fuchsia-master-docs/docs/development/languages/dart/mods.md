 
# Flutter Module Development  颤振模块开发 

TODO(MS-2346): Update documentation below.  TODO（MS-2346）：更新以下文档。

This directory demonstrates how you create modules with Dart and Flutter. At the moment this document assumes that every module gets built as part of the corefuchsia build and included in the bootfs. 该目录演示了如何使用Dart和Flutter创建模块。目前，该文档假设每个模块都是corefuchsia构建的一部分，并包含在bootfs中。

 
# Example Modules  示例模块 

 
## Hello  你好 

(More samples located in `//topaz/examples/ui/`)  （更多示例位于`// topaz / examples / ui /`中）

This example demonstrates how to create a minimal flutter module and implement the `Module` interface. It shows a simple flutter text widget displaying "hello"on the screen. 这个例子演示了如何创建一个最小的颤动模块并实现`Module`接口。它显示了一个简单的颤动文本窗口小部件，在屏幕上显示“ hello”。

 
## Running the Examples on Fuchsia  在紫红色上运行示例 

You can run an example module without going through the full-blown session shell. The available URLs for flutter module examples are: 您可以运行示例模块，而无需经历成熟的会话外壳。 flutter模块示例的可用URL是：

 
*   `hello_mod`  *`hello_mod`

After a successful build of fuchsia, type the following command from the zx console to run the basemgr with the dev session shell: 紫红色成功构建后，从zx控制台键入以下命令，以使用dev会话shell运行basemgr：

```sh
killall scenic  # Kills all other mods.
basemgr --session_shell=dev_session_shell --session_shell_args=--root_module=hello_mod
```
 

 
# Basics  基本 

A flutter module is a flutter app which uses ModuleDriver.  抖动模块是使用ModuleDriver的抖动应用程序。

Below we reproduce the contents of `main()` from that example:  下面，我们从该示例复制`main（）`的内容：

```dart
final ModuleDriver _driver = ModuleDriver();

void main() {
  setupLogger(name: 'Hello mod');

  _driver.start().then((ModuleDriver driver) {
      log.info('Hello mod started');
    });

  runApp(
    MaterialApp(
      title: 'Hello mod',
      home: ScopedModel<_MyModel>(
        model: _MyModel(),
        child: _MyScaffold(),
      ),
    ),
  );
}
```
 

 
# Importing Packages  导入包 

 
## Adding Dependency to BUILD.gn  将依赖项添加到BUILD.gn 

To import a dart package written within the fuchsia tree, the dependency should be added to the project's `BUILD.gn`. The `BUILD.gn` file for the hello_modexample looks like this: 要导入在紫红色的树中编写的dart包，应将依赖项添加到项目的“ BUILD.gn”中。 hello_modexample的`BUILD.gn`文件如下所示：

```gn
import("//topaz/runtime/flutter_runner/flutter_app.gni")

flutter_app("hello_mod") {
  main_dart = "main.dart"
  package_name = "hello_mod"
  fuchsia_package_name = "hello_mod"
  deps = [
    "//topaz/public/dart/widgets:lib.widgets",
    "//topaz/public/lib/app_driver/dart",
  ]
}
```
 

There are two types of dart packages we can include as `BUILD.gn` dependencies.  我们可以将两种类型的dart程序包作为“ BUILD.gn”依赖项包括在内。

 
### 1. Normal Dart Packages  1.普通飞镖包装 

Any third-party dart packages, or regular dart packages manually written in the fuchsia tree. Import them with their relative paths from the `<fuchsia_root>`directory followed by two slashes. Third-party dart packages are usually locatedat `//third_party/dart-pkg/pub/<package_name>`. 在紫红色的树中手动编写的任何第三方dart程序包或常规dart程序包。从<fuchsia_root>目录中导入它们及其相对路径，后跟两个斜杠。第三方dart软件包通常位于`// third_party / dart-pkg / pub / <package_name>`。

 
### 2. FIDL-Generated Dart Bindings  2. FIDL生成的Dart绑定 

To use any FIDL generated dart bindings, you need to first look at the `BUILD.gn` defining the `fidl` target that contains the desired `.fidl` file.For example, let's say we want to import and use the `module.fidl` file (locatedin `//peridot/public/lib/module/fidl/`) in our dart code. We should firstlook at the `BUILD.gn` file, in this case `//peridot/public/lib/BUILD.gn`. Inthis file we can see that the `module.fidl` file is included in the`fidl("fidl")` target. 要使用FIDL生成的飞镖绑定，首先需要查看BUILD.gn定义包含所需的.fidl文件的fidl目标，例如，假设我们要导入并使用模块.fidl`文件（位于// peridot / public / lib / module / fidl /`中）。我们应该首先查看`BUILD.gn`文件，在这种情况下为`// peridot / public / lib / BUILD.gn`。在此文件中，我们可以看到`module.fidl`文件包含在`fidl（“ fidl”）`目标中。

```gn
fidl("fidl") {
  sources = [
    ...
    "module/fidl/module.fidl",   # This is the fidl we want to use for now.
    ...
  ]
}
```
 

This means that we need to depend on this group of fidl files. In our module's `BUILD.gn`, we can add the dependency with the following syntax: 这意味着我们需要依赖于这组fidl文件。在模块的“ BUILD.gn”中，我们可以使用以下语法添加依赖项：

`"//<dir>:<fidl_target_name>_dart"`  `“ // <目录>：<fidl_target_name> _dart”`

Once this is done, we can use all the protocols defined in `.fidl` files contained in this `story` fidl target from our code. 完成此操作后，我们可以使用代码中此“故事” fidl目标中包含的“ .fidl”文件中定义的所有协议。

 
## Importing in Dart Code  导入Dart代码 

Once the desired package is added as a BUILD.gn dependency, the dart files in those packages can be imported in our dart code. Importing dart packages infuchsia looks a bit different than normal dart packages. Let's look at theimport statements in `main.dart` of the hello_world example. 将所需的软件包作为BUILD.gn依赖项添加后，可以将这些软件包中的dart文件导入到我们的dart代码中。导入飞镖包的紫红色看上去与普通飞镖包有些不同。让我们来看一下hello_world示例的`main.dart`中的import语句。

```dart
import 'package:lib.app.dart/app.dart';
import 'package:lib.app.fidl/service_provider.fidl.dart';
import 'package:apps.modular.services.story/link.fidl.dart';
import 'package:apps.modular.services.module/module.fidl.dart';
import 'package:apps.modular.services.module/module_context.fidl.dart';
import 'package:lib.fidl.dart/bindings.dart';

import 'package:flutter/widgets.dart';
```
 

To import things in the fuchsia tree, we use dots (`.`) instead of slashes (`/`) as path delimiter. For FIDL-generated dart files, we add `.dart` at the end ofthe corresponding fidl file path. (e.g. `module.fidl.dart`) 要在紫红色的树中导入东西，我们使用点（`.`）而不是斜杠（`/`）作为路径定界符。对于FIDL生成的dart文件，我们在相应的fidl文件路径的末尾添加`.dart`。 （例如`module.fidl.dart`）

 
# Using FIDL Dart Bindings  使用FIDL Dart绑定 

See the [FIDL tutorial](../fidl/tutorial/tutorial-dart.md).  请参阅[FIDL教程]（../ fidl / tutorial / tutorial-dart.md）。

 
## Things to Watch Out For  注意事项 

 
### Handles Can Only Be Used Once  手柄只能使用一次 

Once an `InterfaceHandle<Foo>` is bound to a proxy, the handle cannot be used in other places. Often, in case you have to share the same service with multipleparties (e.g. sharing the same `fuchsia::modular::Link` service across multiplemodules), the service will provide a way to obtain a duplicate handle (e.g.`fuchsia::modular::Link::Dup()`). 一旦将“ InterfaceHandle <Foo>”绑定到代理，该句柄就不能在其他地方使用。通常，如果您必须与多方共享同一服务（例如，跨多个模块共享相同的`fuchsia :: modular :: Link`服务），则该服务将提供一种获取重复句柄的方法（例如，`fuchsia :: modular”） :: Link :: Dup（）`）。

You can also call `unbind()` method on `ProxyController` to get the usable `InterfaceHandle<Foo>` back, which then can be used by someone else. 您还可以在ProxyController上调用unbind（）方法来获取可用的InterfaceHandle <Foo>，然后其他人可以使用它。

 
### Proxies and Bindings Should Be Closed Properly  代理和绑定应正确关闭 

You need to explicitly close `FooProxy` and `FooBinding` objects that are bound to channels, when they are no longer in use. You do not need to explicitly close`InterfaceRequest<Foo>` or `InterfaceHandle<Foo>` objects, as those objectsrepresent unbound channels. 当不再使用绑定到通道的`FooProxy`和`FooBinding`对象时，您需要显式关闭它们。您不需要显式关闭“ InterfaceRequest <Foo>”或“ InterfaceHandle <Foo>”对象，因为这些对象表示未绑定的通道。

If you don't close or unbind these objects and they get picked up by the garbage collector, then FIDL will terminate the process and (in debug builds) log theDart stack for when the object was bound. The only exception to this rule is for*static* objects that live as long as the isolate itself. The system is able toclose these objects automatically for you as part of an orderly shutdown of theisolate. 如果您不关闭或解除绑定这些对象，并且垃圾回收器将它们拾取，则FIDL将终止该过程，并（在调试版本中）记录绑定对象的Dart堆栈。此规则的唯一例外是对于*静态*对象的生存时间与隔离对象本身一样长。系统可以自动关闭这些对象，作为隔离隔离的有序关闭的一部分。

If you are writing a Flutter widget, you can override the `dispose()` function on `State` to get notified when you're no longer part of the tree. That's acommon time to close the proxies used by that object as they are often no longerneeded. 如果您正在编写Flutter小部件，则可以在State上覆盖`dispose（）`函数，以便在您不再属于树的一部分时得到通知。这是关闭该对象使用的代理的常见时间，因为通常不再需要它们。

 
# Other Useful Tips  其他有用的提示 

 
## Getting the Atom dartlang plugin to work correctly  使Atom dartlang插件正常工作 

You need to have the correct `.packages` file generated for the dart packages in fuchsia tree. After building fuchsia, run this script form the terminal of yourdevelopment machine: 您需要为樱红色树中的飞镖包生成正确的`.packages`文件。构建紫红色之后，请在开发机器的终端上运行以下脚本：

```sh
<fuchsia_root>$ scripts/symlink-dot-packages.py
```
 

Also, for flutter projects, the following line should be manually added to the `.packages` file manually (fill in the fuchsia root dir of yours): 同样，对于flutter项目，应手动将以下行手动添加到`.packages`文件中（填写您的紫红色根目录）：

```
sky_engine:file:///<abs_fuchsia_root>/third_party/dart-pkg/git/flutter/bin/cache/pkg/sky_engine/lib/
```
 

You might have to relaunch Atom to get everything working correctly. With this `.packages` files, you get all dartanalyzer errors/warnings, jump to definition,auto completion features. 您可能必须重新启动Atom才能正常运行。有了这个.packages文件，您将获得所有dartanalyzer错误/警告，跳转到定义，自动完成功能。

 
# Testing  测试中 

