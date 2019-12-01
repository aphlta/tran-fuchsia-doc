 
# Testing Scenic and Escher  测试Scenic和Escher 

 
## Testability  可测性 

Information about testability:  有关可测试性的信息：

 
* All changes within Fuchsia need to adhere to the [Testability rubric](/docs/development/testing/testability_rubric.md).  *紫红色中的所有更改都必须遵守[Testability rubric]（/文档/开发/测试/testability_rubric.md）。
* See also: [general Fuchsia testing documentation](/docs/development/testing/environments.md)  *另请参见：[紫红色的常规测试文档]（/ docs / development / testing / environments.md）

 
## Scenic test packages  风景测试包 

You can specify packages in these ways:  您可以通过以下方式指定软件包：

 
* Everything:  *一切：

  ```
  --with //bundles:tests
  ```
 

 
* Individually, if you want to build less packages:  *单独地，如果您想减少软件包的数量：

  ```
  --with //garnet/packages/tests:scenic
  --with //garnet/packages/tests:scenic_cpp
  --with //garnet/packages/tests:escher
  --with //garnet/packages/tests:ui
  --with //garnet/packages/tests:e2e_input_tests
  --with //garnet/packages/tests:vulkan
  --with //garnet/packages/tests:magma
  ```
 

 
## Scenic and CQ  风景名胜区 

Trybots run tests automatically before submission of every change in Fuchsia. See the "fuchsia-x64-release" and "fuchsia-x64-debug" bots on [https://ci.chromium.org/p/fuchsia/builders](https://ci.chromium.org/p/fuchsia/builders). 在提交紫红色的所有更改之前，Trybots会自动运行测试。请参阅[https://ci.chromium.org/p/fuchsia/builders]上的“ fuchsia-x64-release”和“ fuchsia-x64-debug”机器人（https://ci.chromium.org/p/fuchsia / builders）。

 
## Unit tests and integration tests  单元测试和集成测试 

To run tests locally during development:  在开发过程中本地运行测试：

 
### Running on device  在设备上运行 

Some of these tests require the test Scenic to connect to the real display controller.  其中一些测试需要将Scenic测试连接到实际的显示控制器。

Run `fx shell killall scenic.cmx` to kill an active instance of Scenic.  运行`fx shell killall Scenic.cmx`杀死一个活动的Scenic实例。

 
* Run all Scenic tests:  *运行所有布景测试：

  From host workstation, ensure `fx serve` is running, then:  在主机工作站上，确保“ fx serve”正在运行，然后：

  ```
  fx run-test scenic_tests
  fx run-test escher_tests
  fx run-test flutter_screencap_test
  ```
 

  From Fuchsia target device:  从紫红色目标设备：

  ```
  runtests -t gfx_apptests,gfx_unittests,escher_unittests,input_unittests,a11y_manager_apptests
  ```
 

 
* Run a specific test binary:  *运行特定的测试二进制文件：

  From host workstation, ensure `fx serve` is running, then:  在主机工作站上，确保“ fx serve”正在运行，然后：

  ```
  fx run-test scenic_tests -t gfx_unittests  # -t <test binary name>
  ```
 

  From Fuchsia target device:  从紫红色目标设备：

  ```
  runtests -t gfx_unittests
  ```
 

 
* Run a single test:  *运行一个测试：

  From host workstation, ensure `fx serve` is running, then:  在主机工作站上，确保“ fx serve”正在运行，然后：

  ```
  fx run-test scenic_tests -t gfx_unittests -- --gunit_filter=HostImageTest.FindResource
  ```
 

  From Fuchsia target device:  从紫红色目标设备：

  ```
  runtests -t gfx_unittests -- --gtest_filter=HostImageTest.FindResource
  ```
 

  See more documentation about the [glob pattern for the filter arg](https://github.com/google/googletest/blob/master/googletest/docs/advanced.md).  请参阅有关[过滤器arg的全局模式的更多文档]（https://github.com/google/googletest/blob/master/googletest/docs/advanced.md）。

 
* Run a specific component  *运行特定的组件

  From your host workstation:  从您的主机工作站：

  ```
  fx shell run-test-component fuchsia-pkg://fuchsia.com/scenic_tests#meta/gfx_unittests.cmx
  ```
 

  Note: `gfx_unittests.cmx` can be swapped for [any test component](/src/ui/scenic/BUILD.gn) . There is also fuzzy matching!  注意：gfx_unittests.cmx可以交换为[任何测试组件]（/ src / ui / scenic / BUILD.gn）。还有模糊匹配！

 
* Pixel tests  *像素测试

  If you get an error connecting to a display controller, first kill all UI services.  如果在连接显示控制器时遇到错误，请首先终止所有UI服务。

  From your host workstation, run:  在主机工作站上，运行：

  ```
  fx shell "killall base_mgr.cmx; killall root_presenter.cmx; killall scenic.cmx; killall tiles.cmx; killall present_view"
  ```
 

  Then run the pixel tests:  然后运行像素测试：

  ```
  fx shell run fuchsia-pkg://fuchsia.com/scenic_tests#meta/gfx_pixeltests.cmx
  ```
 

  Alternatively, run:  或者，运行：

  ```
  fx shell runtests -t gfx_pixeltests
  ```
 

  Note: `gfx_pixeltests` currently requires `//bundles:tests` to be in your list of packages (e.g., `fx set [...] --with //bundles:tests`)  注意：gfx_pixeltests当前要求将“ // bundles：tests”添加到您的软件包列表中（例如，“ fx set [...] --with // bundles：tests`”）

 
### Running on emulator  在模拟器上运行 

From your host workstation:  从您的主机工作站：

```
fx set terminal.x64 --release --with-base //garnet/packages/tests:scenic
```
 

Then, start an emulator:  然后，启动一个仿真器：

 
* Start QEMU:  *启动QEMU：

  ```
  fx qemu
  ```
 

 
* Start AEMU:  *启动AEMU：

  ```
  fx emu -N
  ```
 

Then, in the QEMU or EMU shell:  然后，在QEMU或EMU Shell中：

```
runtests -t gfx_apptests,gfx_unittests,escher_unittests,input_unittests,a11y_manager_apptests
```
 

 
### Host tests  主机测试 

 
* `fx run-host-tests` will run all the host tests, but you probably only want to run Escher tests.  *`fx run-host-tests`将运行所有主机测试，但是您可能只想运行Escher测试。
