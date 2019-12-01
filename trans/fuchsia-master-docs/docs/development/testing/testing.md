 
# Testing  测试中 

 
## Quick Start  快速开始 

To build Zircon and run unit tests, run one of the following commands:  要构建Zircon并运行单元测试，请运行以下命令之一：

```sh
# Build and run x64.
fx set bringup.x64 --with-base //garnet/packages/tests:zircon
fx build
fx qemu

# Build and run arm64.
fx set bringup.arm64 --with-base //garnet/packages/tests:zircon
fx build
fx qemu
```
 

Once the scripts finish running, you should see the Zircon shell. To run userspace tests, use the Zircon shell to run: 脚本运行完成后，您将看到Zircon Shell。要运行用户空间测试，请使用Zircon shell运行：

```sh
runtests
```
 

To run in-kernel tests, use the Zircon shell to run:  要运行内核内测试，请使用Zircon shell运行：

```sh
k ut all
```
 

Fuchsia's [Get Started](/docs/getting_started.md) page has more details about how to use the Zircon shell and how to automatically build all supported architectures. Fuchsia的[Get Started]（/ docs / getting_started.md）页面包含有关如何使用Zircon Shell以及如何自动构建所有受支持的体系结构的更多详细信息。

 
## Userspace Tests  用户空间测试 

The test harness, runtests, picks up and runs all of the executables from the `/boot/test` and `/system/test` directories. If you provide a command-lineargument, such as `runtests -S -m widget_test`, runtests will only run thesingle test requested -- in this case, `widget_test`. 测试工具runtests从/ boot / test目录和/ system / test目录中拾取并运行所有可执行文件。如果提供命令线性参数，例如`runtests -S -m widget_test`，则runtests将仅运行请求的单个测试-在这种情况下为`widget_test`。

"runtests" takes command-line arguments to toggle classes of tests to execute.  “ runtests”使用命令行参数来切换要执行的测试类别。

These classes are the following:  这些类如下：

 
* **Small**: Isolated tests for functions and classes. These must be totally synchronous and single-threaded. These tests should be parallelizable; thereshouldn't be any shared resources between them. * **小**：对函数和类进行隔离测试。这些必须完全同步并且是单线程的。这些测试应该是可并行的。它们之间不应有任何共享资源。
* **Medium**: Single-process integration tests. Ideally these are also synchronous and single-threaded but they might run through a large chunk of code in eachtest case, or they might use disk, making them a bit slower. * **中**：单进程集成测试。理想情况下，它们也是同步的和单线程的，但是在每种测试情况下，它们都可能运行大量代码，或者它们可能使用磁盘，从而使其运行速度变慢。
* **Large**: Slow, multi-process, or particularly incomprehensible single-process integration tests. These tests are often too slow / flaky to run in a CQ, andwe should try to limit how many we have. * **大型**：缓慢，多进程或特别难以理解的单进程集成测试。这些测试通常太慢/不稳定，无法在CQ中运行，我们应该尝试限制有多少。
* **Performance**: Tests which are expected to pass, but which are measured using other metrics (thresholds, statistical techniques) to identifyregressions. * **性能**：预期会通过，但使用其他指标（阈值，统计技术）进行测量以识别回归的测试。

Since runtests doesn't really know what "class" is executing when it launches a test, it encodes this information in the environment variable`RUNTESTS_TEST_CLASS`, which is detailed in [the unittestheader][unittest-header] , and lets the executable itself decide what to run /not run. This environment variable is a bitmask indicating which tests to run. 由于runtests在启动测试时并不真正知道正在执行的“类”，因此会将其信息编码到环境变量RUNTESTS_TEST_CLASS中，该变量在[unittestheader] [unittest-header]中进行了详细说明，并让可执行文件自己执行决定要运行/不运行。该环境变量是一个位掩码，指示要运行的测试。

For example, if a a test executable is run with "small" and "medium" tests, it will be executed ONCE with `RUNTESTS_TEST_CLASS` set to 00000003 (thehex bitwise OR of "TEST_SMALL" and "TEST_MEDIUM" -- though this informationshould be parsed using the [unittest header][unittest-header], as it may beupdated in the future). 例如，如果一个测试可执行文件在“小型”和“中型”测试中运行，则将在“ RUNTESTS_TEST_CLASS”设置为00000003的情况下执行一次（“ TEST_SMALL”和“ TEST_MEDIUM”的十六进制按位OR －尽管应该解析此信息）使用[unittest标头] [unittest-header]，因为将来可能会更新）。

 
### Zircon Tests (ulib/test, and/or using ulib/unittest)  锆石测试（ulib /测试和/或使用ulib / unittest） 

