 
# Overview  总览 

There are various tools at the disposal of Fuchsia developers for linting and formatting code. This is a general overview of those tools for each language, as well as a description of how additionallint checks should be added and the accuracy standards to which they should be held. Fuchsia开发人员可以使用各种工具来整理和格式化代码。这是针对每种语言的那些工具的概述，并描述了应如何添加附加毛绒检查以及应遵循的精度标准。

Note that this doesn't try to explain the specific language configurations for each linter and formatter. Though the purpose of linting and formatting is to encourage and enforce recommendationsaround style and best practices, each relevant language has its own guides that explain thedecisions made and the configurations enabled. 请注意，这并不试图解释每个linter和formatter的特定语言配置。尽管整理和格式化的目的是鼓励和实施有关样式和最佳实践的建议，但是每种相关语言都有其自己的指南，这些指南解释了所做的决定和启用的配置。

 
# Tooling Integration  工具整合 

The Fuchsia team provides two ways to format and lint code: subcommands in the developer-side fx tool, and integrated Tricium analysis on uploaded CLs. In addition, a subset of formatting andlinting is eligible to be directly included in the build, with strict limitations around accuracy. Fuchsia团队提供了两种格式化和整理代码的方法：开发人员端fx工具中的子命令，以及对上载CL的集成Tricium分析。此外，格式化和皮棉的子集有资格直接包含在版本中，但对准确性有严格的限制。

 
## Developer tooling (IDEs and fx)  开发人员工具（IDE和FX） 

The primary developer tooling suite is the fx command and its subcommands. It provides two subcommands relevant here: fx format-code and fx lint. Each runs the relevant tooling on a list offiles and prints the output to the terminal’s stdout/stderr. Running fx lint assumes that thedeveloper has already run fx build; if not, many of the linters will produce errors related tomissing files that are created by the build. 开发人员的主要工具套件是fx命令及其子命令。它提供了两个与此处相关的子命令：fx格式代码和fx lint。每个工具都在文件列表上运行相关工具，并将输出打印到终端的stdout / stderr。运行fx lint假定开发人员已经运行过fx build。否则，许多短毛猫将产生与缺少由构建创建的文件有关的错误。

The list of files can be specified in one of three ways:  可以通过以下三种方式之一指定文件列表：
 - The list of files changed since the second-to-last Git commit, including committed, modified, and cached files (this is the default behavior) -自倒数第二次Git提交以来已更改的文件列表，包括已提交，已修改和缓存的文件（这是默认行为）
 - A list of files passed in a comma-separated list to the --files flag  -以逗号分隔的列表传递到--files标志的文件列表
 - The list of files in the sources of the GN target passed to the --target flag  -传递给--target标志的GN目标源中的文件列表

Formatting is done in-place. Linting is by default warn-only, but users can pass the --fix flag to fx lint to automatically fix the errors for which the tools provide fixes. 格式化是就地完成的。默认情况下，lint仅警告，但用户可以将--fix标志传递给fx lint，以自动修复工具提供修复的错误。

Most editors will also integrate formatters and linters to allow developers to automatically format-on-save or format-on-keybinding. In most cases, setup (if any) consists of pointing the IDEat the relevant configuration file and Fuchsia-distributed tool binary. 大多数编辑器还将集成格式化程序和Linter，以使开发人员能够自动保存格式或键绑定格式。在大多数情况下，设置（如果有）包括将IDE指向相关的配置文件和Fuchsia分发的工具二进制文件。

 
## Integrated tooling (Tricium)  集成工具（Tricium） 

Tricium is a service that integrates with the Gerrit code review system to surface relevant warnings in a way that does not block commits. It triggers on each patchset uploaded by a user withcommit access to the Fuchsia repository and runs two suites of tooling analysis. Tricium是一项与Gerrit代码检查系统集成的服务，以不阻止提交的方式显示相关警告。它在用户有权访问Fuchsia存储库的用户上传的每个补丁集上触发，并运行两套工具分析工具。

The formatter analysis does a minimal checkout (no third_party, no prebuilts) and extracts the list of changed files from the patch commit. It runs the relevant formatter based on file extension oneach file. If the produced formatted file differs from the file content in the uploaded patch,Tricium posts a comment on the patch explaining how to run the appropriate formatter on the file. 格式化程序分析会进行最少的签出（没有third_party，没有预建），并从补丁提交中提取已更改文件的列表。它基于每个文件的文件扩展名运行相关的格式化程序。如果生成的格式化文件与上载补丁程序中的文件内容不同，Tricium会在补丁程序上发表评论，说明如何在文件上运行适当的格式化程序。

