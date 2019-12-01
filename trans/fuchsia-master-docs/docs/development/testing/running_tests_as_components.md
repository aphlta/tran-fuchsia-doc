 
# Running tests as components  将测试作为组件运行 

Tests on Fuchsia can either be run as standalone executables or as components. Standalone executables are invoked in whatever environment the test runnerhappens to be in, whereas components executed in a test runner are run in ahermetic environment. 紫红色的测试可以作为独立的可执行文件或组件运行。独立可执行文件在测试运行程序将要处于的任何环境中调用，而在测试运行程序中执行的组件则在密封环境中运行。

These hermetic environments are fully separated from the host services, and the test manifests can stipulate that new instances of services should be started inthis environment, or services from the host should be plumbed in to the testenvironment. 这些封闭的环境与主机服务完全隔离，测试清单可以规定应在此环境中启动服务的新实例，或者应将来自主机的服务插入到测试环境中。

This document aims to outline the idiomatic way for a developer to configure their test artifacts to be run as components. This document is targeted towardsdevelopers working inside of `fuchsia.git`, and the workflow described isunlikely to work for SDK consumers. 本文档旨在概述开发人员配置其测试工件以作为组件运行的惯用方式。本文档针对的是在`fuchsia.git`内部工作的开发人员，所描述的工作流程不太可能适用于SDK使用者。

An example setup of a test component is available at `//examples/hello_world/rust`. 在// examples / hello_world / rust中可以找到测试组件的示例设置。

 
## Building the test  建立测试 

The exact GN invocations that should be used to produce a test vary between different classes of tests and different languages. The rest of this documentassumes that test logic is being built somewhere, and that the test output issomething that can be run as a component. For C++ and Rust, this would be theexecutable file the build produces. 在不同类别的测试和不同语言之间，应用于生成测试的确切GN调用有所不同。本文档的其余部分假定在某个地方构建了测试逻辑，并且测试输出可以作为组件运行。对于C ++和Rust，这将是生成的可执行文件。

Further documentation for building tests is [available for Rust][rust_testing].  有关构建测试的更多文档，[可用于Rust] [rust_testing]。

 
## Packaging and component-ifying the tests  将测试打包并打包 

Once the build rule for building a test executable exists, a component manifest referencing the executable and a package build rule containing the executableand manifest must be created. 一旦存在用于构建测试可执行文件的构建规则，则必须创建引用该可执行文件的组件清单以及包含该可执行文件和清单的程序包构建规则。

 
### Component manifests  组件清单 

The component manifest exists to inform the component framework how to run something. In this case, it's explaining how to run the test binary. This filetypically lives in a `meta` directory next to the `BUILD.gn` file, and will beincluded in the package under a top level directory also called `meta`. 存在组件清单是为了通知组件框架如何运行某些程序。在这种情况下，它说明了如何运行测试二进制文件。该文件通常位于“ BUILD.gn”文件旁边的“元”目录中，并将包含在软件包中的顶层目录（也称为“元”）下。

The simplest possible component manifest for running a test would look like this: 用于运行测试的最简单的组件清单如下所示：

```cmx
{
    "program": {
        "binary": "test/hello_world_rust_bin_test"
    }
}
```
 

This component, when run, would invoke the `test/hello_world_rust_bin_test` binary in the package. 这个组件在运行时会在包中调用`test / hello_world_rust_bin_test`二进制文件。

This example manifest may be insufficient for many use cases as the program will have a rather limited set of capabilities, for example there will be no mutablestorage available and no services it can access. The `sandbox` portion of themanifest can be used to expand on this. As an alternative to the prior example,this example will give the component access to storage at `/cache` and willallow it to talk to the service located at `/svc/fuchsia.logger.LogSink`. 对于许多用例，此示例清单可能不足，因为该程序将具有相当有限的功能集，例如，将没有可变存储可用，也没有可访问的服务。清单的“沙盒”部分可用于对此进行扩展。作为先前示例的替代，此示例将使组件可以访问“ / cache”中的存储，并允许其与位于“ /svc/fuchsia.logger.Log.ink”中的服务进行通信。

