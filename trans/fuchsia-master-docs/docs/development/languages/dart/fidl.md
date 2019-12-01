 
# FIDL  FIDL 

 

[FIDL targets][fidl] generate implicit Dart bindings targets. To use the bindings generated for: [FIDL目标] [fidl]生成隐式Dart绑定目标。要将生成的绑定用于：

```
//foo/bar
//foo/bar:blah
```
 

add a dependencies in BUILD.gn:  在BUILD.gn中添加一个依赖项：

```
deps = [
   ...
   "//foo/bar",
   "//foo/bar:blah",
   ...
]
```
 

There are 3 files generated for dart from FIDL.  These are found in `out/default/dartlang/gen/<path-to-target>/<fidl-servicename>_package/lib` FIDL为飞镖生成了3个文件。这些可以在`out / default / dartlang / gen / <目标路径> / <fidl-servicename> _package / lib中找到。

 
* fidl.dart - the synchronous bindings  * fidl.dart-同步绑定
* fidl_async.dart - the asynchronous bindings  * fidl_async.dart-异步绑定
* fidl_test.dart - the stubbed out implementation of the service.  * fidl_test.dart-该服务的存根实现。

 

```dart
import "package:fidl_foo_bar/fidl.dart";
import "package:fidl_foo_bar_blah/fidl_async.dart";
```
 

 

 
## Known issues  已知的问题 

 
### Multiple FIDL targets in a single BUILD file  单个BUILD文件中有多个FIDL目标 

If two FIDL targets coexist in a single BUILD file:  如果两个FIDL目标共存于一个BUILD文件中：

 
* Their respective, generated files will currently be placed in the same subdirectory of the output directory.  This means that files belonging to onetarget will be available to clients of the other target, and this will likelyconfuse the analyzer.  This should not be a build issue now but could becomeone once the generated Dart files are placed in separate directories ifclients do not correctly set up their dependencies. *它们各自生成的文件当前将放置在输出目录的同一子目录中。这意味着属于一个目标的文件将可供另一目标的客户端使用，这可能会使分析器感到困惑。现在这应该不是构建问题，但是如果客户端未正确设置其依赖项，则一旦将生成的Dart文件放置在单独的目录中就可能成为一个问题。
* Depending on one of these targets from *another* FIDL target that is used by a Dart package leads to a `Unable to read Dart source ...` error. Thebindings generator for FIDL builds Dart package names based on the directorystructure containing the included FIDL file, while GN (used to computedependencies for the Dart package) does so using the full GN target name. Forexample: depending on `lib/foo/fidl:bar` generates a package like`lib.foo.fidl._bar`. Depending on the top-level target `lib/foo/fidl`generates the package `lib.foo.fidl`, which coincides with the Dart FIDLbinding's assumptions. *取决于Dart包使用的*另一个* FIDL目标中的这些目标之一，将导致“无法读取Dart源...”错误。 FIDL的绑定生成器基于包含所包含的FIDL文件的目录结构来构建Dart包名称，而GN（用于Dart包的计算依赖项）则使用完整的GN目标名称来构建Dart包名称。例如：依赖于`lib / foo / fidl：bar`生成一个像`lib.foo.fidl._bar`这样的包。根据顶层目标`lib / foo / fidl`生成软件包`lib.foo.fidl`，这与Dart FIDLbinding的假设是一致的。
  
 
## Calling a FIDL service  呼叫FIDL服务 

The generated bindings for Dart require the importing of fuchsia_services.  为Dart生成的绑定需要导入fuchsia_services。

 

```dart
import 'package:fuchsia_services/services.dart';
```
 

 

In order to use the Launcher service to start services that implement a FIDL interface, you need to have the `fuchsia.sys.Launcher` service declared in the .cmx 为了使用Launcher服务启动实现FIDL接口的服务，您需要在.cmx中声明`fuchsia.sys.Launcher`服务。

 

