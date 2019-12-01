 
## Magma Contributing and Best Practices  岩浆贡献和最佳实践 

 
### Submitting a patch  提交补丁 

See [Contributing](/CONTRIBUTING.md).  请参阅[贡献]（/ CONTRIBUTING.md）。

 
### Source Code  源代码 

The source code for a magma graphics driver may be hosted entirely within the garnet repository.  岩浆图形驱动程序的源代码可以完全托管在石榴石存储库中。

The core magma code is found under:  核心岩浆代码位于：

 
* [lib/magma/src](/garnet/lib/magma/src)  * [lib / magma / src]（/ garnet / lib / magma / src）

Implementations of the magma service drivers are found under:  岩浆服务驱动程序的实现位于：

 
* [drivers/gpu](/garnet/drivers/gpu)  * [drivers / gpu]（/ garnet / drivers / gpu）

Implementations of the magma application driver may be located in drivers/gpu; though often these are built from third party projects, such as third_party/mesa. 岩浆应用程序驱动程序的实现可以位于drivers / gpu中。尽管这些通常是由第三方项目（例如，third_party / mesa）构建的。

 
### Coding Conventions and Formatting  编码约定和格式 

 
* Use the **[Google style guide](https://google.github.io/styleguide/cppguide.html)** for source code.  *使用** [Google样式指南]（https://google.github.io/styleguide/cppguide.html）**作为源代码。
* Run **clang-format** on your changes to maintain consistent formatting.  *对更改运行** clang-format **，以保持一致的格式。

 
### Build Configuration for Testing  构建测试配置 

 
##### Product for L0 and L1 testing:  L0和L1测试产品： 
* core  *核心

 
##### Packages for L0 and L1 testing:  L0和L1测试的软件包： 
* src/graphics/lib/magma/tests:l1  * src / graphics / lib / magma / tests：l1

 
##### Product for L2 testing:  L2测试产品： 
* workstation  *工作站

 
##### Package for L2 testing:  L2测试套件： 
* topaz/app/spinning_cube  *黄玉/ app / spinning_cube

 
### Testing Pre-Submit  测试预提交 

For details on the testing strategy for magma, see [Test Strategy](test_strategy.md).  有关岩浆的测试策略的详细信息，请参见[测试策略]（test_strategy.md）。

There are multiple levels for magma TPS.  Each level includes all previous levels.  岩浆TPS有多个级别。每个级别包括所有以前的级别。

When submitting a change you must indicate the TPS level tested, preface by the hardware on which the testing was performed: 提交更改时，您必须指明已测试的TPS级别，并以执行测试的硬件作为序言：

TEST:   nuc,vim2:go/magma-tps#L2nuc,vim2:go/magma-tps#S1nuc,vim2:go/magma-tps#C0nuc,vim2:go/magma-tps#P0 测试：nuc，vim2：go / magma-tpsL2nuc，vim2：go / magma-tpsS1nuc，vim2：go / magma-tpsC0nuc，vim2：go / magma-tpsP0

 
#### L0  L0 

Includes all unit tests and integration tests.  There are 2 steps at this tps level:  包括所有单元测试和集成测试。此tps级别有2个步骤：

 
1. Build with --args magma_enable_developer_build=true; this will run unit tests that require hardware, then present the device as usual for general applications.  Inspect the syslog for test results. 1.使用--args magma_enable_developer_build = true进行构建；这将运行需要硬件的单元测试，然后像常规应用一样照常显示该设备。检查系统日志以获取测试结果。

 
2. Run the test script [lib/magma/scripts/test.sh](/garnet/lib/magma/scripts/test.sh) and inspect the test results.  2.运行测试脚本[lib / magma / scripts / test.sh]（/ garnet / lib / magma / scripts / test.sh）并检查测试结果。

 
#### L1  L1 

If you have an attached display, execute the spinning [vkcube](/src/graphics/examples/vkcube). This test uses an imagepipe swapchain to pass frames to the system compositor.Build with `--with src/graphics/lib/magma/tests:l1`.Run the test with `run fuchsia-pkg://fuchsia.com/present_view#meta/present_view.cmx fuchsia-pkg://fuchsia.com/vkcube_on_scenic#meta/vkcube_on_scenic.cmx`. 如果您有附属的显示器，请执行旋转的[vkcube]（/ src / graphics / examples / vkcube）。该测试使用一个图像管道交换链将帧传递给系统合成器。使用--with src / graphics / lib / magma / tests：l1进行构建。使用run fuchsia-pkg：//fuchsia.com/present_viewmeta运行该测试/present_view.cmx fuchsia-pkg：// fuchsia.com / vkcube_on_scenicmeta / vkcube_on_scenic.cmx`。

 
#### L2  L2 

A full UI 'smoke' test. Build the entire product including your change.    完整的UI“烟熏”测试。构建包括变更在内的整个产品。

Login as Guest on the device and run both of these commands: ./scripts/fx shell sessionctl  --story_name=spinning_cube --mod_name=spinning_cube --mod_url=spinning_cube add_mod spinning_cube./scripts/fx shell sessionctl  --story_name=spinning_cube2 --mod_name=spinning_cube2 --mod_url=spinning_cube add_mod spinning_cube 以访客身份在设备上登录并运行以下两个命令：./scripts/fx shell sessionctl --story_name = spinning_cube --mod_name = spinning_cube --mod_url = spinning_cube add_mod Spinning_cube./scripts/fx shell sessionctl --story_name = spinning_cube2- -mod_name = spinning_cube2 --mod_url = spinning_cube add_mod Spinning_cube

For details, refer to top level project documentation.  有关详细信息，请参阅顶层项目文档。

 
#### S0  S0 

For stress testing, run the test script [lib/magma/scripts/stress.sh](/garnet/lib/magma/scripts/stress.sh) and ensure that the driver does not leak resources over time. 对于压力测试，请运行测试脚本[lib / magma / scripts / stress.sh]（/ garnet / lib / magma / scripts / stress.sh），并确保驱动程序不会随时间泄漏资源。

 
#### S1  S1 

A full UI stress test.  Launch the spinning_cube example and the infinite_scroller, and let them run overnight.  完整的UI压力测试。启动spinning_cube示例和infinite_scroller，然后让它们运行一整夜。

 
#### C0  C0 

For some changes, it's appropriate to run the Vulkan conformance test suite before submitting. See [Conformance](#conformance). 对于某些更改，在提交之前运行Vulkan一致性测试套件是适当的。请参阅[符合性]（符合性）。

 
#### P0  P0 

For some changes, it's appropriate to run benchmarks to validate performance metrics. See [Benchmarking](#benchmarking).  对于某些更改，运行基准测试以验证性能指标是适当的。请参阅[基准测试]（基准测试）。

 
### Conformance  符合标准 

For details on the Vulkan conformance test suite, see  有关Vulkan一致性测试套件的详细信息，请参阅

 
* [../third_party/vulkan-cts](/third_party/vulkan-cts)  * [../third_party/vulkan-cts](/third_party/vulkan-cts）

 
### Benchmarking  标杆管理 

The source to Vulkan gfxbench is access-restricted. It should be cloned into third_party.  Vulkan gfxbench的源受到访问限制。应该将其克隆到third_party。

 
* https://fuchsia-vendor-internal.googlesource.com/gfxbench  * https://fuchsia-vendor-internal.googlesource.com/gfxbench

 
### See Also  也可以看看 
