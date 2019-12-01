 
# Dart  镖 

 

 
## Overview  总览 

Dart artifacts are not built the same way in Fuchsia as they are on other platforms. Dart工件在紫红色中的构建方式与在其他平台上不同。

Instead of relying on [`pub`][pub] to manage dependencies, sources of third-party packages we depend on are checked into the tree under`//third_party/dart-pkg`.This is to ensure we use consistent versions of our dependencies across multiplebuilds. 无需依赖[pub]] [pub]来管理依赖项，而是将我们依赖的第三方程序包的源检入// third_party / dart-pkg下的树中。这是为了确保我们使用一致的版本我们跨多个构建的依赖关系。

Likewise, no build output is placed in the source tree as everything goes under `out/`. That includes `.packages` files which are generated as part of the buildbased on a target's dependency. 同样，由于所有内容都在`out /`下，因此没有构建输出放置在源树中。其中包括“ .packages”文件，这些文件是根据目标的依赖关系在构建过程中生成的。

 
## Exiting Dart programs  退出Dart程序 

The Dart runner for Fuchsia does not monitor the FIDL channels opened by Dart programs and as a result does not endthe program normally, but rather waits for the explict call to `fuchsia.exit()`to indicate the program should be ended. 倒挂金钟的Dart运行程序不会监视Dart程序打开的FIDL通道，因此不会正常结束该程序，而是等待对`fuchsia.exit（）`的明确调用以指示该程序应该结束。

Note: Calling exit() from dart:io will result in an exception since components are not allowed to call this method since it would shutdown the dart_runner process. 注意：从dart：io调用exit（）将导致异常，因为不允许组件调用此方法，因为它将关闭dart_runner进程。

```dart
import 'package:fuchsia/fuchsia.dart' as fuchsia;

void main(List<String> args) {
  print('Hello Dart!');
  fuchsia.exit(23);
}
```
 

 

 
## Targets  目标 

There are five gn targets for building Dart:  构建Dart有五个gn目标：

 
- [`dart_library`][target-library] defines a library that can be used by other Dart targets; -[`dart_library`] [target-library]定义了可供其他Dart目标使用的库；
- [`dart_app`][target-app] defines a Dart executable for Fuchsia;  -[`dart_app`] [target-app]为紫红色定义了Dart可执行文件；
- [`dart_tool`][target-tool] defines a Dart tool for the host;  -[`dart_tool`] [target-tool]为主机定义了Dart工具；
- [`flutter_app`][target-flutter] defines a [Flutter][flutter] application;  -[`flutter_app`] [target-flutter]定义了[Flutter] [flutter]应用；
- [`dart_test`][target-test] defines a group of test.  -[`dart_test`] [target-test]定义了一组测试。

See the definitions of each of these targets for how to use them.  请参阅每个目标的定义以了解如何使用它们。

 

 
## Package layout  包装布局 

We use a layout very similar to the [standard layout][package-layout].  我们使用的布局与[标准布局] [封装布局]非常相似。

```
my_package/
  |
  |-- pubspec.yaml           # Empty, used as a marker [mandatory]
  |-- BUILD.gn               # Contains all targets
  |-- analysis_options.yaml  # Analysis configuration [mandatory]
  |-- lib/                   # dart_library contents
  |-- bin/                   # dart_binary's (target) or dart_tool's (host)
  |-- test/                  # dart_test contents
```
 

 
## Going further  更进一步 

 
- [Running analysis](analysis.md)  -[运行分析]（analysis.md）
- [Style](style.md)  -[样式]（style.md）
- [Testing](testing.md)  -[测试]（testing.md）
- [Logging](logging.md)  -[记录]（logging.md）
- [Using FIDL](fidl.md)  -[使用FIDL]（fidl.md）
- [Managing third_party dependencies](third_party.md)  -[管理第三方依赖关系]（third_party.md）
- [IDEs](ides.md)  -[IDEs]（ides.md）

 

