 
# Lint  皮棉 

We use clang-tidy to lint C++ code and aim to keep the repository warning-clean. The linter is configured in the root level `.clang-tidy` file. Developersshould not create additional configuration files at a lower level, asthis will cause disagreements in the tree. 我们使用clang-tidy整理C ++代码，旨在保持警告源干净。短绒是在根目录“ .clang-tidy”文件中配置的。开发人员不应在较低级别上创建其他配置文件，因为这将导致树中的分歧。

 
## How to lint  如何皮棉 

`fx lint` is a Fuchsia script that wraps language-specific linters in a common command line interface. It gathers a list of files, based on the options youspecify, separates them by matching linter, and executes each required linter.`clang-tidy` is used for C and C++ files. fx lint是一种紫红色的脚本，将特定于语言的短绒包裹在一个通用的命令行界面中。它根据您指定的选项收集文件列表，通过匹配linter分离它们，并执行每个必需的linter。`clang-tidy`用于C和C ++文件。

Without any other arguments, `fx lint` lints the files in your most recent git commit, and passes them through the linter: 没有任何其他参数，`fx lint`会在最新的git commit中将文件插入文件中，并通过linter传递它们：

```
fx lint
```
 

To restrict linting to C++, add a double-dash (--) followed by the file pattern(s) to match, such as: 要将linting限制为C ++，请添加双破折号（-），后跟要匹配的文件模式，例如：

```
fx lint -- '*.cc' '*.cpp'
```
 

To run a specific GN target through the linter, use:  要通过lint运行特定的GN目标，请使用：

```
fx lint --target=<target>
```
 

In order to lint all files under the current working directory, add `--all`. Running `fx lint --all` from the top-level `fuchsia` directory is generally notrecommended, and will likely take several hours to complete. Be certain you`cd` to the best top level directory for your analysis requirements. For example: 为了整理当前工作目录下的所有文件，添加`--all`。通常不建议从顶层`fuchsia`目录运行`fx lint --all`，这可能需要几个小时才能完成。确定您已将CD定位到最佳的顶层目录，以进行分析。例如：

```
(cd <your/subdir>; fx lint --all -- '*.cc')
```
 

You can also add `--fix` in order to automatically generate fixes for some (but not all) of the warnings. 您还可以添加--fix以自动为某些（但不是全部）警告生成修复程序。

Additional options and examples are documented in the tool itself. For the most up to date documentation on `fx lint`, including examples, run: 工具本身中记录了其他选项和示例。有关`fx lint`的最新文档，包括示例，请运行：

```
fx lint --help
```
 

 
## Suppressing warnings  禁止警告 

Any warning can be suppressed by adding a `// NOLINT(<check_name>)` or a `// NOLINTNEXTLINE(<check_name>)` comment to the offending line. It is alsopossible to disable the check entirely within the repository by editing theroot level `.clang-tidy` file. 通过将“ // NOLINT（<check_name>）”或“ // NOLINTNEXTLINE（<check_name>）”注释添加到有问题的行可以抑制任何警告。也可以通过编辑根目录.clang-tidy文件来完全禁用存储库中的检查。

 
## Checks  支票 

There are a number of check categories enabled, and specific checks within them have been disabled for the reasons below. The list of enabled check categoriesis as follows: 启用了许多检查类别，并且由于以下原因已禁用其中的特定检查。启用的检查类别列表如下：

 
 - `bugprone-*`  -`bugprone- *`
 - `clang-diagnostic-*`  -`clang-diagnostic- *`
 - `google-*`  -`google- *`
 - `misc-*`  -`misc- *`
 - `modernize-`  -`modernize-`
 - `performance-*`  -`performance- *`
 - `readability-*`  -`可读性-*`

This list tracks the reasons for which we disabled in particular [checks]:  此列表跟踪了我们特别禁用的[检查]的原因：

 
 - `clang-diagnostic-unused-command-line-argument` - ninja-generated compilation database contains the linker argument which ends up unused and triggers thiswarning for every file -`clang-diagnostic-unused-command-line-argument`-ninja生成的编译数据库包含链接器参数，该参数最终未使用并触发每个文件的警告
 - `misc-noexcept*` - Fuchsia doesn't use C++ exceptions  -`misc-noexcept *`-紫红色不使用C ++异常
 - `misc-non-private-member-variables-in-classes` - We don't allow classes/structs with a mix of private and public members, but all public is fine. -“其他类中的非私有成员变量”-我们不允许私人/公共成员混合使用的类/结构，但所有公共场所都可以。
 - `modernize-deprecated-headers` - Fuchsia uses old-style C headers  -`modernize-deprecated-headers`-紫红色使用老式的C标头
 - `modernize-use-nodiscard` - Not generally used in the Fuchsia codebase  -`modernize-use-nodiscard`-紫红色代码库中通常不使用
 - `modernize-raw-string-literal` - the check was suggesting to convert `\xFF` literals, which we'd rather keep in the escaped form. -`modernize-raw-string-literal`-检查建议转换为\ xFF`文字，我们宁愿保留转义形式。
 - `modernize-return-braced-init-list` - concerns about readability of returning braced initialization list for constructor arguments, prefer to use aconstructor explicitly -`modernize-return-braced-init-list`-有关为构造函数参数返回支撑初始化列表的可读性的担忧，更喜欢显式使用构造函数
 - `modernize-use-emplace` - enabled the IgnoreImplicitConstructors option to comply with [Abseil Tip of the Week #112](https://abseil.io/tips/112). -`modernize-use-emplace`-启用IgnoreImplicitConstructors选项以符合[Abseil本周技巧112]（https://abseil.io/tips/112）。
 - `modernize-use-equals-delete` - flagging all gtest TEST_F  -`modernize-use-equals-delete`-标记所有gtest TEST_F
 - `modernize-use-trailing-return-type` - Fuchsia C++ code typically uses the `int foo()` style of defining functions, and not the `auto foo() -> int`style as recommended by this check. -`modernize-use-trailing-return-type`-紫红色的C ++代码通常使用“ int foo（）”样式定义函数，而不是本检查建议的“ auto foo（）-> int`样式”。
 - `readability-implicit-bool-conversion` - Fuchsia C++ code commonly uses implicit bool cast of pointers and numbers -`readability-implicit-bool-conversion`-紫红色C ++代码通常使用指针和数字的隐式布尔转换
 - `readability-isolate-declaration` - Zircon code commonly uses paired declarations.  -`readability-isolate-declaration`-Zircon代码通常使用成对的声明。
 - `readability-uppercase-literal-suffix` - Fuchsia C++ code chooses not to impose a style on this. -`readability-uppercase-literal-suffix`-紫红色C ++代码选择不对此施加样式。