```cmx
{
    "program": {
        "binary": "test/hello_world_rust_bin_test"
    },
    "sandbox": {
        "features": [ "isolated-cache-storage" ],
        "services": [ "fuchsia.logger.LogSink" ]
    }
}
```
 

Test components can also have new instances of services created inside their test environment, thus isolating the impact of the test from the host. In thefollowing example, the service available at `/svc/fuchsia.example.Service` willbe handled by a brand new instance of the service referenced by the URL. 测试组件还可以在其测试环境中创建新的服务实例，从而将测试的影响与主机隔离开。在下面的示例中，`/ svc / fuchsia.example.Service`中可用的服务将由URL引用的服务的全新实例处理。

```cmx
{
    "program": {
        "binary": "test/hello_world_rust_bin_test"
    },
    "facets": {
        "fuchsia.test": {
            "injected-services": {
                "fuchsia.example.Service": "fuchsia-pkg://fuchsia.com/example#meta/example_service.cmx"
            }
        }
    },
    "sandbox": {
        "services": [
            "fuchsia.example.Service"
        ]
    }
}
```
 

For a more thorough description of what is valid in a component manifest, please see the [documentation on component manifests][component_manifest]. 有关组件清单中有效内容的更详尽说明，请参见[有关组件清单的文档] [component_manifest]。

 
### Component and package build rules  组件和包的构建规则 

With a component manifest written the GN build rule can now be added to create a package that holds the test component. 编写组件清单后，现在可以添加GN构建规则以创建包含测试组件的软件包。

```GN
import("//build/test/test_package.gni")

test_package("hello_world_rust_tests") {
  deps = [
    ":bin",
  ]
  tests = [
    {
      name = "hello_world_rust_bin_test"
    }
  ]
}
```
 

This example will produce a new package named `hello_world_rust_tests` that contains the artifacts necessary to run a test component. This example requiresthat the `:bin` target produce a test binary named `hello_world_rust_bin_test`. 这个例子将产生一个名为`hello_world_rust_tests`的新包，其中包含运行测试组件所必需的工件。这个例子要求`：bin`目标产生一个名为`hello_world_rust_bin_test`的测试二进制文件。

The `test_package` template requires that `meta/${TEST_NAME}.cmx` exist and that the destination of the test binary match the target name. In this example, thismeans that `meta/hello_world_rust_bin_test.cmx` must exist. This templateproduces a package in the same way that the `package` template does, but it hasextra checks in place to ensure that the test is set up properly. For moreinformation, please  see the [documentation on `test_package`][test_package]. “ test_package”模板要求存在“ meta / $ {TEST_NAME} .cmx”，并且测试二进制文件的目标与目标名称匹配。在这个例子中，这意味着`meta / hello_world_rust_bin_test.cmx`必须存在。这个模板产生的软件包的方式与`package`模板相同，但是它进行了额外的检查以确保测试正确设置。有关更多信息，请参见[test_package上的文档] [test_package]。

 
## Running tests  运行测试 

Warning: This is an experimental test command.  警告：这是一个实验性的测试命令。

To test the package, use the `fx test` command with the name of the package:  要测试软件包，请使用带有软件包名称的`fx test`命令：

```bash
$ fx test ${TEST_PACKAGE_NAME}
```
 

If the package you specified is a test component, the command makes your Fuchsia device load and run said component. However, if the package you specified is ahost test, the command directly invokes that test binary. 如果您指定的软件包是测试组件，则该命令将使您的Fuchsia设备加载并运行该组件。但是，如果您指定的软件包是主机测试，则该命令将直接调用该测试二进制文件。

 
### Customize `fx test` invocations  自定义“ fx测试”调用 

In most cases, you should run the entire subset of test that verify the code that you are editing. You can run `fx test` with arguments to run specific testsor test suites, and flags to filter down to just host or device tests. Tocustomize `fx test`: 在大多数情况下，您应该运行测试的整个子集，以验证正在编辑的代码。您可以运行带有参数的“ fx test”来运行特定的测试或测试套件，并使用标记过滤以仅针对主机或设备测试。要自定义“ fx测试”：

```bash
fx test [FLAGS] [TEST [TEST [...]]]
```
 

 
### Three Ways to Specify a Test  指定测试的三种方法 

