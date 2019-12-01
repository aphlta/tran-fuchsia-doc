 
# Fuzz testing in Fuchsia with LibFuzzer  使用LibFuzzer在紫红色中进行模糊测试 

Fuzzing is a testing technique that feeds auto-generated inputs to a piece of target code in an attempt to crash the code. This technique finds securityvulnerabilities and stability bugs that other testing might miss. You can seeFuchsia fuzzing trophies in Monorail by using the[`component:Security>clusterfuzzreporter:clusterfuzz@chromium.org`](https://bugs.fuchsia.dev/p/fuchsia/issues/list?colspec=ID%20jira_id%20Component%20Type%20Pri%20Status%20Owner%20Summary%20Modified&q=component%3ASecurity%3Eclusterfuzz%20reporter%3Aclusterfuzz%40chromium.org&can=2)filter. 模糊测试是一种测试技术，可将自动生成的输入馈送到目标代码，以使代码崩溃。该技术可以发现其他测试可能会遗漏的安全漏洞和稳定性错误。您可以使用[`component：Security> clusterfuzzreporter：clusterfuzz @ chromium.org`]（https://bugs.fuchsia.dev/p/fuchsia/issues/list?colspec=ID%20jira_id%，在单轨火车上看到紫红色的模糊奖杯20Component％20Type％20Pri％20Status％20Owner％20Summary％20Modifiedq = component％3ASecurity％3Eclusterfuzz％20reporter％3Aclusterfuzz％40chromium.orgcan = 2）过滤器。

This guide focuses on [LibFuzzer](#q-what-is-libfuzzer), an in-process fuzzing engine. 本指南重点介绍[LibFuzzer]（q-what-is-libfuzzer），它是一个进程内的模糊引擎。

 
## Quick-start guide  快速入门指南 

 
1. Pass fuzzed inputs to your library by implementing [LLVMFuzzerTestOneInput](#q-what-do-i-need-to-write-to-create-a-fuzzer). 1.通过实现[LLVMFuzzerTestOneInput]（q-需要做些什么来编写以创建一个模糊器），将模糊的输入传递给您的库。
1. Add a fuzzer build rule:  1.添加一个模糊器构建规则：
  * Add a [`fuzzer`][gn fuzzer] to the appropriate BUILD.gn.  *将[`fuzzer`] [gn fuzzer]添加到适当的BUILD.gn。
  * Fuchsia: Create or extend a [`fuzzers_package`][gn fuzzers package] in an appropriate BUILD.gn.  *紫红色：在适当的BUILD.gn中创建或扩展[`fuzzers_package`] [gn fuzzers软件包]。
  * Ensure there's a path from  a top-level target, e.g. `//bundles:tests`, to your fuzzers package.  *确保从顶级目标（例如`// bundles：tests`，到您的Fuzzer软件包
1. Configure, build, and boot (with networking), e.g.:  1.配置，构建和引导（通过网络），例如：
  * _if a Fuchsia instance is not already running:_ `fx qemu -N`  * _如果Fuchsia实例尚未运行：_`fx qemu -N`
  * `fx set core.x64 --fuzz-with asan --with //bundles:tests --with //garnet/packages/products:devtools`  *`fx set core.x64 --fuzz-with asan --with // bundles：tests --with // garnet / packages / products：devtools`
  * `fx build`  *`fx build`
  * `fx serve`  *`fx服务`
1. Use the fuzzer tool:  1.使用模糊器工具：
  * To display fuzzers: `$ fx fuzz list` *显示模糊器：`$ fx fuzz list`
  * To start a fuzzer. `$ fx fuzz <fuzzer>` *启动模糊器。 $ fx fuzz <模糊器>
  * To see if the fuzzer found crashes. `$ fx fuzz check <fuzzer>` *查看是否发现模糊器崩溃。 $ fx模糊检查<fuzzer>
  * To replay a crash. `$ fx fuzz repro <fuzzer> [crash]` *重播崩溃。 `$ fx fuzz repro <fuzzer> [崩溃]`
1. File bug using the following labels:  1.使用以下标签归档错误：
  * `found-by-fuzzing`  *“通过模糊发现”
  * `Sec-TriageMe`  *`Sec-TriageMe`
  * `libfuzzer`  *`libfuzzer`

[TOC]  [目录]

 
## Q: What is fuzzing? {#q-what-is-fuzzing}  问：什么是绒毛？ {q-what-is-fuzzing} 

A: Fuzzing or fuzz testing is style of testing that stochastically generates inputs to targeted interfaces in order to automatically find defects and/or vulnerabilities.  In this document,a distinction will be made between two components of a fuzzer: the fuzzing engine, which producescontext-free inputs, and the fuzz target function, which submits those inputs to a specificinterface. 答：模糊测试或模糊测试是一种测试类型，它会随机生成目标接口的输入，以便自动发现缺陷和/或漏洞。在本文档中，将对模糊器的两个组件进行区分：模糊引擎（产生上下文无关的输入）和模糊目标函数（将这些输入提交给特定的接口）。

Among the various styles of fuzzing, coverage-based fuzzing has been shown to yield a particularly high number of bugs for the effort involved.  In coverage-based fuzzing, the code under test isinstrumented for coverage. The fuzzing engine can observe when inputs increase the overall codecoverage and use those inputs as the basis for generating further inputs.  This group of "seed"inputs is collectively referred to as a corpus. 在各种类型的模糊测试中，基于覆盖的模糊测试已显示出涉及所涉及工作的大量错误。在基于覆盖率的模糊测试中，要测试覆盖范围内的代码。当输入增加整体代码覆盖率时，模糊引擎可以观察这些输入，并将这些输入用作生成更多输入的基础。这组“种子”输入统称为语料库。

 
## Q: What is libFuzzer? {#q-what-is-libfuzzer}  问：什么是libFuzzer？ {q-what-is-libfuzzer} 

A: [LibFuzzer] is an in-process fuzzing engine integrated within LLVM as a compiler runtime. [Compiler runtimes][compiler-rt] are libraries that are invoked by hooks that compiler adds to thecode it builds.  Other examples include [sanitizers] such as [ASan], which detects certain overflowsand memory corruptions. LibFuzzer uses these sanitizers both for [coverage data][sancov] provided bysanitizer-common, as well as to detect when inputs trigger a defect. 答：[LibFuzzer]是LLVM中作为编译器运行时集成的进程内模糊引擎。 [Compiler runtimes] [compiler-rt]是由钩子调用的库，钩子将编译器添加到其生成的代码中。其他示例包括[消毒剂]，例如[ASan]，它可以检测某些溢出和内存损坏。 LibFuzzer将这些消毒剂用于消毒剂常见的[coverage data] [sancov]，以及检测输入何时触发缺陷。

 
## Q: What do I need to write to create a fuzzer? {#q-what-do-i-need-to-write-to-create-a-fuzzer}  问：创建模糊器需要写什么？ {q需要做什么来创建一个模糊器} 

A: LibFuzzer can be used to make a coverage-based fuzzer binary by combining it with a sanitized library and the implementation of the [fuzz target] function: 答：通过将LibFuzzer与经过清理的库以及[fuzz target]函数的实现结合使用，可以使用它来制作基于coverage的模糊器二进制文件：

```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  // Use the data to do something interesting with your API
  return 0;
}
```
 

Optionally, you can also add an initial [corpus].  Without it, libFuzzer will start from an empty fuzzer and will (eventually) learn how to make appropriate inputs [on its own][thin-air]. 您也可以选择添加一个初始的[corpus]。没有它，libFuzzer将从一个空的模糊器开始，并且（最终）将学习如何[自行] [稀薄地]进行适当的输入。

LibFuzzer then be able to generate, submit, and monitor inputs to the library code: ![Coverage guided fuzzing](/docs/images/fuzzing/coverage-guided.png) 然后，LibFuzzer能够生成，提交和监视对库代码的输入：！[Coverage guide fuzzing]（/ docs / images / fuzzing / coverage-guided.png）

Developer-provided components are in green.  开发人员提供的组件为绿色。

 
## Q: What should I fuzz with libFuzzer? {#q-what-should-i-fuzz-with-libfuzzer}  问：我应该如何使用libFuzzer进行测试？ {q-我应该使用libfuzzer进行模糊测试} 

A: Coverage based fuzzing works best when fuzzing targets resemble [unit tests][fuzzer scope].  If your code is already organized to make it easy to unit test, you can add targets for each of theinterfaces being tested., e.g. something like: 答：当模糊测试目标类似于[单元测试] [模糊测试范围]时，基于覆盖的模糊测试效果最好。如果您的代码已经组织好以使其易于进行单元测试，则可以为每个要测试的接口添加目标。就像是：

```cpp
  // std::string json = ...;
  Metadata metadata;
  EXPECT_TRUE(metadata.Parse(json));
```
 

becomes:  变成：

```cpp
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  std::string json(static_cast<const char *>(Data), Size);
  metadata.Parse(json);
  return 0;
}
```
 

With a corpus of JSON inputs, `Data` may be close to what the `Metadata` object expects to parse. If not, the fuzzer will eventually discover what inputs are meaningful to it through randommutations, trial and error, and code coverage data. 使用JSON输入语料库，“数据”可能接近“元数据”对象期望解析的内容。否则，模糊器将最终通过随机变异，反复试验和代码覆盖率数据发现哪些输入对其有意义。

 
### Q: How do I fuzz more complex interfaces?  {#q-how-do-i-fuzz-more-complex-interfaces}  问：如何模糊更复杂的界面？ {q-如何做我更复杂的接口} 

A: The [`FuzzedDataProvider`][fuzzed-data-provider] library helps you map portions of the provided `Data` to ["plain old data" (POD)][pod] types. More complex objects can almostalways be (eventually) built out of POD types and variable arrays. 答：[`FuzzedDataProvider`] [fuzzed-data-provider]库可帮助您将提供的`Data`的某些部分映射到[“ plain old data”（POD）] [pod]类型。最终（最终）几乎可以使用POD类型和变量数组来构建更复杂的对象。

```cpp
  #include <fuzzer/FuzzedDataProvider.h>

  extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
    FuzzedDataProvider fuzzed_data(Data, Size);

    auto flags = fuzzed_data.ConsumeIntegral<uint32_t>();
    auto name_len =
         fuzzed_data.ConsumeIntegralInRange<size_t>(0, MAX_NAME_LEN - 1);

    std::string name = fuzzed_data.ConsumeBytesAsString(name_len);

    Parser parser(name.c_str(), flags);

    auto remaining = fuzzed_data.ConsumeRemainingBytes<char>();
    parser.Parse(remaining.data(), remaining.size());
    return 0;
  }
```
 

Note that using this library for splitting your data might make it harder for you to provide a corpus for your fuzzer, as the splitting happens dynamically.Other alternatives are explored in the [split inputs] documentation. 请注意，由于该拆分是动态进行的，因此使用此库拆分数据可能会使您更难为模糊器提供语料库。[拆分输入]文档中探讨了其他替代方法。

 

In some cases, you may have expensive set-up operations that you would like to do once.  The libFuzzer documentation has tips on how to do [startup initialization].  Be aware though that suchstate will be carried over from iteration to iteration.  This can be useful as it may expose newbugs that depend on the library's persisted state, but it may also make bugs harder to reproducewhen they depend on a sequence of inputs rather than a single one. 在某些情况下，您可能需要执行一次昂贵的设置操作。 libFuzzer文档包含有关如何进行[启动初始化]的提示。请注意，尽管这样的状态将在迭代之间延续。这可能很有用，因为它可能会暴露依赖于库持久状态的新错误，但是当它们依赖一系列输入而不是单个输入时，也可能使错误难以重现。

 
### Q: What if my object expects more `Data` than what libfuzzer provides? {#q-what-if-size-is-too-small}  问：如果我的对象期望比libfuzzer提供的更多“数据”怎么办？ {q-如果尺寸太小} 

If `Size` isn't long enough for your needs, you can simply `return 0;`. The fuzzer will quickly learn that inputs below that length aren't interesting andwill stop generating them. 如果“大小”不足以满足您的需求，则可以简单地“返回0;”。模糊器将迅速了解到该长度以下的输入没有意思，并且将停止生成它们。

By default, libfuzzer generates inputs with a maximum size of 4096. If you need to generate larger inputs, you can provide the `-max_len` flag to `fx fuzzstart`. If you provide a corpus input large enough, libfuzzer will increase themaximum size to that corpus size. 默认情况下，libfuzzer会生成最大大小为4096的输入。如果需要生成较大的输入，则可以向`fx fuzzstart`提供`-max_len`标志。如果您提供足够大的语料库输入，libfuzzer会将最大大小增加到该语料库大小。

 
### Q: How should I scope my fuzzer? {#q-how-should-i-scope-my-fuzzer}  问：我应该如何调整我的模糊器？ {q我应该如何看待我的模糊器} 

A: In general, an in-process coverage-based fuzzer, iterations should be __short__ and __focused__. The more focused a [fuzz target] is, the faster libFuzzer will be able to find "interesting" inputsthat increase code coverage. 答：通常，基于过程覆盖的模糊器的迭代应该是__short__和__focused__。 [fuzz目标]越集中，libFuzzer就能更快地找到“有趣的”输入，从而增加了代码覆盖率。

At the same time, becoming __too__ focused can lead to a proliferation of fuzz targets.  Consider the example of a routine that parses incoming requests.  The parser may recognize dozens ofdifferent request types, so developing a separate fuzz target for each may be cumbersome.  Analternative in this case may be to develop a single fuzzer, and include examples of the differentrequests in the initial [corpus].  In this way the single fuzz target can still bypass a largeamount of shallow fuzzing by being guided towards the interesting inputs. 同时，过分专注会导致模糊目标的扩散。考虑一个解析传入请求的例程的示例。解析器可能会识别数十种不同的请求类型，因此为每种请求开发单独的模糊目标可能很麻烦。在这种情况下，替代方案可能是开发单个模糊器，并在初始[语料库]中包含不同请求的示例。通过这种方式，单个模糊目标仍可以通过被引向有趣的输入而绕过大量浅层模糊。

Note: Currently, libFuzzer can be used in Fuchsia to fuzz C/C++ code. Additional language support is [planned][todo]. 注意：目前，在紫红色中可以使用libFuzzer来模糊C / C ++代码。其他语言支持为[计划中] [待办事项]。

 
## Q: LibFuzzer isn't quite right; what else could I use? {#q-libfuzzer-isnt-quite-right-what-else-could-i-use}  问：LibFuzzer不太正确；我还能用什么呢？ {q-libfuzzer-isnt-quit-正确，我可以使用什么} 

A: There's many other fuzzing engines out there:  答：还有许多其他模糊测试引擎：

 
* If the code you want to fuzz isn't a library with linkable interfaces, but instead a standalone binary, then [AFL] may be a be better suited. *如果要模糊处理的代码不是具有可链接接口的库，而是独立的二进制文件，则[AFL]可能更适合。

Note: AFL support on Fuchsia is [not yet supported][todo].  注意：[不支持] [todo]支持紫红色的AFL。

 
* If you want to fuzz a service through [FIDL] calls in the style of an integration test, see [Fuzzing FIDL Servers with LibFuzzer on Fuchsia][fidl_fuzzing]. *如果要以集成测试的方式通过[FIDL]调用来对服务进行模糊处理，请参阅[使用紫红色的LibFuzzer对FIDL服务器进行模糊处理] [fidl_fuzzing]。

 
* If none of these options fit your needs, you can still write a custom fuzzer and have it run continuously under [ClusterFuzz]. *如果这些选项都不满足您的需要，您仍然可以编写一个自定义模糊器，并使其在[ClusterFuzz]下连续运行。

 
## Q: How do I create a Fuchsia fuzzer? {#q-how-do-i-create-a-fuchsia-fuzzer}  问：如何创建紫红色的模糊器？ {q我如何创建紫红色的模糊器} 

A: First, create your [fuzz target] function.  It's recommended that the fuzzer's target is clear from file name.  If the library code already has a directory for unit tests, you should use asimilar directory for your fuzzing targets.  If not, make sure the file's name clearly reflects itis a fuzzer binary.  In general, use naming and location to make the fuzzer easy to find and itspurpose clear. 答：首先，创建您的[模糊目标]函数。建议从文件名中清除模糊器的目标。如果库代码已经具有用于单元测试的目录，则应将类似的目录用于模糊测试目标。如果不是，请确保文件名清楚地反映出模糊的二进制文件。通常，使用命名和位置使模糊器易于查找并且其目的明确。

_Example:_ A fuzzer for `//src/lib/cmx` might be located at `//src/lib/cmx/cmx_fuzzer.cc`, to match `//src/lib/cmx/cmx_unittest.cc`. _示例：_“ // src / lib / cmx”的模糊器可能位于“ //src/lib/cmx/cmx_fuzzer.cc”处，以匹配“ //src/lib/cmx/cmx_cmx_unittest.cc”。

Libfuzzer already [provides tips][fuzz target] on writing the fuzz target function itself.  Libfuzzer在编写模糊目标函数本身时已经[提供提示] [模糊目标]。

Next, add the build instructions to the library's BUILD.gn file.  Adding an import to [//build/fuzzing/fuzzer.gni][fuzzer.gni] will provide two templates: 接下来，将构建说明添加到库的BUILD.gn文件中。向[//build/fuzzing/fuzzer.gni][fuzzer.gni]添加导入将提供两个模板：

 
### The fuzzer GN template {#the-fuzzer-gn-template}  模糊器GN模板{the-fuzzer-gn-template} 

The `fuzzer` [template][fuzzer.gni] is used to build the fuzzer executable.  Given a fuzz target function in a source file and the library under test as a dependency, it will provided the correct[compiler flags] to link against the fuzzing engine: `fuzzer` [template] [fuzzer.gni]用于构建fuzzer可执行文件。给定源文件中的模糊目标函数和要测试的库作为依赖项，它将提供正确的[compiler flags]来链接模糊引擎：

```python
import("//build/fuzzing/fuzzer.gni")

fuzzer("cowsay_simple_fuzzer") {
  sources = [ "cowsay_fuzzer.cpp" ]
  deps = [ ":cowsay_sources" ]
}
```
 

It also enables the  `FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` [build macro].  If the software under test needs fuzzing-specific modifications, they can be wrapped in a preprocessor conditionalon this macro, e.g.: 它还启用了“ FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION” [构建宏]。如果被测软件需要特定于模糊测试的修改，则可以在此宏的条件下将其包装在预处理器中，例如：

```cpp
#ifdef FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION
  srand(++global_counter);
  rand_int = rand();
#else
  zx_cprng_draw(&rand_int, size_of(rand_int));
#endif
```
 

This can be useful to allow either more deterministic fuzzing and/or deeper coverage.  这对于允许更确定性的模糊和/或更深的覆盖范围很有用。

The fuzzer template also allows you include additional inputs to control the fuzzer:  模糊器模板还允许您包括其他输入来控制模糊器：

 
* [Dictionaries] are files with tokens, one per line, that commonly appear in the target's input, e.g. "GET" and "POST" for HTTP. * [Dictionaries]是带有令牌的文件，每行一个，通常出现在目标的输入中，例如HTTP的“ GET”和“ POST”。
* An options file, made up a series of key-value pairs, one per line, of libFuzzer command line [options]. *一个选项文件，由libFuzzer命令行[options]的一系列键值对组成，每行一个。

```python
import("//build/fuzzing/fuzzer.gni")

fuzzer("cowsay_simple_fuzzer") {
  sources = [ "cowsay_fuzztest.cpp" ]
  deps = [ ":cowsay_sources" ]
  dictionary = "test_data/various_moos.dict"
  options = "test_data/fuzzer.opts"
}
```
 

When you use the [fx fuzz tool], libFuzzer's `merge`, `jobs`, `dict`, and `artifact_prefix` options are set automatically. You do not need to specify these options unless they differ from the defaultvalues. 当您使用[fx模糊工具]时，libFuzzer的`merge`，`jobs`，`dict`和`artifact_prefix`选项会自动设置。除非它们与默认值不同，否则无需指定这些选项。

 
### The fuzzers_package GN template {#the-fuzzers-package-gn-template}  fuzzers_package GN模板{the-fuzzers-package-gn-template} 

The `fuzzers_package` [template][fuzzer.gni] bundles fuzzers into a Fuchsia package in the same way that a normalpackage bundles binaries. `fuzzers_package` [template] [fuzzer.gni]将fuzzers捆绑到Fuchsia软件包中，就像普通软件包捆绑二进制文件一样。

```python
fuzzers_package("cowsay_fuzzers") {
  fuzzers = [ ":cowsay_simple_fuzzer" ]
}
```
 

By default, the package will support all sanitizers. This can be restricted by providing an optional "sanitizers" list, e.g. `sanitizers = [ "asan", "ubsan" ]` 默认情况下，该软件包将支持所有消毒剂。这可以通过提供可选的“消毒剂”列表来限制，例如`sanitizers = [“ asan”，“ ubsan”]`

Once defined, a package needs to be included in the build dependency graph like any other test package.  This typically means adding it to a group of tests, e.g. a `group("tests")` target. 定义后，需要像其他测试包一样将包包含在构建依赖关系图中。这通常意味着将其添加到一组测试中，例如一个group（“ tests”）`目标。

__IMPORTANT__: The Fuchsia build system will build the fuzzers __only__ if it is explicitly told to instrument them for fuzzing with an appropriate sanitizer.  The easiest way to achieve this is usingthe `--fuzz-with <sanitizer>` flag with `fx set`, e.g: __重要__：如果明确要求Fuchsia构建系统仅______构建绒毛机，并用适当的消毒剂对绒毛进行检测。最简单的方法是使用带有--fx-set的--fuzz-with <sanitizer>标志，例如：

```
$ fx set core.x64 --fuzz-with asan --with //bundles:tests --with //garnet/packages/products:devtools
$ fx build
```
 

 
## Q: How do I create a Zircon fuzzer? {#q-how-do-i-create-a-zircon-fuzzer}  问：如何创建锆石模糊器？ {q如何制作锆石模糊器} 

Zircon has a different [fuzzer.gni template][fuzzer.gni] from the rest of Fuchsia, but is used similarly:  锆石与紫红色的其余部分具有不同的[fuzzer.gni模板] [fuzzer.gni]，但用法类似：

```python
import("$zx/public/gn/fuzzer.gni")

fuzzer("zx-fuzzer") {
  sources = [ "zx_fuzzer.cpp" ]
  deps = [ ":zx_sources" ]
}
```
 

---------------------------------------  ---------------------------------------

> NOTE: Due to gn unification, you will also need to manually add the binary targets to > `build/unification/images/BUILD.gn`: >注意：由于gn的统一，您还需要将二进制目标手动添加到>`build / unification / images / BUILD.gn`：

> [TODO(41279)](https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=41279): Update these docs with zircon > fuzzing instructions. > [TODO（41279）]（https://bugs.fuchsia.dev/p/fuchsia/issues/detail?id=41279）：使用Zircon>模糊测试说明更新这些文档。

```
aggregate_manifest("legacy-image") {
  deps = [ (...)
    ":bin.zx-fuzzer.asan",
    ":bin.zx-fuzzer.asan-ubsan",
    ":bin.zx-fuzzer.ubsan",
```
 

Zircon fuzzers will be built with all supported sanitizers automatically. These fuzzers can be included in a Fuchsia instance by including the `zircon_fuzzers` package, e.g.: 锆石模糊测试器将自动构建所有受支持的消毒器。可以通过包含`zircon_fuzzers`软件包将这些模糊器包含在Fuchsia实例中，例如：

```
$ fx set core.x64 --with //garnet/tests/zircon:zircon_fuzzers --with //garnet/packages/products:devtools
$ fx build
```
 

Note that Zircon fuzzers *must* have names that end in "-fuzzer".  请注意，“锆石”模糊器*必须*的名称以“ -fuzzer”结尾。

 
## Q: How do I run a fuzzer? {#q-how-do-i-run-a-fuzzer}  问：如何运行模糊器？ {q-我如何运行模糊器} 

A: Use the `fx fuzz` tool which knows how to find fuzzing related files and various common options.  答：请使用“ fx fuzz”工具，该工具知道如何查找与模糊相关的文件和各种常用选项。

 

The fuzzer binary can be started directly, using the normal libFuzzer options, if you prefer. However, it is easier to use the `fx fuzz` devshell tool, which understands where to look forfuzzing related files and knows various common options.  Try one or more of the following: 如果愿意，可以使用常规的libFuzzer选项直接启动模糊器二进制文件。但是，使用`fx fuzz` devshell工具会更容易，它可以了解在哪里查找与相关文件相关的模糊文件，并知道各种常用选项。请尝试以下一项或多项：

 
* To see available commands and options: `$ fx fuzz help` *要查看可用的命令和选项：`$ fx fuzz help`
* To see available fuzzers: `$ fx fuzz list` *要查看可用的模糊器：`$ fx fuzz list`
* To start a fuzzer: `fx fuzz [package]/[fuzzer]` *启动模糊器：`fx fuzz [package] / [fuzzer]`

(Ignore errors of the form `Error: no such package.` These come from CIPD and should not affect the fuzzer!)  （忽略以下形式的错误：“错误：没有这样的软件包。”这些错误来自CIPD，不应影响模糊器！）

`package` and `fuzzer` match those reported by `fx fuzz list`, and may be abbreviated.  For commands that accept a single fuzzer, e.g. `check`, the abbreviated name must uniquely identify exactly onefuzzer. “ package”和“ fuzzer”与“ fx fuzz list”报告的匹配，可以缩写。对于接受单个模糊器的命令，例如“ check”（缩写名称）必须唯一地唯一标识一个模糊器。

When starting a fuzzer, the tool will echo the command it is invoking, prefixed by `+`.  This can be useful if you need to manually reproduce the bug with modified libFuzzer [options]. 启动模糊器时，该工具将回显正在调用的命令，并以“ +”为前缀。如果您需要使用修改后的libFuzzer [options]手动重现该错误，这将很有用。

 
## Q: How can I reproduce crashes found by the fuzzer? {#q-how-can-i-reproduce-crashes-found-by-the-fuzzer}  问：如何重现模糊器发现的崩溃？ {q我如何重现模糊器发现的崩溃} 

A: Use the [fx fuzz tool]:  答：使用[fx模糊工具]：

 
* To check on the fuzzer and list found artifacts: `fx fuzz check [package]/[fuzzer]` *要检查模糊器并列出找到的工件：`fx模糊检查[package] / [fuzzer]`
* To run the fuzzer on just the found artifacts: `fx fuzz repro [package]/[fuzzer]` *仅在找到的工件上运行模糊器：`fx fuzz repro [package] / [fuzzer]`

The test artifact are also copied to `//test_data/fuzzing/<package>/<fuzzer>/<timestamp>`. The most recent fuzzer run is symbolically linked to `//test_data/fuzzing/<package>/<fuzzer>/latest`. 测试工件也被复制到`// test_data / fuzzing / <package> / <fuzzer> / <timestamp>`。最新的模糊器运行在符号上链接到`// test_data / fuzzing / <package> / <fuzzer> / latest`。

As with `fx fuzz start`, the fuzzer will echo the command it is invoking, prefixed by `+`.  This can be useful if you need to manually reproduce the bug with modified parameters. 与“ fx fuzz start”一样，模糊器将回显正在调用的命令，并以“ +”为前缀。如果您需要使用已修改的参数手动重现该错误，这将很有用。

 
## Q: What should I do with these bugs? {#q-what-should-i-do-with-these-bugs}  问：我应该如何处理这些错误？ {我应该如何处理这些错误} 

A: File them, then fix them!  答：归档，然后修复！

Note: The bug tracker is currently only open to Googlers.  注意：错误跟踪器目前仅向Google员工开放。

When filing bugs, __please__ use the following custom labels: `found-by-fuzzing`, `libfuzzer` and `Sec-TriageMe`. This will help the security team see where fuzzers are being used and stayaware of any critical issues they are finding. 提交错误时，请使用以下自定义标签：“通过模糊查找”，“ libfuzzer”和“ Sec-TriageMe”。这将有助于安全团队了解在哪里使用了Fuzzer，并始终警惕他们发现的任何关键问题。

As with other potential security issues, bugs should be filed __in the component of the code under test__ (and __not__ in the [security component]).  Conversely, if you encounter problems orshortcomings in the fuzzing framework _itself_, please __do__ open bugs or feature requests in the[security component] with the label `libFuzzer`. 与其他潜在的安全问题一样，应在被测代码的组件中（和[安全组件]的__not__）提交错误。相反，如果您在模糊测试框架_itself_中遇到问题或不足，请__do__在[安全组件]中打开标签为libFuzzer的错误或功能请求。

As with all potential security issues, don't wait for triage to begin fixing the bug!  Once fixed, don't forget to link to the bug in the commit message.  This may also be a good time to considerminimizing and uploading your corpus at the same time (see the next section). 与所有潜在的安全性问题一样，请勿等待分类尝试修复该错误！一旦修复，别忘了链接到提交消息中的错误。这也是考虑同时最小化和上传您的语料库的好时机（请参阅下一节）。

 
## Q: How do I manage my corpus? {#q-how-do-i-manage-my-corpus}  问：如何管理语料库？ {如何管理我的语料库} 

A: When you first begin fuzzing a new target, the fuzzer may crash very quickly.  Typically, fuzzing has a large initial spike of defects found followed by a long tail.  Fixing these initial, shallowdefects will allow your fuzzer to reach deeper and deeper into the code. Eventually your fuzzer willrun for several hours (e.g. overnight) without crashing.  At this point, you will want to save the[corpus]. 答：当您第一次开始对新目标进行模糊测试时，模糊器可能会很快崩溃。通常，起毛有大量的初始缺陷尖峰，然后出现长尾巴。修复这些初始的浅缺陷，将使您的模糊器越来越深入代码。最终，您的模糊器将运行数小时（例如整夜）而不会崩溃。此时，您将要保存[corpus]。

To do this, use the [fx fuzz tool]: `fx fuzz merge <package>/<fuzzer>` 为此，请使用[fx fuzz工具]：`fx fuzz merge <package> / <fuzzer>

This will pull down the current corpus from [CIPD], merge it with your corpus on the device, minimize it, and upload it to [CIPD] as the *new* latest corpus. 这将从[CIPD]中提取当前语料库，将其与设备上的语料库合并，将其最小化，然后将其作为*最新*最新语料库上传到[CIPD]。

When uploaded, the corpus is tagged with the current revision of the integration branch.  If needed, you can retrieve older versions of the corpus relating to a specific version of the code:`fx fuzz fetch <package>/<fuzzer> <integration-revision>` 上载后，语料库将使用集成分支的当前修订版进行标记。如果需要，您可以检索与特定代码版本相关的语料库的旧版本：fx fuzz fetch <package> / <fuzzer> <integration-revision>

 
## Q: Can I use an existing third party corpus?  {#q-can-i-use-an-existing-third-party-corpus}  问：我可以使用现有的第三方语料库吗？ {q我可以使用现有的第三方语料库} 

A: Yes! by fetching the corpus, and then performing a normal corpus update:  A：是的！通过获取语料库，然后执行正常的语料库更新：

 
1. Fetch from a directory rather than CIPD:  1.从目录而非CIPD获取：
* `fx fuzz fetch --no-cipd --staging /path/to/third/party/corpus [package]/[fuzzer]`  *`fx fuzz fetch --no-cipd --staging / path / to / third / party / corpus [package] / [fuzzer]`
1. Upload the corpus to [CIPD].  1.将语料库上传到[CIPD]。
* `fx fuzz merge [package]/[fuzzer]`  *`fx模糊合并[package] / [fuzzer]`

 
## Q: Can I run my fuzzer on host? {#q-can-i-run-my-fuzzer-on-host}  问：我可以在主机上运行我的模糊器吗？ {我可以在主机上运行我的模糊器} 

A: Yes, although the extra tooling of `fx fuzz` is not currently supported.  This means you can build host fuzzers with the GN templates, but you'll need to manually run them, reproduce the bugsthey find, and manage their corpus data. 答：是的，尽管当前不支持`fx fuzz`的额外工具。这意味着您可以使用GN模板构建主机模糊测试器，但是您需要手动运行它们，重现他们发现的错误并管理其语料库数据。

If your fuzzers don't have Fuchsia dependencies, you can build host versions simply by setting `fuzz_host=true` in the `fuzzers_package`[gn fuzzers package]: 如果您的Fuzzer没有Fuchsia依赖性，则可以通过在`fuzzers_package` [gn fuzzers软件包]中设置`fuzz_host = true`来构建主机版本：

```python
fuzzers_package("overnet_fuzzers") {
  fuzzers = [ "packet_protocol:packet_protocol_fuzzer" ]
  fuzz_host = true
}
```
 

Upon building, the host fuzzers with can be found in in the host variant output directory, e.g. `//out/default/host_x64-asan-fuzzer`. 构建后，可以在主机变量输出目录中找到主机模糊器，例如`// out / default / host_x64-asan-fuzzer`。

 
## Q: How do I make my fuzzer better? {#q-how-do-i-make-my-fuzzer-better}  问：如何使我的模糊器变得更好？ {如何使我的模糊器更好} 

A: Once crashes begin to become infrequent, it may be because almost all the bugs have been fixed, but it may also be because the fuzzer isn't reaching new code that still has bugs.  Codecoverage information is needed to determine the quality of the fuzzer.  Use[source-based code coverage] to see what your current corpus reaches. 答：一旦崩溃开始变得罕见，可能是因为几乎所有的错误都已修复，但也可能是因为模糊器没有到达仍然有错误的新代码。需要代码覆盖信息来确定模糊器的质量。使用[基于源代码的覆盖率]查看您当前的语料库达到的范围。

Note: Source-based code coverage is under [active development][todo].  注意：基于源代码的覆盖范围在[active development] [todo]下。

If coverage in a certain area is low, there are a few options:  如果某个区域的覆盖率较低，则有以下几种选择：

 
  * Improve the [corpus].  If there are types of inputs that aren't represented well, add some manually.  For code dealing with large inputs with complex types (e.g. X.509 certificates), youprobably want to provide an initial corpus from the start. *提高[语料库]。如果某些输入类型显示不正确，请手动添加一些。对于处理复杂类型的大型输入的代码（例如X.509证书），您可能希望从一开始就提供一个初始语料库。
  * Add a [dictionary][dictionaries].  If the code deals with data that has a certain grammar (e.g. HTML), adding that grammar in a dictionary allows the fuzzer to produce more meaningful inputsfaster. *添加[字典] [字典]。如果代码处理的是具有特定语法（例如HTML）的数据，则在字典中添加该语法可以使模糊器更快地生成更有意义的输入。
  * Disable uninteresting shallow checks.  A function that verifies a checksum before proceeding is hard to fuzz, even though a maliciously crafted input may be easy enough to construct.  You candisable such checks by wrapping them in the `FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION`[build macro] described [above][gn fuzzer]. *禁用无趣的浅层检查。即使进行恶意制作的输入可能很容易构造，也很难对进行校验和的功能进行模糊处理。您可以通过将它们包装在[gn fuzzer]中所述的`FUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION` [build macro]中来禁用这些检查。

The "run, merge, measure, improve" steps can be repeated for as many iterations as you feel are needed to create a quality fuzzer.  Once ready, you'll need to upload your corpus and update the[GN fuzzer] in the appropriate project.  At this point, others will be able use your fuzzer.This includes [ClusterFuzz] which will automatically find new fuzzers and continuously fuzz them,updating their corpora, filing bugs for crashes, and closing them when fixed. 可以重复“运行，合并，测量，改进”步骤，进行多次重复，以创建质量模糊测试器。准备好之后，您将需要上载语料库，并在适当的项目中更新[GN模糊器]。此时，其他人将可以使用您的模糊器。包括[ClusterFuzz]，它将自动查找新的模糊器并对其进行连续模糊处理，更新其语料库，提交崩溃的bug，并在修复后关闭它们。

Note: ClusterFuzz integration is in [development][todo].  注意：ClusterFuzz集成在[development] [todo]中。

 
## Q: What can I expect in the future for fuzzing in Fuchsia? {#q-what-can-i-expect-in-the-future-for-fuzzing-in-fuchsia}  问：将来紫红色的绒毛有什么期望？ {q我能在紫红色的将来期待什么} 

A: As you can see from the various notes in this document, there's still plenty more to do!  答：从本文档的各种说明中可以看出，还有很多工作要做！

 
* Add additional language support, e.g for [Rust][rust-fuzzing] and [Go][go-fuzzing].  *添加其他语言支持，例如[Rust] [rust-fuzzing]和[Go] [go-fuzzing]。
* Add support for [AFL]  on Fuchsia.  Some design questions need to be worked out, as processes will not typically be run executed from the shell in the long term. *添加对紫红色的[AFL]支持。需要解决一些设计问题，因为从长远来看，通常不会从外壳执行流程。
* Continue to improve FIDL fuzzing, through both [libFuzzer][fidl_fuzzing] and [syzkaller].  *通过[libFuzzer] [fidl_fuzzing]和[syzkaller]继续改善FIDL模糊测试。
* *Maybe* extend [Clusterfuzz] work to include [OSS-Fuzz] as well.  * *也许*扩展[Clusterfuzz]的工作范围，使其也包括[OSS-Fuzz]。
* Provide source-based code coverage.  *提供基于源代码的覆盖范围。

We will continue to work on these features and others, and update this document accordingly as they become available. 我们将继续致力于这些功能和其他功能，并在可用时相应地更新本文档。

