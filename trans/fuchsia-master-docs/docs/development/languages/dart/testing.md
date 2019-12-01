 
# Testing  测试中 

 
## Types of tests  测试类型 

Multiple Dart test targets are available:  提供多个Dart测试目标：

 
- [dart_fuchsia_test] runs the test as a package on a fuchsia device. This must be used if there is anything fuchsia specific being used like fidl. It is runwith `fx run-test`. -[dart_fuchsia_test]以测试包的形式在紫红色的设备上运行测试。如果有任何像fidl一样的紫红色使用，则必须使用它。它与`fx run-test`一起运行。
- [dart_test] runs unit tests that can be run on the host or on a fuchsia device. The dart:ui package is not made available to these tests. The test canbe run with `fx run-host-tests`. -[dart_test]运行可以在主机或紫红色设备上运行的单元测试。 dart：ui软件包不适用于这些测试。该测试可以通过fx run-host-tests运行。
- [flutter_test] is just like dart_test except the dart:ui package is made available to it, so it can test widget code. -[flutter_test]与dart_test相似，不同之处在于dart：ui包可供使用，因此它可以测试小部件代码。

For information on integration testing [Flutter mods](mods.md), see [mod integration testing](mod_integration_testing.md). 有关集成测试[Flutter mods]（mods.md）的信息，请参阅[mod集成测试]（mod_integration_testing.md）。

Note that in order to be built and run on bots, the test targets need to be included in the packages that are configured to run there. For example, intopaz this can be achieved by adding those tests to `//topaz/packages/tests`. 请注意，为了在bot上构建和运行，测试目标需要包含在配置为在bot上运行的软件包中。例如，intopaz可以通过将这些测试添加到“ // topaz / packages / tests”中来实现。

 
## Code coverage  代码覆盖率 

To generate an HTML coverage report from all `dart_test`s, first build them with `fx build` and then run: 要从所有`dart_test`生成HTML覆盖率报告，请首先使用`fx build`构建它们，然后运行：

```sh
scripts/dart/report_coverage.py --report-dir ...
```
 

This script runs all of the dart tests in your `<out>/host_tests/` dir with coverage enabled. Under the hood, each test uses the coverage collection supportfrom [flutter](https://github.com/flutter/flutter/wiki/Test-coverage-for-package:flutter). 该脚本在启用<cover>的`<out> / host_tests /`目录中运行所有dart测试。在幕后，每个测试都使用[flutter]（https://github.com/flutter/flutter/wiki/Test-coverage-for-package:flutter）的coverage收集支持。

The basic logic is:  基本逻辑是：

```
for test in host_tests:
  covered_lines += lines in test's package that were covered by test
  total_lines += all lines in test's package
```
 

So if there are packages that have no tests at all, they won't be considered in the denominator of the report, which can give you a misleadingly high coveragenumber. 因此，如果有些软件包根本没有测试，那么它们将不会在报告的分母中考虑，这可能会误导您高覆盖率。