The linter analysis does a full checkout and does a minimal build (to produce the necessary configuration files and headers). It extracts the list of changed files from the patch commit andthen runs the relevant linter based on file extension. Machine-readable outputs are requested fromthe linters, and if warnings are produced the output is then parsed and collected into commentform. Tricium then comments on the appropriate line with the linter warning. 短绒分析将进行完整的检出并进行最小的构建（以生成必要的配置文件和头文件）。它从补丁提交中提取已更改文件的列表，然后基于文件扩展名运行相关的linter。从短绒机请求机器可读的输出，如果产生警告，则将输出解析并收集到注释表中。然后Tricium在适当的行上加上linter警告进行评论。

Tricium, where possible, only runs the tools on the changed lines in a commit, though not all linters support this behavior. For the ones that do, this is so that existing but irrelevant linterrors do not distract from the CL itself and only directly relevant lints are surfaced. Tricium在可能的情况下，仅在提交时在更改的行上运行工具，尽管并非所有的linter都支持此行为。对于那些这样做的人，这样做是为了使现有但不相关的棉绒错误不会分散到CL本身，而只会出现直接相关的棉绒。

Analysis results are often based on heuristics. As a result, they do from time to time produce false positives. Fuchsia aims to support a high bar for these analyzers, with any analyzer withgreater than 10% error rates as measured by the metrics produced by the Tricium service being disabled. 分析结果通常基于启发式方法。结果，它们会不时产生误报。倒挂金钟旨在为这些分析仪提供更高的标准，禁用通过Tricium服务生成的指标来测量的任何分析仪，其错误率大于10％。

New linters should generally be added to the existing Tricium recipes. Since checkout/build times are by far the most costly in these builds (the analysis itself takes at best a few seconds, and atworst a few minutes, while checkouts and/o builds can take much longer), it is more efficient fromboth time and infrastructure resource perspectives to simply extend the existing builders. Theselection of which recipe to extend should be based on the amount of information needed, e.g. ifprebuilts/third_party code are not needed to run the analysis, the minimal checkout recipe shouldbe used. 通常应将新的短绒添加到现有的Tricium配方中。由于结帐/构建时间迄今为止是这些构建中最昂贵的（分析本身最多需要几秒钟，并且至少要花几分钟，而结账和/或构建可能要花费更长的时间），因此从时间和成本两方面都效率更高基础架构资源的观点来简单地扩展现有的构建器。选择要扩展的配方应基于所需的信息量，例如如果不需要prebuilts / third_party代码来运行分析，则应使用最少的结帐方法。

 
## Build Integration  建立整合An alternative for linter checks that provide zero false-positive rates is to include them in the build. Currently, the Fuchsia build runs the dartanalyzer in this capacity as a type checker.Adding additional checks to this category is not encouraged unless it is certain that they do notfire on false positives. 提供零假阳性率的短绒检查的另一种方法是将它们包括在构建中。目前，Fuchsia构建以这种类型的检查器的身份运行dartanalyzer。除非鼓励我们确保不会因误报而触发此类检查，否则不鼓励在此类别中添加其他检查。

These checks are directly implemented in the build (generally as actions that run the relevant script), and so will cause the whole build to fail if they catch errors. They also extend the buildtime, and so should only be used in cases where they provide valuable and correct information tothe developer. 这些检查直接在构建中实现（通常作为运行相关脚本的操作），因此如果它们捕获错误，将导致整个构建失败。它们还延长了构建时间，因此仅应在向开发人员提供有价值且正确的信息的情况下使用。

 
# Standards  标准品 

 
## Formatters  格式化程序 

Formatters should adhere to the relevant style guides, but whether the formatter’s output is the source-of-truth for the style guide is left up to languages and their style arbiters. When aformatter is changed in the upstream community (e.g. when the Rust community changes `rustfmt`),the updated formatter will roll into Fuchsia with the toolchain. This doesn't happen often, but canbe the cause of conflicting formats between Tricium and local tooling until developers update touse the new toolchain. 格式制定者应遵守相关的样式指南，但是格式制定者的输出是否是样式指南的真实来源，则取决于语言及其样式仲裁者。当上游社区中的格式化程序发生更改时（例如，Rust社区更改了“ rustfmt”时），更新的格式化程序将随工具链一起进入紫红色。这种情况很少发生，但是可能是Tricium和本地工具之间格式冲突的原因，直到开发人员更新为使用新的工具链。

Generally, Fuchsia’s support for formatters is dependent on developers running the formatting commands. The only automation is from Tricium, which will warn if a file differs from theformatter’s output, but will not block the CL’s commit. 通常，紫红色对格式器的支持取决于运行格式命令的开发人员。唯一的自动化来自Tricium，它会在文件与格式化程序的输出不同时发出警告，但不会阻止CL的提交。

 
## Linters  短绒 

