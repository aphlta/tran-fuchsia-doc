 
# How to write benchmarks  如何编写基准 

 
* Updated: 2018 August 9  *更新时间：2018年8月9日

[TOC]  [目录]

 

 
## Overview  总览 

This guide will walk you through the process of writing a benchmark, running it at every commit, and automatically tracking the results in the [Performance Dashboard]. 本指南将引导您完成编写基准，在每次提交时运行基准以及在[Performance Dashboard]中自动跟踪结果的过程。

Today we support automating benchmarks for these projects:  今天，我们支持这些项目的自动化基准测试：
* Garnet (Also runs Zircon benchmarks)  *石榴石（还运行Zircon基准测试）
* Peridot  *橄榄石
* Topaz  *黄玉

 
## Writing a benchmark  编写基准 

Fuchsia benchmarks are command-line executables that produce a JSON results file.  The executable must meet the following criteria: 紫红色基准测试是产生JSON结果文件的命令行可执行文件。可执行文件必须满足以下条件：

 
1. It accepts the location to the results file as a command line flag.  1.它接受结果文件的位置作为命令行标志。
2. It produces JSON results that match the [benchmark results schema]:  2.产生与[基准结果模式]相匹配的JSON结果：

 
## Building your benchmark  建立基准 

Your benchmark executable should be built into a Fuchsia package.  For more information please read the [Fuchsia Build overview]. 您的基准可执行文件应内置在Fuchsia软件包中。有关更多信息，请阅读[Fuchsia Build概述]。

 
## Automating your benchmark  自动化基准 

We have shell scripts that run all of a layer's benchmarks at every commit to that layer.  我们拥有在该层的每次提交时都运行该层的所有基准测试的Shell脚本。

 
* Garnet: [//garnet/tests/benchmarks](/garnet/tests/benchmarks)  *石榴石：[//石榴石/测试/基准]（//石榴石/测试/基准）
* Peridot: [//peridot/tests/benchmarks](/peridot/tests/benchmarks)  *橄榄石：[//橄榄石/测试/基准]（//橄榄石/测试/基准）
* Topaz: [//topaz/tests/benchmarks](https://fuchsia.googlesource.com/topaz/+/master/tests/benchmarks)  *黄玉：[// topaz / tests / benchmarks]（https://fuchsia.googlesource.com/topaz/+/master/tests/benchmarks）

These shell scripts are written using a helper library called [benchmarking].  Add a command to the appropriate script to execute your test.  See the existing commands forexamples. 这些shell脚本是使用称为[benchmarking]的帮助程序库编写的。将命令添加到适当的脚本以执行测试。有关示例，请参见现有命令。

 
## Testing  测试中 

At this point, you're ready to build Fuchsia and test that your benchmark runs successfully. Run the following in a shell: 至此，您已经准备好构建Fuchsia并测试您的基准测试是否成功运行。在shell中运行以下命令：

```sh
jiri update -gc
# Benchmarks are not included in production packages, so use $layer/packages/kitchen_sink
# or they will not be built.
fx set core.<board> --with //bundles:kitchen_sink
fx build && fx emu
```
 

Once the Fuchsia shell is loaded:  紫红色的外壳加载后：

```sh
# Run just your benchmark
run my_benchmark [options]

# Run all benchmarks for $layer
/pkgfs/packages/${layer}_benchmarks/0/bin/benchmarks.sh /tmp
```
 

If no errors occurred, you should see your benchmark's output file in `/tmp`, along with the results files of other benchmarks. 如果没有发生错误，您应该在/ tmp中看到基准的输出文件，以及其他基准的结果文件。

 
## Tracking in the performance dashboard  在效果信息中心中进行跟踪 

Please see the [Performance Dashboard User Guide]  请参阅[Performance Dashboard用户指南]

Note: We do not yet have a User guide for the [Performance Dashboard Version 2].  注意：我们还没有[Performance Dashboard Version 2]的用户指南。

