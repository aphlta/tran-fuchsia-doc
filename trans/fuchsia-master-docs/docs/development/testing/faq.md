 
# Testing: Questions and Answers  测试：问题与解答 

You are encouraged to add your own questions (and answers) here!  我们鼓励您在此处添加您自己的问题（和答案）！

[TOC]  [目录]

 
## Q: How do I define a new unit test?  问：如何定义新的单元测试？ 

A: Use language-appropriate constructs, like GTest for C++. You can define a new file if need be, such as: 答：使用适合语言的结构，例如GTest for C ++。您可以根据需要定义一个新文件，例如：

(in a BUILD.gn file)  （在BUILD.gn文件中）

```code
executable("unittests") {
  output_name = "scenic_unittests"
  testonly = true
  sources = ["some_test.cc"],
  deps = [":some_dep"],
}
```
 

 
## Q: What ensures it is run?  问：什么可以确保其运行？ 

A: An unbroken chain of dependencies that roll up to your `fx set` command's universe of available packages (expandable using the[`--with`](/tools/devshell/set)flag), typically going through the `all` target of`//<layer>/packages/tests/BUILD.gn`, such as[`//garnet/packages/tests:all`](/garnet/packages/tests/BUILD.gn). 答：不间断的依赖关系链会累积到您的`fx set`命令的可用软件包的范围内（可使用[`--with`]（/ tools / devshell / set）标志进行扩展），通常会经过“ all” // <layer> / packages / tests / BUILD.gn`的目标，例如[`//garnet/packages/tests:all`](/garnet/packages/tests/BUILD.gn）。

For example:  例如：

`//src/ui/scenic:scenic_unittests`  `// src / ui / scenic：scenic_unittests`

is an executable, listed under the "tests" stanza of  是可执行文件，在以下文件的“测试”节下列出

`//src/ui/scenic:scenic_tests`  `// src / ui / scenic：scenic_tests`

which is a package, which is listed in a package group  这是一个软件包，在软件包组中列出

`//garnet/packages/tests:scenic`  `// garnet / packages / tests：scenic`

which is itself included in the catch-all group,  它本身就包含在全部使用的组中，

`//garnet/packages/tests:all`  `// garnet / packages / tests：all`

