 
# Analysis  分析 

 

Analysis is run as part of the Fuchsia build.  分析是紫红色版本的一部分。

For each `dart_library` target, an analysis script gets also generated in the output directory under: 对于每个`dart_library`目标，还将在输出目录下的以下位置生成一个分析脚本：

```sh
out/<build-type>/gen/path/to/package/package.analyzer.sh
```
 

Running this script will perform an analysis of the target's sources. Note that other templates usually define a Dart library they build upon. Forexample, a _flutter_app_ `//foo/bar` will yield a `//foo/bar:bar_dart_library`target which can also be analyzed. 运行此脚本将对目标源进行分析。请注意，其他模板通常会定义基于它们的Dart库。例如，_flutter_app_`// foo / bar`将产生一个`// foo / bar：bar_dart_library`目标，也可以对其进行分析。

As with standard Dart packages, analysis options are defined in an `analysis_options.yaml` file, which must be placed at the package root.This file may refer to a common set of options by way of an `include` directive: 与标准Dart包一样，分析选项在`analysis_options.yaml`文件中定义，该文件必须放在包根目录下。该文件可以通过`include`指令引用一组常用选项：

```
include: relative/path/to/options.file
```
 

A canonical set is available at [//topaz/tools/analysis_options.yaml](https://fuchsia.googlesource.com/topaz/+/master/tools/analysis_options.yaml) It is customary to merely include that set from a local options file: 可以在[//topaz/tools/analysis_options.yaml](https://fuchsia.googlesource.com/topaz/+/master/tools/analysis_options.yaml）上找到规范集。本地选项文件：

```
include: path/to/topaz/tools/analysis_options.yaml
```
 

Analysis may be disabled altogether for a given target with:  对于给定的目标，可以通过以下方式完全禁用分析：

```
dart_library("foo") {
  disable_analysis = true
}
```
 

The `//scripts/run-dart-action.py` script makes it easy to run the analysis over multiple targets: 使用//scripts/run-dart-action.py脚本可以轻松地对多个目标运行分析：

```sh
scripts/run-dart-action.py analyze --out out/<build-type> --tree //topaz/shell/*
```
 

Regular analyzer flags may also be passed:  常规分析器标志也可以传递：

```sh
scripts/run-dart-action.py analyze --out out/<build-type> --fatal-warnings --lints
```
 

