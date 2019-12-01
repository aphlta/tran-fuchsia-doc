Contributing to FIDL ==================== 贡献给FIDL ====================

[TOC]  [目录]

 
## Overview  总览 

The [FIDL](README.md) toolchain is composed of roughly three parts:  [FIDL]（README.md）工具链大致包括三个部分：

 
1. Front-end, a.k.a. `fidlc`  1.前端，又称fidlc
    *   Parses and validates `.fidl` files  *解析并验证`.fidl`文件
    *   Calculates size, alignment, and offset of various structures  *计算各种结构的尺寸，对齐方式和偏移量
    *   Produces a [JSON IR][jsonir] (Intermediate Representation)  *产生[JSON IR] [jsonir]（中间表示）
2. Back-end  2.后端
    *   Works off the IR (except the C back-end)  *不使用IR（C后端除外）
    *   Produces target language specific code, which ties into the libraries for that language  *生成特定于目标语言的代码，并将其绑定到该语言的库中
3. Runtime Libraries  3.运行时库
    *   Implement encoding/decoding/validation of messages  *实现消息的编码/解码/验证
    *   Method dispatching mechanics  *方法调度机制

 
### Code Location  代码位置 

The front-end lives at [//zircon/tools/fidl/][fidlc-source], with tests in [//zircon/system/utest/fidl/][fidlc-tests]. 前端位于[// zircon / tools / fidl /] [fidlc-source]中，测试位于[// zircon / system / utest / fidl /] [fidlc-tests]中。

The back-end and runtime library locations are based on the target:  后端和运行时库位置基于目标：

Target     | Back-end                                               | Runtime Libraries -----------|--------------------------------------------------------|------------------C          | [//zircon/tools/fidl/lib/c_generator.cc][be-c]         | [//zircon/system/ulib/fidl/][rtl-c]C++        | [//garnet/go/src/fidl/compiler/backend/cpp/][be-cpp]   | [//zircon/system/ulib/fidl/][rtl-c] & [//sdk/lib/fidl/cpp/][rtl-cpp]Go         | [//garnet/go/src/fidl/compiler/backend/golang/][be-go] | [//third_party/go/src/syscall/zx/fidl/][rtl-go]Rust       | [//garnet/go/src/fidl/compiler/backend/rust/][be-rust] | [//garnet/public/lib/fidl/rust/fidl/][rtl-rust]Dart       | [//topaz/bin/fidlgen_dart/][be-dart]                   | [//topaz//public/dart/fidl/][rtl-dart]<br>[//topaz/bin/fidl_bindings_test/][bindings_test-dart]JavaScript | [chromium:build/fuchsia/fidlgen_fs][be-js]             | [chromium:build/fuchsia/fidlgen_js/runtime][rtl-js] 目标|后端|运行时库----------- || ------------------------------------ -------------------- | ------------------ C | [//zircon/tools/fidl/lib/c_generator.cc][be-c] | [// zircon / system / ulib / fidl /] [rtl-c] C ++ | [// garnet / go / src / fidl / compiler / backend / cpp /] [be-cpp] | [// zircon / system / ulib / fidl /] [rtl-c] [// sdk / lib / fidl / cpp /] [rtl-cpp] [// garnet / go / src / fidl / compiler / backend / golang /] [开始] | [// third_party / go / src / syscall / zx / fidl /] [rtl-go] [// garnet / go / src / fidl / compiler / backend / rust /] [be-rust] | [// garnet / public / lib / fidl / rust / fidl /] [rtl-rust] Dart | [// topaz / bin / fidlgen_dart /] [be-dart] | [// topaz // public / dart / fidl /] [rtl-dart] <br> [// topaz / bin / fidl_bindings_test /] [bindings_test-dart] JavaScript | [chromium：build / fuchsia / fidlgen_fs] [be-js] | [chromium：build / fuchsia / fidlgen_js / runtime] [rtl-js]

 
### Other FIDL Tools  其他FIDL工具 

**TBD: linter, formatter, gidl, difl, regen scripts, etc.**  ** TBD：linter，formatter，gidl，difl，regen脚本等**

 
### Common Development Tools  通用开发工具 

This is a crowdsourced section from the FIDL team on useful tools that they use for working on the FIDL codebase. 这是FIDL团队的众包部分，介绍了用于FIDL代码库的有用工具。

 
#### IDEs  集成开发环境 

Most of the FIDL team uses VSCode for development. Some useful plugins and workflows:  FIDL团队中的大多数人都使用VSCode进行开发。一些有用的插件和工作流程：

 
* The [remote ssh](https://code.visualstudio.com/docs/remote/ssh) feature works really well for doing remote work from your laptop. * [remote ssh]（https://code.visualstudio.com/docs/remote/ssh）功能非常适合在笔记本电脑上进行远程工作。
  * Setting up tmux or screen is also helpful for remote work, to preserve history and manage multiple sessions in the shell. *设置tmux或屏幕对于远程工作也很有帮助，以保留历史记录并在Shell中管理多个会话。
* The Fuchsia documentation has instructions for setting up language servers:  *紫红色的文档中包含有关设置语言服务器的说明：
  * [clangd](/docs/development/languages/c-cpp/editors.md) for c++  * [clangd]（/ docs / development / languages / c-cpp / editors.md）for c ++
  * [rls](/docs/development/languages/rust/editors.md) for rust  * [rls]（/ docs / development / languages / rust / editors.md）
* The [rewrap extension](https://marketplace.visualstudio.com/items?itemName=stkb.rewrap) is useful for automatically reflowing lines to a certain length (e.g. when editing markdown files). * [rewrap扩展名]（https://marketplace.visualstudio.com/items?itemName=stkb.rewrap）对于自动重排特定长度的行（例如，编辑降价文件时）很有用。
* To get automatic syntax highlighting for the bindings golden files, update the `file.associations` setting: *要获取绑定黄金文件的自动语法高亮显示，请更新`file.associations`设置：

  ```json
  "files.associations": {
      "*.test.fidl.json.rs.golden": "rust",
      "*.test.fidl.json.cc.golden": "cpp",
      "*.test.fidl.json.h.golden": "cpp",
      "*.test.fidl.json.llcpp.cc.golden": "cpp",
      "*.test.fidl.json.llcpp.h.golden": "cpp",
      "*.test.fidl.json.h.go.golden": "go",
      "*.test.fidl.json_async.dart.golden": "dart",
      "*.test.fidl.json_test.dart.golden": "dart"
  },
  ```
 

 
### C++ Style Guide  C ++样式指南 

We follow the [Fuchsia C++ Style Guide][cpp-style], with additional rules to further remove ambiguity around the application or interpretation of guidelines. 我们遵循[Fuchsia C ++样式指南] [cpp样式]，并附加了规则，以进一步消除有关应用程序或准则解释的歧义。

 
#### Constructors  建设者 

Always place the initializer list on a line below the constructor.  始终将初始化程序列表放在构造函数下方的一行上。

```cpp
// Don't do this.
SomeClass::SomeClass() : field_(1), another_field_(2) {}

// Correct.
SomeClass::SomeClass()
    : field_(1), another_field_(2) {}
```
 

 
#### Comments  评论 

Comments must respect 80 columns line size limit, unlike code which can extend to 100 lines size limit. 注释必须遵守80列的行大小限制，这与可以扩展到100行大小限制的代码不同。

 
##### Lambda captures  Lambda捕获 

 
* If a lambda escapes the current scope, capture all variables explicitly.  *如果lambda逃脱了当前作用域，则显式捕获所有变量。
* If the lambda is local (does not escape the current scope), prefer using a default capture by reference ("`[&]`"). *如果lambda是本地的（不会转义当前范围），则最好使用默认的引用捕获（“`[]`”）。

Seeing `[&]` is a strong signal that the lambda exists within the current scope only, and can be used to distinguish local from non-local lambdas. 看到[[]]是一个强有力的信号，说明lambda仅存在于当前范围内，可用于区分本地和非本地lambda。

```cpp
// Correct.
std::set<const flat::Library*, LibraryComparator> dependencies;
auto add_dependency = [&](const flat::Library* dep_library) {
  if (!dep_library->HasAttribute("Internal")) {
    dependencies.insert(dep_library);
  }
};
```
 

 
## General Setup  常规设置 

 
### Fuchsia Setup  紫红色设置 

Read the [Fuchsia Getting Started][getting_started] guide first.  首先阅读[Fuchsia入门] [getting_started]指南。

 
### fx set  外汇套 

```sh
fx set core.x64 --with //bundles:tests --with //topaz/packages/tests:all --with //sdk:modular_testing
```
 

or, to ensure there's no breakage with lots of bindings etc.:  或者，以确保不因大量的装订等而破损：

```sh
fx set terminal.x64 --with //bundles:kitchen_sink --with //vendor/google/bundles:buildbot
```
 

 
### symbolizer  符号化器 

To symbolize backtraces, you'll need a symbolizer in scope:  要符号化回溯，您需要在范围内使用符号化器：

```sh
export ASAN_SYMBOLIZER_PATH="$FUCHSIA_DIR/prebuilt/third_party/clang/$HOST_PLATFORM/bin/llvm-symbolizer"
```
 

 
## Compiling, and Running Tests  编译和运行测试 

We provide mostly one-liners to run tests for the various parts. When in doubt, refer to the "`Test:`" comment in the git commit message;we do our best to describe the commands used to validate our work there. 我们主要提供单线来对各个零件进行测试。如有疑问，请参考git commit消息中的“`Test：`”注释；我们将尽力描述用于验证此处的工作的命令。

 
### fidlc  场 

```sh
# optional; builds fidlc for the host with ASan <https://github.com/google/sanitizers/wiki/AddressSanitizer>
fx set core.x64 --variant=host_asan

# build fidlc
fx build zircon/tools
```
 

If you're doing extensive edit-compile-test cycles on `fidlc`, building with no optimizations can make a significant difference in the build speed. To optimize the build, change the `opt_level`setting in `zircon/public/gn/config/levels.gni`. 如果您要在`fidlc`上进行大量的编辑-编译-测试循环，则不进行优化就可以大大提高构建速度。要优化构建，请在“ zircon / public / gn / config / levels.gni”中更改“ opt_level”设置。

To avoid accidentally committing this change, run:  为避免意外提交此更改，请运行：

```
git update-index --skip-worktree zircon/public/gn/config/levels.gni
```
 

If you want to allow the changes to be committed again, run:  如果要允许再次提交更改，请运行：

```
git update-index --no-skip-worktree zircon/public/gn/config/levels.gni
```
 

 
### fidlc tests  现场测试 

fidlc tests are at:  fidlc测试位于：

 
* [//zircon/system/utest/fidl-compiler/][fidlc-compiler-tests].  * [// zircon / system / utest / fidl-compiler /] [fidlc-compiler-tests]。
* [//zircon/system/utest/fidl/][fidlc-tests].  * [// zircon / system / utest / fidl /] [fidlc-tests]。
* [//zircon/system/utest/fidl-coding/tables/][fidlc-coding-tables-tests].  * [// zircon / system / utest / fidl-coding / tables /] [fidlc-coding-tables-tests]。
* [//zircon/system/utest/fidl-simple][fidl-simple (C runtime tests)].  * [// zircon / system / utest / fidl-simple] [fidl-simple（C运行时测试）]。

```sh
# build & run fidlc tests
fx build system/utest:host
$FUCHSIA_DIR/out/default.zircon/host-x64-linux-clang/obj/system/utest/fidl-compiler/fidl-compiler-test.debug

# build & run fidl-coding-tables tests
# --with-base puts all zircon tests under /boot with the bringup.x64 target, or /system when using the core.x64 target
fx set bringup.x64 --with-base //garnet/packages/tests:zircon   # optionally append "--variant asan"
fx build
fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-coding-tables-test
```
 

```sh
fx build zircon/tools
$FUCHSIA_DIR/out/default.zircon/tools/fidlc \
  --tables $FUCHSIA_DIR/zircon/system/utest/fidl/fidl/extra_messages.cc \
  --files $FUCHSIA_DIR/zircon/system/utest/fidl/fidl/extra_messages.test.fidl
```
To regenerate the FIDL definitions used in unit testing, run:  要重新生成单元测试中使用的FIDL定义，请运行：

 
### fidlgen (LLCPP, HLCPP, Rust, Go)  fidlgen（LLCPP，HLCPP，Rust，Go） 

Build:  建立：

```sh
fx build garnet/go/src/fidl
```
 

Run:  跑：

```sh
$FUCHSIA_DIR/out/default/host_x64/fidlgen
```
 

Some example tests you can run:  您可以运行一些示例测试：

```sh
fx run-host-tests fidlgen_cpp_test
fx run-host-tests fidlgen_cpp_ir_test
fx run-host-tests fidlgen_golang_ir_test
```
 

To regenerate the goldens:  要重新生成黄金：

```sh
fx exec garnet/go/src/fidl/compiler/backend/typestest/regen.sh
```
 

 
### fidlgen_dart  fidlgen_dart 

Some example tests you can run:  您可以运行一些示例测试：

```sh
fx run-host-tests fidlgen_dart_backend_ir_test
```
 

To regenerate the goldens:  要重新生成黄金：

```sh
fx exec topaz/bin/fidlgen_dart/regen.sh
```
 

 
### C runtime  C运行时 

```sh
fx set core.x64 --with-base //garnet/packages/tests:zircon
fx build
fx qemu -kN

# On Fuchsia device's shell
$ runtests -t fidl-test
$ runtests -t fidl-simple-test
```
 

```
fx qemu -kN -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-test
fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-simple-test
```
You might get lucky with  您可能会很幸运

When the test completes, you're running in the QEMU emulator. To exit, use **`Ctrl-A x`**. 测试完成后，您将在QEMU仿真器中运行。要退出，请使用Ctrl-A x **。

Alternatively, if you build including the shell you can run these commands from the shell: 另外，如果您构建包括外壳程序，则可以从外壳程序运行以下命令：

```sh
Tab 1> fx set core.x64 --with-base //garnet/packages/tests:zircon
Tab 1> fx build && fx qemu -kN

Tab 2> fx shell
Tab 2(shell)> runtests -t fidl-simple-test
Tab 2(shell)> runtests -t fidl-test
```
 

```sh
fx build zircon && fx run-host-tests fidl-test
```
Some of the C runtime tests can run on host: This only includes a few tests, so be sure to check the output to see if it isrunning the test you care about. 一些C运行时测试可以在主机上运行：这仅包括一些测试，因此请确保检查输出以查看它是否正在运行您关注的测试。

 
### C++ runtime  C ++运行时 

You first need to have Fuchsia running in an emulator. Here are the steps:  首先，您需要在模拟器中运行Fuchsia。步骤如下：

```sh
Tab 1> fx build && fx serve-updates

Tab 2> fx qemu -kN

Tab 3> fx run-test fidl_tests
```
 

There are separate tests for LLCPP that can be run in the same way as `fidl_tests`:  LLCPP有单独的测试，可以通过与`fidl_tests`相同的方式运行：

 
* fidl_llcpp_types_test  * fidl_llcpp_types_test
* fidl_llcpp_conformance_test  * fidl_llcpp_conformance_test

 
### Go runtime  去运行 

You first need to have Fuchsia running in an emulator. Here are the steps:  首先，您需要在模拟器中运行Fuchsia。步骤如下：

```sh
Tab 1> fx build && fx serve-updates

Tab 2> fx qemu -kN

Tab 3> fx run-test go_fidl_tests
```
 

As with normal Go tests, you can pass [various flags][go-test-flags] to control execution, filter test cases, run benchmarks, etc. For instance: 与普通的Go测试一样，您可以传递[variable flags] [go-test-flags]来控制执行，过滤测试用例，运行基准测试等。例如：

```sh
Tab 3> fx run-test go_fidl_tests -- -test.v -test.run 'TestAllSuccessCases/.*xunion.*'
```
 

 
### Rust runtime  Rust运行时 

You first need to have Fuchsia running in an emulator. Here are the steps:  首先，您需要在模拟器中运行Fuchsia。步骤如下：

```sh
Tab 1> fx build && fx serve-updates

Tab 2> fx qemu -kN

Tab 3> fx run-test rust_fidl_tests
```
 

 
### Dart runtime  Dart运行时 

The Dart FIDL bindings tests are in [//topaz/bin/fidl_bindings_test/][bindings_test-dart].  Dart FIDL绑定测试位于[// topaz / bin / fidl_bindings_test /] [bindings_test-dart]中。

You first need to have Fuchsia running in an emulator. Here are the steps:  首先，您需要在模拟器中运行Fuchsia。步骤如下：

```sh
Tab 1> fx build && fx serve-updates

Tab 2> fx qemu -kN

Tab 3> fx run-test fidl_bindings_test
```
 

 
### Dart Compatibility Test  飞镖兼容性测试 

The language bindings compatibility test is located in [//topaz/bin/fidl_compatibility_test][compatibility_test],and is launched from a shell script. 语言绑定兼容性测试位于[// topaz / bin / fidl_compatibility_test] [compatibility_test]中，并且是从Shell脚本启动的。

```sh
fx set core.x64 ... --with //topaz/packages/tests:all
```
First, ensure that you include the proper test targets. For instance:  首先，请确保您包括正确的测试目标。例如：

To build this test, use:  要构建此测试，请使用：

```sh
fx build topaz/bin/fidl_compatibility_test:fidl_compatibility_test_topaz
```
 

You first need to have Fuchsia running in an emulator. Here are the steps:  首先，您需要在模拟器中运行Fuchsia。步骤如下：

```sh
Tab 1> fx build && fx serve-updates

Tab 2> fx qemu -kN

Tab 3> fx run-test fidl_compatibility_test_topaz
```
 

 
### GIDL  吉德尔 

To rebuild GIDL:  要重建GIDL：

```sh
fx build host-tools/gidl
```
 

 
### All Tests  所有测试 

| Name                     | Test Command                                        | Directories Covered                                                     | |--------------------------|-----------------------------------------------------|-------------------------------------------------------------------------|| gidl parser              | fx run-host-tests gidl_parser_test                  | tools/fidl/gidl/parser                                                  || fidlgen hlcpp            | fx run-host-tests fidlgen_cpp_test                  | garnet/go/src/fidl/compiler/backend/cpp                                 || fidlgen hlcpp ir         | fx run-host-tests fidlgen_cpp_ir_test               | garnet/go/src/fidl/compiler/backend/cpp/ir                              || fidlgen llcpp            | fx run-host-tests fidlgen_llcpp_test                | garnet/go/src/fidl/compiler/llcpp_backend                               || fidlgen overnet          | fx run-host-tests fidlgen_cpp_overnet_internal_test | garnet/go/src/fidl/compiler/backend/cpp_overnet_internal                || fidlgen golang           | fx run-host-tests fidlgen_golang_test               | garnet/go/src/fidl/compiler/backend/golang                              || fidlgen golang ir        | fx run-host-tests fidlgen_golang_ir_test            | garnet/go/src/fidl/compiler/backend/golang/ir                           || fidlgen rust             | fx run-host-tests fidlgen_rust_test                 | garnet/go/src/fidl/compiler/backend/rust                                || fidlgen rust ir          | fx run-host-tests fidlgen_rust_ir_test              | garnet/go/src/fidl/compiler/backend/rust/ir                             || fidlgen syzkaller        | fx run-host-tests fidlgen_syzkaller_test            | garnet/go/src/fidl/compiler/backend/syzkaller                           || fidlgen syzkaller ir     | fx run-host-tests fidlgen_syzkaller_ir_test         | garnet/go/src/fidl/compiler/backend/syzkaller/ir                        || fidlgen type definitions | fx run-host-tests fidlgen_types_test                | garnet/go/src/fidl/compiler/backend/types                               || fidl c runtime host test | fx run-host-tests fidl-test                         | zircon/system/ulib/fidl                                                 || c++ host unittests       | fx run-host-tests fidl_cpp_host_unittests           | sdk/lib/fidl                                                            || c++ bindings tests       | fx run-test fidl_tests                              | sdk/lib/fidl                                                            || llcpp bindings tests     | fx run-test fidl_llcpp_types_test                   | garnet/go/src/fidl/compiler/llcpp_backend                               || go bindings tests        | fx run-test go_fidl_tests                           | third_party/go/syscall/zx/fidl third_party/go/syscall/zx/fidl/fidl_test || dart bindings tests      | fx run-test fidl_bindings_test                      | topaz/public/dart/fidl                                                  || rust bindings            | fx run-test rust_fidl_tests                         | garnet/public/lib/fidl/rust/fidl                                        | |姓名|测试命令涵盖的目录| | -------------------------- | ---------------------- ------------------------------- || ------------------ -------------------------------------------------- ----- || gidl解析器| fx运行主机测试gidl_parser_test |工具/ fidl / gidl / parser || fidlgen hlcpp | fx运行主机测试fidlgen_cpp_test |石榴石/ go / src / fidl / compiler / backend / cpp || fidlgen hlcpp ir | fx运行主机测试fidlgen_cpp_ir_test |石榴石/ go / src / fidl / compiler / backend / cpp / ir || fidlgen llcpp | fx运行主机测试fidlgen_llcpp_test |石榴石/ go / src / fidl / compiler / llcpp_backend || fidlgen overnet | fx运行主机测试fidlgen_cpp_overnet_internal_test |石榴石/ go / src / fidl / compiler / backend / cpp_overnet_internal || fidlgen golang | fx运行主机测试fidlgen_golang_test |石榴石/ go / src / fidl / compiler / backend / golang || fidlgen golang ir | fx运行主机测试fidlgen_golang_ir_test |石榴石/ go / src / fidl / compiler / backend / golang / ir || fidlgen锈| fx运行主机测试fidlgen_rust_test |石榴石/ go / src / fidl / compiler /后端/ rust || fidlgen rust ir | fx运行主机测试fidlgen_rust_ir_test |石榴石/ go / src / fidl / compiler / backend / rust / ir || fidlgen syzkaller | fx运行主机测试fidlgen_syzkaller_test |石榴石/ go / src / fidl / compiler / backend / syzkaller || fidlgen syzkaller ir | fx运行主机测试fidlgen_syzkaller_ir_test |石榴石/ go / src / fidl / compiler / backend / syzkaller / ir || fidlgen类型定义| fx运行主机测试fidlgen_types_test |石榴石/ go / src / fidl / compiler / backend / types || FIDL C运行时主机测试| fx运行主机测试fidl测试|锆石/系统/ ulib / fidl || C ++主机单元测试| fx运行主机测试fidl_cpp_host_unittests | sdk / lib / fidl || c ++绑定测试| fx运行测试fidl_tests | sdk / lib / fidl || llcpp绑定测试| fx运行测试fidl_llcpp_types_test |石榴石/ go / src / fidl / compiler / llcpp_backend ||进行绑定测试| fx运行测试go_fidl_tests | third_party / go / syscall / zx / fidl third_party / go / syscall / zx / fidl / fidl_test ||飞镖绑定测试| fx运行测试fidl_bindings_test |黄玉/公共/飞镖/菲尔德||防锈剂| fx运行测试rust_fidl_tests |石榴石/公共/ lib / fidl / rust / fidl |

 

The following requires: fx set bringup.x64 --with-base //garnet/packages/tests:zircon  以下要求：fx设置Bringup.x64 --with-base // garnet / packages / tests：zircon

| Name                      | Test Command                                                                                                  | Directories Covered     | |---------------------------|---------------------------------------------------------------------------------------------------------------|-------------------------|| fidlc host test           | $FUCHSIA_DIR/out/default.zircon/host-x64-linux-clang/obj/system/utest/fidl-compiler/fidl-compiler-test.debug  | zircon/system/host/fidl || fidl coding tables test   | fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-coding-tables-test                               | zircon/system/host/fidl || fidl c runtime test       | fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-test                                             | zircon/system/ulib/fidl || fidl c runtime test       | fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-simple-test                                      | zircon/system/ulib/fidl || fidl c-llcpp interop test | fx qemu -k -c zircon.autorun.boot=/boot/bin/runtests+-t+fidl-llcpp-interop-test                               | zircon/system/ulib/fidl | |姓名|测试命令涵盖的目录| | --------------------------- | --------------------- -------------------------------------------------- ---------------------------------------- | --------- ---------------- || fidlc主机测试| $ FUCHSIA_DIR / out / default.zircon / host-x64-linux-clang / obj / system / utest / fidl-compiler / fidl-compiler-test.debug |锆石/系统/主机/ FIDL || fidl编码表测试| fx qemu -k -c zircon.autorun.boot = / boot / bin / runtests + -t + fidl-coding-tables-test |锆石/系统/主机/ FIDL || FIDL C运行时测试| fx qemu -k -c zircon.autorun.boot = / boot / bin / runtests + -t + fidl-test |锆石/系统/ ulib / fidl || FIDL C运行时测试| fx qemu -k -c zircon.autorun.boot = / boot / bin / runtests + -t + fidl-simple-test |锆石/系统/ ulib / fidl || fidl c-llcpp互操作测试| fx qemu -k -c zircon.autorun.boot = / boot / bin / runtests + -t + fidl-llcpp-interop-test |锆石/系统/ ulib / fidl |

 
### All Regen Commands  所有再生命令 

| Name                                 | Regen Commands                                                              | Input                                                             | Output                                                                                                                                                                                                                                                                                       | |--------------------------------------|-----------------------------------------------------------------------------|-------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|| fidlgen goldens                      | fx exec $FUCHSIA_DIR/garnet/go/src/fidl/compiler/backend/typestest/regen.sh | garnet/go/src/fidl/compiler/backend/goldens                       | garnet/go/src/fidl/compiler/backend/goldens                                                                                                                                                                                                                                                  || dart fidlgen goldens                 | fx exec $FUCHSIA_DIR/topaz/bin/fidlgen_dart/regen.sh                        | garnet/go/src/fidl/compiler/backend/goldens                       | topaz/bin/fidlgen_dart/goldens                                                                                                                                                                                                                                                               || gidl conformance test generation     | fx exec $FUCHSIA_DIR/tools/fidl/gidl-conformance-suite/regen.sh             | tools/fidl/gidl-conformance-suite                                 | third_party/go/src/syscall/zx/fidl/conformance/impl.go third_party/go/src/syscall/zx/fidl/fidl_test/conformance_test.go sdk/lib/fidl/cpp/conformance_test.cc topaz/bin/fidl_bindings_test/test/test/conformance_test_types.dart topaz/bin/fidl_bindings_test/test/test/conformance_test.dart || dangerous identifiers                | garnet/tests/fidl-dangerous-identifiers/generate.py                         | garnet/tests/fidl-dangerous-identifiers/dangerous_identifiers.txt | garnet/tests/fidl-dangerous-identifiers/cpp/ garnet/tests/fidl-dangerous-identifiers/fidl/                                                                                                                                                                                                   || regen third party go                 | fx exec $FUCHSIA_DIR/third_party/go/regen-fidl                              |                                                                   |                                                                                                                                                                                                                                                                                              || regen c-llcpp interop test bindings  | fx exec $FUCHSIA_DIR/zircon/system/utest/fidl-llcpp-interop/gen_llcpp.sh    | zircon/system/utest/fidl-llcpp-interop/*.test.fidl                | zircon/system/utest/fidl-llcpp-interop/generated/                                                                                                                                                                                                                                            || regen llcpp fidl::Bind test bindings | fx exec $FUCHSIA_DIR/zircon/system/utest/fidl/gen.sh                        | zircon/system/utest/fidl/llcpp.test.fidl                          | zircon/system/utest/fidl/generated/                                                                                                                                                                                                                                                          || regen fidl-async test bindings       | fx exec $FUCHSIA_DIR/zircon/system/ulib/fidl-async/test/gen_llcpp.sh        | zircon/system/ulib/fidl-async/test/simple.test.fidl               | zircon/system/ulib/fidl-async/test/generated/                                                                                                                                                                                                                                                || regen llcpp service test bindings    | fx exec $FUCHSIA_DIR/zircon/system/utest/service/gen_llcpp.sh               | zircon/system/utest/service/test.test.fidl                        | zircon/system/utest/service/generated/                                                                                                                                                                                                                                                       || checked in production llcpp bindings | fx build -k 0 tools/fidlgen_llcpp_zircon:update                             | FIDL definitions in zircon/system/fidl/                           | "gen/" folder relative to the corresponding FIDL definition                                                                                                                                                                                                                                  | |姓名|再生命令|输入|输出| | -------------------------------------- | ---------- -------------------------------------------------- ----------------- | -------------------------------- ----------------------------------- | -------------- -------------------------------------------------- -------------------------------------------------- -------------------------------------------------- -------------------------------------------------- -------------------------------------------------- ---------------------- || fidlgen黄金|外汇执行$ FUCHSIA_DIR / garnet / go / src / fidl / compiler / backend / typestest / regensh |石榴石/去/ SRC / FIDL /编译器/后端/黄金石榴石/ go / src / fidl / compiler / backend / goldens || dart fidlgen goldens |外汇执行人$ FUCHSIA_DIR / topaz / bin / fidlgen_dart / regensh |石榴石/去/ SRC / FIDL /编译器/后端/黄金黄玉/ bin / fidlgen_dart / goldens || gidl一致性测试生成|外汇执行$ FUCHSIA_DIR / tools / fidl / gidl-conformance-suite / regensh |工具/ fidl / gidl-conformance-suite | third_party / go / src / syscall / zx / fidl / conformance / impl进入third_party / go / src / syscall / zx / fidl / fidl_test / conformance_test去sdk / lib / fidl / cpp / conformance_testcc黄玉/ bin / fidl_bindings_test / test / test / conformance_test_typesdart topaz / bin / fidl_bindings_test / test / test / conformance_test飞镖||危险标识符|石榴石/测试/ fidl-危险标识符/生成py |石榴石/测试/ fidl-危险标识符/ dangerous_identifierstxt |石榴石/测试/ fidl危险标识符/ cpp /石榴石/测试/ fidl危险标识符/ fidl / ||再生第三方去|外汇执行人$ FUCHSIA_DIR / third_party / go / regen-fidl | | || regen c-llcpp互操作测试绑定|外汇执行$ FUCHSIA_DIR / zircon / system / utest / fidl-llcpp-interop / gen_llcppsh |锆石/系统/最大/ FIDL-llcpp-interop / *测试fidl | zircon / system / utest / fidl-llcpp-interop / Generated / || regen llcpp fidl :: Bind测试绑定|外汇执行$ FUCHSIA_DIR / zircon / system / utest / fidl / gensh |锆石/系统/最大/ FIDL / LLCPP测试fidl |锆石/系统/最大/ FIDL /生成/ || regen fidl异步测试绑定|外汇执行$ FUCHSIA_DIR / zircon / system / ulib / fidl-async / test / gen_llcppsh |锆石/系统/ ulib / fidl-async /测试/简单测试fidl | zircon / system / ulib / fidl-async / test / generated / || regen llcpp服务测试绑定|外汇执行$ FUCHSIA_DIR / zircon / system / utest / service / gen_llcppsh |锆石/系统/测试/服务/测试测试fidl |锆石/系统/测试/服务/生成/签入生产llcpp绑定| fx build -k 0工具/ fidlgen_llcpp_zircon：更新| zircon / system / fidl /中的FIDL定义相对于相应FIDL定义的“ gen /”文件夹

 
## Debugging (host)  调试（主机） 

There are several ways of debugging issues in host binaries. This section gives instructions for the example case where `fidlc --files test.fidl` is crashing: 有几种方法可以调试主机二进制文件中的问题。本节提供有关`fidlc --files test.fidl`崩溃的示例情况的说明：

 
- [GDB](#GDB)  -[GDB]（GDB）
- [Asan](#ASan)  -[Asan]（ASan）
- [Valgrind](#Valgrind)  -[Valgrind]（Valgrind）

Note: Even with all optimizations turned off, the binaries in `out/default/host_x64` are stripped. For debugging, you should use the binarieswith the `.debug` suffix, such as`out/default.zircon/host-x64-linux-clang/obj/tools/fidl/fidlc.debug`. 注意：即使关闭了所有优化，“ out / default / host_x64”中的二进制文件也会被剥离。为了进行调试，您应该使用带有.debug后缀的二进制文件，例如out / default.zircon / host-x64-linux-clang / obj / tools / fidl / fidlc.debug。

 
### GDB {#GDB}  GDB {GDB} 

Start GDB:  启动GDB：

```sh
gdb --args out/default.zircon/host-x64-linux-clang/obj/tools/fidl/fidlc.debug --files test.fidl
```
 

Then, enter "r" to start the program.  然后，输入“ r”以启动程序。

 
### ASan {#ASan}  阿桑{ASan} 

Ensure you are compiling with ASan enabled:  确保在启用ASan的情况下进行编译：

```sh
fx set core.x64 --variant=host_asan
fx build host_x64/fidlc
```
 

Then run `out/default/host_x64/fidlc --files test.fidl`. That binary should be the same as `out/default.zircon/host-x64-linux-asan/obj/tools/fidl/fidlc`. 然后运行`out / default / host_x64 / fidlc --files test.fidl`。该二进制文件应该与`out / default.zircon / host-x64-linux-asan / obj / tools / fidl / fidlc`相同。

 
### Valgrind {#Valgrind}  瓦尔格隆德（Valgrind） 

On Google Linux machines, you may need to install a standard version of Valgrind instead of using the pre-installed binary: 在Google Linux机器上，您可能需要安装标准版本的Valgrind，而不是使用预先安装的二进制文件：

```
sudo apt-get install valgrind
```
 

Then:  然后：

```sh
valgrind -v -- out/default.zircon/host-x64-linux-clang/obj/tools/fidl/fidlc.debug --files test.fidl
```
 

 
## Workflows  工作流程 

 
### Language evolutions  语言演变 

One common task is to evolve the language, or introduce stricter checks in `fidlc`. These changes typically follow a three phase approach: 一项常见的任务是发展语言，或在`fidlc`中引入更严格的检查。这些更改通常遵循三个阶段的方法：

 
1. Write the new compiler code in `fidlc`;  1.在`fidlc`中编写新的编译器代码；
2. Use this updated `fidlc` to compile all layers, including vendor/google, make changes as needed; 2.使用此更新的`fidlc`编译所有层，包括供应商/谷歌，根据需要进行更改；
3. When all is said and done, the `fidlc` changes can finally be merged.  3.说完一切，终于可以合并`fidlc`更改。

All of this assumes that (a) code which wouldn't pass the new checks, or (b) code that has new features, is *not* introduced concurrently between step 2 and step 3.That typically is the case, however, it is ok to deal with breaking rollersonce in a while. 所有这些都假定（a）无法通过新检查的代码，或（b）具有新功能的代码，在步骤2和步骤3之间不是同时*引入的，但是通常是这样。可以在一段时间内处理打破Rollersonce的问题。

 
### Go fuchsia.io and fuchsia.net  去fuchsia.io和fuchsia.net 

To update all the saved `fidlgen` files, run the following command, which automatically searches for and generates the necessary go files: 要更新所有已保存的`fidlgen`文件，请运行以下命令，该命令将自动搜索并生成必要的go文件：

```sh
fx exec third_party/go/regen-fidl
```
 

 
## FAQs  常见问题 

 
### Why is the C back-end different than all other back-ends?  为什么C后端与所有其他后端不同？ 

TBD  待定

 
### Why is fidlc in the zircon repo?  为什么在锆石仓库中使用fidlc？ 

TBD  待定

 
### Why aren't all back-ends in one tool?  为什么不是所有后端都使用一种工具？ 

We'd actually like all back-ends to be in _separate_ tools!  实际上，我们希望所有后端都在_separate_工具中！

Down the road, we plan to have a script over all the various tools (`fidlc`, `fidlfmt`, the various back-ends) to make all things accessible easily,and manage the chaining of these things.For instance, it should be possible to generate Go bindings in one command such as: 接下来，我们计划在所有各种工具（“ fidlc”，“ fidlfmt”，各种后端）上编写一个脚本，以使所有内容都易于访问，并管理这些内容的链接。例如，它应该可以在一个命令中生成Go绑定，例如：

```sh
fidl gen --library my_library.fidl --binding go --out-dir go/src/my/library
```
 

Or format a library in place with:  或使用以下方法就地格式化库：

```sh
fidl fmt --library my_library.fidl -i
```
 