Your product definition (typically one found in [products/](/products) may ormay not transitively include this test group. If it doesn't, add it to your `fxset` command, like so: 您的产品定义（通常在[products /]（/ products）中找到一个，可能会或可能不会包含此测试组。如果没有，请将其添加到您的`fxset`命令中，如下所示：

`fx set ... --with //garnet/packages/tests:scenic_tests`  `fx set ... --with // garnet / packages / tests：scenic_tests`

Typically, one just adds a new test to an existing binary, or a new test binary to an existing package. 通常，只需将新测试添加到现有二进制文件中，或将新测试二进制添加到现有软件包中。

 
## Q: How do I run this unit test on a QEMU instance?  问：如何在QEMU实例上运行此单元测试？ 

There's the easy way if your QEMU has networking, and the hard way if it doesn't. 如果您的QEMU具有联网功能，则有一种简单的方法，而如果没有，则很难。

A (with networking): In one terminal, start your QEMU instance with `fx qemu -N`. Next, on another terminal, type in `fx run-test scenic_tests`. A（具有网络连接）：在一个终端中，使用`fx qemu -N`启动您的QEMU实例。接下来，在另一个终端上，输入“ fx run-test Scenic_tests”。

This invocation runs all the test executables in the `scenic_tests` package.  该调用将运行`scenic_tests`包中的所有测试可执行文件。

A (no networking): Start a QEMU instance (`fx qemu`), and then *manually* invoke the `runtests` command. A（不联网）：启动QEMU实例（`fx qemu`），然后“手动”调用“ runtests”命令。

In the QEMU shell, type in `run-test-component scenic_tests`. The argument is a specific directory containing the test executables. 在QEMU shell中，键入“ run-test-component Scenic_tests”。该参数是包含测试可执行文件的特定目录。

Note Well! Without networking, the files are loaded into the QEMU instance at startup. So after rebuilding a test, you'll need to shutdown and re-start theQEMU instance to see the rebuilt test. 注意！如果不联网，则文件将在启动时加载到QEMU实例中。因此，在重建测试之后，您需要关闭并重新启动QEMU实例才能查看重建的测试。

To exit QEMU, `dm shutdown`.  要退出QEMU，请关闭dm。

 
## Q: How do I run this unit test on my development device?  问：如何在开发设备上运行此单元测试？ 

A: Either manual invocation, like in QEMU, **or** `fx run-test` to a running device. 答：就像在QEMU中一样，手动调用还是对运行中的设备执行fx run-test。

Note that the booted device may not contain your binary at startup, but `fx run-test` will build the test binary, ship it over to the device, and run it,while piping the output back to your workstation terminal. Slick! 请注意，引导的设备在启动时可能不包含您的二进制文件，但是`fx run-test`将构建测试二进制文件，将其运送到设备上并运行，同时将输出通过管道传输回您的工作站终端。光滑！

Make sure your device is running (hit Ctrl-D to boot an existing image) and connected to your workstation. 确保您的设备正在运行（按Ctrl-D启动现有映像）并连接到工作站。

From your workstation, `fx run-test scenic_tests` will serially run through all test executables contained in the `scenic_tests` package. 在您的工作站上，`fx run-test Scenic_tests`将依次运行`scenic_tests`软件包中包含的所有测试可执行文件。

To run just one test executable, `fx run-test scenic_test -t scenic_unittests`, where the argument to `-t` is the executable name. 要仅运行一个测试可执行文件，即fx run-test Scenic_test -t Scenic_unittests，其中-t的参数是可执行文件名称。

You can automatically rebuild, install, and run your tests on every source file change with `fx -i`. For instance: `fx -i run-test scenic_tests`. 您可以使用`fx -i`在每个源文件更改时自动重建，安装和运行测试。例如：`fx -i run-test Scenic_tests`。

 
## Q: Where are the test results captured?  问：在哪里捕获测试结果？ 

A: The output is directed to your terminal.  答：输出直接到您的终端。

There does exist a way to write test output into files (including a summary JSON file), which is how CQ bots collect the test output for automated runs. 确实存在一种将测试输出写入文件（包括JSON摘要文件）的方法，这是CQ机器人如何收集测试输出以进行自动运行的方式。

 
## Q: How to disable a test? How to find and run disabled tests? {#disable-test}  问：如何禁用测试？如何查找和运行禁用的测试？ {disable-test} 

A: There are several ways to do this. Whenever doing any of these, be sure to file a bug and reference that bug in a comment in the code that disables thetest. 答：有几种方法可以做到这一点。无论何时执行这些操作，请务必提交一个错误并在禁用测试的代码中的注释中引用该错误。

 
### Tag the test as flaky  将测试标记为片状 

You can do this by adding "flaky" to the `tags` field in the [test environment](/docs/development/testing/environments.md). This operateson the entire test target (which corresponds to an executable). It will prevent this targetfrom running on the builders in the commit queue, and enable the target on special flakybuilders that continue to run the test in CI. Be sure to note the bug in acomment in the BUILD.gn file.[Example change](https://fuchsia-review.googlesource.com/c/topaz/+/296629/3/bin/flutter_screencap_test/BUILD.gn). 您可以通过在[测试环境]（/ docs / development / testing / environments.md）的`tags'字段中添加“易碎”来实现。这对整个测试目标（对应于可执行文件）进行操作。它将阻止此目标在提交队列中的构建器上运行，并在继续在CI中运行测试的特殊易碎构建器上启用目标。确保在BUILD.gn文件中注意到注释中的错误。[示例更改]（https://fuchsia-review.googlesource.com/c/topaz/+/296629/3/bin/flutter_screencap_test/BUILD.gn） 。

If you want to disable only some tests that are part of a larger test target, you'll need to split the target into two GN targets, and tag one as flaky. 如果只想禁用属于较大测试目标的一部分测试，则需要将目标分为两个GN目标，并将其中一个标记为易碎。

 
### C++ googletest only: Prefix name with DISABLED  仅适用于C ++ googletest：前缀名称为DISABLED 

To disable a particular test inside of a larger test executable, you can mark it as disabled. Disabled tests are defined by having their nameprefixed with `DISABLED_`. One way to find them is therefore simply `git grepDISABLED_`. 要在较大的测试可执行文件中禁用特定测试，可以将其标记为已禁用。禁用的测试是通过使用“ DISABLED_”前缀来定义的。因此找到它们的一种方法就是`git grepDISABLED_`。

If running the test outputs `YOU HAVE 1 DISABLED TEST`, you can also pass the following flags to find out which test is disabled: `fx run-test scenic_tests ----gtest_list_tests --gtest_filter=*DISABLED_*`. 如果运行测试输出“ YOU HAVE 1 DISABLED TEST”，您还可以传递以下标志来找出禁用了哪些测试：`fx run-test Scenic_tests ---- gtest_list_tests --gtest_filter = * DISABLED_ *。

To force-run disabled tests: `fx run-test scenic_tests -- --gtest_also_run_disabled_tests`. 强制运行禁用的测试：`fx run-test Scenic_tests---gtest_also_run_disabled_tests`。

 
### Mark test disabled  标记测试已禁用 

Alternatively, you may also disable an entire test executable within a package containing several test executables. To do this, edit the `BUILD.gn` asfollows: `tests = [ { name = "scenic_unittests", disabled = true } ]`. As aresult, `scenic_unittests` will be put in a `disabled` sub-directory of`/pkgfs/packages/<package_name>/0/test`, and will not be run by the CQ system. 或者，您也可以在包含多个测试可执行文件的程序包中禁用整个测试可执行文件。为此，请编辑如下的“ BUILD.gn”：“ tests = [{name =“ scenic_unittests”，disabled = true}]。因此，“ scenic_unittests”将被放在“ / pkgfs / packages / <package_name> / 0 / test”的“ disabled”子目录中，并且不会由CQ系统运行。

 
### Comment out the test  注释掉测试 

To disable a particular test inside of a larger test executable, you can comment out the code that defines that test. 要在较大的测试可执行文件中禁用特定测试，可以注释掉定义该测试的代码。

 
## Q: How do I run a bunch of tests automatically? How do I ensure all dependencies are tested?  问：如何自动运行一堆测试？如何确保所有依赖项都经过测试？ 

A: Upload your patch to Gerrit and do a CQ dry run.  答：将补丁上传到Gerrit并进行CQ空运行。

 
## Q: How do I run this unit test in a CQ dry run?  问：如何在CQ空运行中运行此单元测试？ 

A: Clicking on CQ dry run (aka +1) will take your CL's properly defined unit test and run it on multiple bots, one for each build target (*x86-64* versus*arm64*, *release* versus *debug*). Each job will have an output page showingall the tests that ran. 答：单击CQ空运行（又名+1）将进行CL正确定义的单元测试，并在多个机器人上运行它，每个构建目标一个（* x86-64 *与* arm64 *，* release *与* debug * ）。每个作业都有一个输出页面，显示所有已运行的测试。

 
## Q: How do I use some build time artifacts in my unit test?  问：如何在单元测试中使用一些构建时间工件？ 

A: The simplest artifact is just a file that is in your source directory.  For this you just need to add it to `resources` attribute of the package definitionof your unit test.  For example, you may do something like this in your`BUILD.gn`: 答：最简单的工件只是源目录中的一个文件。为此，您只需要将其添加到单元测试的包定义的`resources`属性即可。例如，您可以在`BUILD.gn`中执行以下操作：

```code
rustc_binary("my-great-app") {
  with_unit_tests = true

  ...
}

test_package("my-great-app-tests") {
  deps = [
    ":my-great-app_test",
  ]

  resources = [
    {
      path = "source.zip"
      dest = "testing.zip"
    }
  ]
```
 

The file will be available as `/pkg/data/testing.zip` inside the environment where the test binary will be executed. 在将执行测试二进制文件的环境中，该文件将以`/ pkg / data / testing.zip`的形式提供。