`fx test` supports multiple ways to reference a specific test.  “ fx测试”支持多种引用特定测试的方法。

 
1. Full or partial paths:  1.完整或部分路径：

    Provide a partial path to match against all test binaries in children directories. 提供部分路径以匹配子目录中的所有测试二进制文件。

    ```
    $ fx test //host_x64/gen/sdk
    ```
 

    Provide a full path to match against that exact binary.  提供完整路径以与该确切二进制文件进行匹配。

    ```
    $ fx test //host_x64/pm_cmd_pm_genkey_test
    ```
 

    Note: `//` stands for the root of a Fuchsia tree checkout.  注意：`//`代表紫红色的树结帐的根。

 
2. Full or partial [Fuchsia Package URLs][fuchsia_package_url]:  2.全部或部分[Fuchsia Package URL] [fuchsia_package_url]：

    Provide a partial URL to match against all test components whose Package URLs start with the supplied value. 提供一个部分URL，以匹配其Package URL以提供的值开头的所有测试组件。

    ```
    $ fx test fuchsia-pkg://fuchsia.com/slider_mod_tests
    ```
 

    Provide a full URL to match against that exact test component.  提供完整的URL以与该确切的测试组件相匹配。

    ```
    $ fx test fuchsia-pkg://fuchsia.com/slider_mod_tests#meta/slider_mod_tests.cmx
    ```
 

 
3. Test name:  3.测试名称：

    Supplying the common name for either host tests (likely a binary) or device test (a Fuchsia component) is supported. This name value is found in thebuild directory’s `tests.json` manifest file, under the `"name"` key or asthe first URI segment in a Package URL. 支持为主机测试（可能是二进制文件）或设备测试（紫红色的组件）提供通用名称。该名称值可在构建目录的“ tests.json”清单文件中的“名称”键下找到，也可以作为Package URL中的第一个URI段找到。

    ```
    $ fx test slider_mod_tests
    ```
 

 
### Running multiple tests  运行多个测试 

If you want to run multiple sets of Fuchsia tests, configure your Fuchsia build to include several of the primary testing bundles, build Fuchsia, and then runall tests in the build: 如果要运行多组Fuchsia测试，请配置Fuchsia构建以包括多个主要测试包，构建Fuchsia，然后在构建中运行所有测试：

```bash
fx set core.x64 --with //bundles:tools,//bundles:tests,//garnet/packages/tests:all
fx build
fx test
```
 

 

 
## Running tests (Legacy)  运行测试（旧版） 

Tests can be exercised with the `fx run-test` command by providing the name of the package containing the tests. 通过提供包含测试的软件包的名称，可以使用“ fx run-test”命令来执行测试。

```bash
$ fx run-test ${TEST_PACKAGE_NAME}
```
 

This command will rebuild any modified files, push the named package to the device, and run it. 此命令将重建所有修改过的文件，将命名包推送到设备，然后运行它。

Tests can also be run directly from the shell on a Fuchsia device with the `run-test-component` command, which can take either a fuchsia-pkg URL or aprefix to search pkgfs for. 也可以使用“ run-test-component”命令在Fuchsia设备上直接从外壳运行测试，该命令可以使用fuchsia-pkg URL或前缀来搜索pkgfs。

If using a fuchsia-pkg URL the test will be automatically updated on the device, but not rebuilt like if `fx run-test` was used. The test will be neither rebuiltnor updated if a prefix is provided. 如果使用的是fuchsia-pkg URL，则测试将在设备上自动更新，但不会像使用`fx run-test`那样进行重建。如果提供了前缀，则既不会重建测试也不会更新测试。

In light of the above facts, the recommended way to run tests from a Fuchsia shell is: 鉴于上述事实，从紫红色的外壳运行测试的推荐方法是：

```bash
$ run-test-component `locate ${TEST_PACKAGE_NAME}`
```
 

The `locate` tool will search for and return fuchsia-pkg URLs based on a given search query. If there are multiple matches for the query the above command willfail, so `locate` should be invoked directly to discover the URL that should beprovided to `run-test-component` “ locate”工具将根据给定的搜索查询来搜索并返回紫红色pkg URL。如果查询有多个匹配项，则上述命令将失败，因此应直接调用“ locate”以发现应提供给“ run-test-component”的URL。