The following macros can be used to filter tests into these categories:  以下宏可用于将测试过滤到这些类别中：

```
RUN_TEST_SMALL(widget_tiny_test)
RUN_TEST_MEDIUM(widget_test)
RUN_TEST_LARGE(widget_big_test)
RUN_TEST_PERFORMANCE(widget_benchmark)
```
 

The legacy `RUN_TEST(widget_test)` is aliased to mean the same thing as `RUN_TEST_SMALL`. 遗留的RUN_TEST（widget_test）的别名与RUN_TEST_SMALL的含义相同。

 
### Fuchsia Tests (not using ulib/unittest)  紫红色测试（不使用ulib / unittest） 

The environment variable `RUNTESTS_TEST_CLASS` will still be available to all executables launched by runtests. The [unittest header][unittest-header] can beused to parse different categories of tests which the runtests harness attemptedto run. 环境变量“ RUNTESTS_TEST_CLASS”仍将对运行测试启动的所有可执行文件可用。可以使用[unittest标头] [unittest-header]来解析runtests利用试图运行的不同类别的测试。

 
### Runtests CLI  运行测试CLI 

By default, runtests will run both small and medium tests.  默认情况下，运行测试将同时运行中小型测试。

To determine how to run a custom set of test categories, run `runtests -h`, which includes usage information. 要确定如何运行一组自定义的测试类别，请运行“ runtests -h”，其中包括使用情况信息。

[unittest-header]: /zircon/system/ulib/unittest/include/unittest/unittest.h "Unittest Header"  [unittest-header]：/zircon/system/ulib/unittest/include/unittest/unittest.h“Unittest标头”

 

 
## Kernel-mode Tests  内核模式测试 

The kernel contains unit tests and diagnostics, which can be run using the `k` command. The output of the `k` command will only be shown on theconsole. Depending on your configuration, this might be the serial console, orthe `debuglog` virtual terminal. 内核包含单元测试和诊断，可以使用`k`命令运行。 k命令的输出将仅显示在控制台上。根据您的配置，这可能是串行控制台或“ debuglog”虚拟终端。

 
### Unit tests  单元测试 

Many parts of the kernel have unit tests, which report success/failure automatically. These unit tests are built using the primitives provided by [thekernel unit-test library](/zircon/kernel/lib/unittest/). You can find these staticallyby searching for `UNITTEST_START_TESTCASE`. 内核的许多部分都有单元测试，它们会自动报告成功/失败。这些单元测试是使用[thekernel单元测试库]（/ zircon / kernel / lib / unittest /）提供的原语构建的。您可以通过搜索“ UNITTEST_START_TESTCASE”来静态找到这些内容。

These tests can be run from the shell with `k ut`. `k ut all` will run all tests or you can use `k ut $TEST_NAME` to run a specific test. 这些测试可以使用`k ut`从外壳运行。 `k ut all`将运行所有测试，或者您可以使用`k ut $ TEST_NAME`运行特定的测试。

 
### Diagnostics  诊断程序 

Many parts of the kernel provide diagnostics, whose output requires manual inspection. Some of these diagnostics are used to verify correctness(e.g. [`timer_diag`](/zircon/kernel/tests/timer_tests.cc)), while others simplystress test a part of the system(e.g. [`timer_stress`](/zircon/kernel/tests/timer_tests.cc)). 内核的许多部分提供诊断，其输出需要手动检查。其中一些诊断程序用于验证正确性（例如[`timer_diag`]（/ zircon / kernel / tests / timer_tests.cc）），而其他诊断程序只是对系统的一部分进行压力测试（例如[`timer_stressg]]（/ zircon /内核/测试/timer_tests.cc））。

To run a diagnostic, simply pass its name to the `k` command. For example, to run the kernel's [builtin benchmarks](/zircon/kernel/tests/benchmarks.cc), run `kbench`. To find the full set of kernel diagnostics statically, search for`STATIC_COMMAND`. To enumerate them dynamically, run `k help`. 要运行诊断，只需将其名称传递给`k`命令即可。例如，要运行内核的[内置基准测试]（/ zircon / kernel / tests / benchmarks.cc），请运行`kbench`。要静态地找到完整的内核诊断集，请搜索“ STATIC_COMMAND”。要动态枚举它们，运行`k help`。