Linters should generally provide useful and actionable comments to developers. Since they are often heuristics-based, they can produce false positives, but any linter exceeding the 10% false positiverate should be disabled. The process for adding a linter check is to file a bug requesting the newcheck, outlining its value and the expected false positive rate. Removing a linter check can eitherbe done by filing a bug or submitting a patch with the requested configuration change. Linters通常应向开发人员提供有用且可操作的评论。由于它们通常是基于启发式的，因此它们会产生误报，但是任何超过10％误报率的短绒都应该禁用。添加棉绒支票的过程是提交一个要求新支票的错误，概述其价值和预期的误报率。可以通过提交错误或提交带有请求的配置更改的补丁来删除linter检查。

Only linters that are guaranteed to not produce false positives should be implemented in the build itself. These should be enforced by both local builds and by CQ, so that there are no surpriseswhen developers attempt to submit their code. 只有保证不会产生误报的短绒在构建本身中才应实施。这些应该由本地版本和CQ强制执行，因此当开发人员尝试提交其代码时，不要感到意外。

 
# Language Tools  语言工具 

Each supported language provides a formatter and optionally linters. This section describes the integration of these tools into the Fuchsia workflow. While the formatters tend to bestraightforward, the tooling is a bit complex in how the linters are integrated. In most cases,developers do not need to understand the internals of `fx` and Tricium. 每种受支持的语言都提供格式化程序和可选的linters。本节描述将这些工具集成到Fuchsia工作流程中。尽管格式化程序通常很简单，但在整合短绒的方式上，工具却有些复杂。在大多数情况下，开发人员无需了解`fx`和Tricium的内部。

All commands are assumed to be run from the root of a Fuchsia checkout.  假定所有命令都从紫红色结帐的根开始运行。

 
## C/C++  C / C ++ 

C/C++ code uses [`clang-format`](https://clang.llvm.org/docs/ClangFormat.html) and [`clang-tidy`](https://clang.llvm.org/extra/clang-tidy/). These are distributed as prebuilts from the Clang toolchain. Both use root-level configuration files (`.clang-format` and `.clang-tidy`,respectively). Developers should not create additional configuration files at a lower level, asthis will cause disagreements in the tree. C / C ++代码使用[`clang-format`]（https://clang.llvm.org/docs/ClangFormat.html）和[`clang-tidy`]（https://clang.llvm.org/extra/ clang-tidy /）。这些是从Clang工具链中预构建的。两者都使用根级配置文件（分别为.clang-format和.clang-tidy）。开发人员不应在较低级别上创建其他配置文件，因为这将导致树中的分歧。

`clang-format` is run on source files as follows:  在源文件上运行`clang-format`如下：

```sh
prebuilt/third_party/clang/$HOST_PLATFORM/bin/clang-format \
-i \
-style=file \
-fallback-style=Google \
-sort-includes \
$FILES
```
 

Before you run `clang-tidy`, you must:  在运行`clang-tidy`之前，您必须：

 
* Create the compilation command database. The compilation command database is created from running `fx compdb`. *创建编译命令数据库。编译命令数据库是通过运行`fx compdb`创建的。
* Build the set of generated headers. The `clang-tidy` tool partially compiles the source code and most C and C++ code in Fuchsiaincludes headers generated as part of the build. *构建生成的标题集。 “ clang-tidy”工具会部分编译源代码，而Fuchsia中的大多数C和C ++代码都包含作为构建的一部分生成的标头。

Once the compilation database and generated headers are present, you can run the `run-clang-tidy.py` script to start the `clang-tidy` tool. The script handles handles parallelization and deduplicationof errors which is necessary when the same header is included in multiple source files. When youuse this script, you must also pass the `clang-tidy` and `clang-apply-replacements` binaries fromthe distributed Fuchsia toolchain to make sure the correct ones are used. 一旦存在编译数据库和生成的头文件，您就可以运行`run-clang-tidy.py`脚本来启动`clang-tidy`工具。该脚本处理并行化和重复数据删除错误，当多个源文件中包含相同的标头时，这是必需的。使用此脚本时，还必须传递分布式Fuchsia工具链中的`clang-tidy`和`clang-apply-replacements`二进制文件，以确保使用正确的二进制文件。

```sh
export CLANG_TOOLCHAIN_PREFIX=prebuilt/third_party/clang/$HOST_PLATFORM
$CLANG_TOOLCHAIN_PREFIX/share/clang/run-clang-tidy.py \
  -clang-tidy-binary $CLANG_TOOLCHAIN_PREFIX/bin/clang-tidy \
  -clang-apply-replacements-binary $CLANG_TOOLCHAIN_PREFIX/bin/clang-apply-replacements \
  $FILES
```
 

An optional `-fix` flag can be added to automatically apply fixes. This is available in the developer-side tooling. 可以添加一个可选的-fix标志来自动应用修订。在开发人员工具中可用。

 
## Rust  锈 

Rust code uses [`rustfmt`](https://github.com/rust-lang/rustfmt) and [`clippy`](https://github.com/rust-lang/rust-clippy). These are distributed as prebuilts from the Rust toolchain. The formatter has a root-level configuration file (`rustfmt.toml`). Rust代码使用[`rustfmt`]（https://github.com/rust-lang/rustfmt）和[`clippy`]（https://github.com/rust-lang/rust-clippy）。这些都是从Rust工具链中作为预构建件分发的。格式化程序有一个根级配置文件（`rustfmt.toml`）。

`rustfmt` runs on source files as follows:  rustfmt在源文件上运行如下：

```sh
prebuilt/third_party/rust/${HOST_PLATFORM}/bin/rustfmt \
--config-path=rustfmt.toml \
--unstable-features \
--skip-children \
$FILES
```
 

TODO(TC-588): Document clippy once implementation details are finalized.  待办事项（TC-588）：一旦实施细节定案，文件便会变得片刻。

 
## Go  走 

Go code uses [`gofmt`](https://golang.org/cmd/gofmt/) and [`go vet`](https://golang.org/cmd/vet/). These are built as part of the Go toolchain build, and also distributed in the Go host toolchain prebuilts. Go代码使用[`gofmt`]（https://golang.org/cmd/gofmt/）和[`go vet`]（https://golang.org/cmd/vet/）。这些是在Go工具链构建的一部分中构建的，并在预构建的Go主机工具链中分发。

`gofmt` runs on source files as follows:  gofmt在源文件上运行如下：

```sh
prebuilt/third_party/go/$HOST_PLATFORM/bin/gofmt -s -w $FILES
```
 

TODO(TC-587): Document go vet once implementation details are finalized.  待办事项（TC-587）：一旦实施细节确定下来，请审查文件。

 
## Dart  镖 

Dart uses [`dartfmt`](https://github.com/dart-lang/dart_style) and [`dartanalyzer`](https://github.com/dart-lang/sdk/tree/master/pkg/analyzer_cli). These are distributed as prebuilts from the Dart toolchain. The `dartanalyzer` is run as part of the build rather than as a check, as it performs type-checking andother assertive checks. Dart使用[`dartfmt`]（https://github.com/dart-lang/dart_style）和[`dartanalyzer`]（https://github.com/dart-lang/sdk/tree/master/pkg/analyzer_cli ）。这些作为Dart工具链中的预构建件进行分发。 dartanalyzer是作为构建的一部分而不是作为检查运行的，因为它执行类型检查和其他肯定检查。

`dartfmt` runs on source files as follows:  dartfmt在源文件上运行如下：

```sh
prebuilt/third_party/dart/${HOST_PLATFORM}/bin/dartfmt -w $FILES
```
 

The `dartanalyzer` is run as part of the build, triggered when the [`dart_library`](/build/dart/dart_library.gni) GN template is invoked. The [invocation](/build/dart/gen_analyzer_invocation.py) is: dartanalyzer`作为构建的一部分运行，在调用[`dart_library`]（/ build / dart / dart_library.gni）GN模板时触发。 [invocation]（/ build / dart / gen_analyzer_invocation.py）是：

```sh
prebuilt/third_party/dart/${HOST_PLATFORM}/bin/dartanalyzer \
  --packages=$DOT_PACKAGES_FILE \
  --dart-sdk=prebuilt/third_party/dart/${HOST_PLATFORM} \
  --fatal-warnings \
  --fatal-hints \
  --fatal-lints \
  --options=$PACKAGE_ROOT/analysis_options \
  $FILES
  ```
 

 
## FIDL  FIDL 

FIDL code uses the `fidl-format` and `fidl-lint` tools. These are built as host tools from in-tree. Before running either the `zircon/tools` target must be built so that the binaries exist. FIDL代码使用`fidl-format`和`fidl-lint`工具。这些是从树中作为宿主工具构建的。在运行任何一个zircon / tools目标之前，必须先构建二进制文件。

`fidl-format` runs on source files as follows:  fidl-format在源文件上运行如下：

```sh
$ZIRCON_BUILD_DIR/tools/fidl-format -i $FILES
```
 

`fidl-lint` runs on source files as follows:  fidl-lint在源文件上运行如下：

```sh
$ZIRCON_BUILD_DIR/tools/fidl-lint $FILES
```
 

 
## GN  GN 

GN files use the [`gn format`](https://gn.googlesource.com/gn/+/master/docs/reference.md#cmd_format) subcommand. There is not a linter. This is distributed as part of the GN prebuilt. GN文件使用[`gn格式`]（https://gn.googlesource.com/gn/+/master/docs/reference.mdcmd_format）子命令。没有短绒。这是作为GN预先构建的一部分分发的。

It runs on source files as follows:  它在源文件上运行，如下所示：

```sh
prebuilt/third_party/gn/$HOST_PLATFORM/gn format <files>
```
